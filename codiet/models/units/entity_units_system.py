from codiet.utils.map import Map
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.entity_unit_conversion import EntityUnitConversion
from collections import deque

class EntityUnitsSystem:
    """
    Represents a system for managing entity units and conversions.
    """

    def __init__(
        self,
        global_units: set[Unit]|None = None,
        global_unit_conversions: set[UnitConversion]|None = None,
        entity_unit_conversions: set[EntityUnitConversion]|None = None
    ):
        """Initialises the EntityUnitsSystem object."""

        self._global_units = global_units or set()
        self._global_unit_conversions = global_unit_conversions or set()
        self._entity_unit_conversions = entity_unit_conversions or set()

        self._graph: dict[Unit, dict[Unit, float]] = {}
        self._path_cache: dict[tuple[Unit, Unit], list[tuple[Unit, Unit]]] = {}
        self._name_unit_map: Map[str, Unit]|None = None
        self._gram: Unit|None = None
        self._update()        

    @property
    def gram(self) -> Unit:
        """Retrieves the gram unit."""
        return self.get_unit("gram")

    @property
    def global_units(self) -> frozenset[Unit]:
        """Retrieves the global units."""
        return frozenset(self._global_units)
    
    @property
    def entity_unit_conversions(self) -> frozenset[EntityUnitConversion]:
        """Retrieves the entity unit conversions."""
        return frozenset(self._entity_unit_conversions)

    @entity_unit_conversions.setter
    def entity_unit_conversions(self, entity_unit_conversions: set[EntityUnitConversion]):
        """Replaces the existing entity unit conversions with a new list."""
        self._entity_unit_conversions = entity_unit_conversions
        self._update()

    def get_unit(self, unit_name:str) -> Unit:
        """Retrieves a unit by its name."""
        if self._name_unit_map is None:
            self._cache_name_unit_map()
        unit = self._name_unit_map.get_value(unit_name) # type: ignore # cache guarantees map is not None
        if unit is None:
            raise ValueError(f"Unit {unit_name} not found.")
        return unit

    def update_entity_unit_conversions(self, entity_unit_conversions: set[EntityUnitConversion]):
        """Adds entity unit conversions to the existing list."""
        for conversion in entity_unit_conversions:
            if conversion in self._entity_unit_conversions:
                # Replace with the new version
                self._entity_unit_conversions.remove(conversion)
                self._entity_unit_conversions.add(conversion)
            else:
                # Add the new one
                self._entity_unit_conversions.add(conversion)
        # Rebuild everything
        self._update()

    def can_convert_units(self, from_unit: Unit, to_unit:Unit) -> bool:
        """Checks if two units can be converted between."""
        try:
            self._find_conversion_path(from_unit, to_unit)
            return True
        except ValueError:
            return False

    def get_conversion_factor(self, from_unit: Unit, to_unit: Unit) -> float:
        """
        Calculates the conversion factor between two unit IDs.
        To go from 'from_unit' to 'to_unit', we multiply the first unit qty by the factor.

        Raises:
            ValueError: If no conversion path is found between the given units.
        """
        path = self._find_conversion_path(from_unit, to_unit)
        factor = 1.0
        for u1, u2 in path:
            factor *= self._graph[u1][u2]
        return factor

    def convert_units(self, quantity: float, from_unit: Unit, to_unit: Unit) -> float:
        """
        Converts a quantity from one unit to another.

        Raises:
            ValueError: If no conversion path is found between the given unit IDs.
        """
        conversion_factor = self.get_conversion_factor(from_unit, to_unit)
        return quantity * conversion_factor

    def rescale_quantity(
            self,
            ref_from_unit: Unit,
            ref_to_unit: Unit,
            ref_from_quantity: float,
            ref_to_quantity: float,
            quantity: float,
    ) -> float:
        """
        Rescales a quantity based on a change in a reference quantity.
        """
        ref_from_quantity_base = self.convert_units(ref_from_quantity, ref_from_unit, self.gram)
        ref_to_quantity_base = self.convert_units(ref_to_quantity, ref_to_unit, self.gram)
        quantity_base = self.convert_units(quantity, ref_from_unit, self.gram)

        scaling_factor = quantity_base / ref_from_quantity_base
        result_base = ref_to_quantity_base * scaling_factor
        result = self.convert_units(result_base, self.gram, ref_to_unit)

        return result

    def get_available_units(self, root_unit: Unit|None=None) -> list[Unit]:
        """
        Retrieves all available units starting from a root unit ID.
        If the root unit ID is None, the root unit is assumed to be grams.
        """
        if root_unit is None:
            root_unit = self.gram

        visited = set()
        queue = deque([root_unit])
        available_units = []

        while queue:
            unit = queue.popleft()
            if unit not in visited:
                visited.add(unit)
                available_units.append(unit)
                queue.extend(set(self._graph.get(unit, {}).keys()) - visited)

        return available_units

    def clear_path_cache(self):
        """
        Clears the conversion path cache.
        """
        self._path_cache.clear()

    def _find_conversion_path(self, from_unit: Unit, to_unit: Unit) -> list[tuple[Unit, Unit]]:
        """
        Finds a conversion path between two units using BFS.
        """
        cache_key = (from_unit, to_unit)
        if cache_key in self._path_cache:
            return self._path_cache[cache_key]

        queue = deque([(from_unit, [])])
        visited = set()

        while queue:
            current_unit, path = queue.popleft()
            if current_unit == to_unit:
                self._path_cache[cache_key] = path
                return path

            if current_unit not in visited:
                visited.add(current_unit)
                for next_unit in self._graph.get(current_unit, {}):
                    if next_unit not in visited:
                        new_path = path + [(current_unit, next_unit)]
                        queue.append((next_unit, new_path))

        raise ValueError(f"No conversion path found between {from_unit.unit_name} and {to_unit.unit_name}")

    def _update(self):
        """Updates the object to reflect the latest units and conversions."""
        self._cache_name_unit_map()

        self._graph.clear()
        self._path_cache.clear()
        all_conversions = self._global_unit_conversions.union(self._entity_unit_conversions)

        for conv in all_conversions:
            if conv.from_unit not in self._graph:
                self._graph[conv.from_unit] = {}
            if conv.to_unit not in self._graph:
                self._graph[conv.to_unit] = {}
            
            self._graph[conv.from_unit][conv.to_unit] = conv.ratio
            self._graph[conv.to_unit][conv.from_unit] = 1 / conv.ratio

    def _cache_name_unit_map(self):
        """Caches the name-unit map."""
        # Create the map if was None
        if self._name_unit_map is None:
            self._name_unit_map = Map[str, Unit]()
        # Recreate the map
        self._name_unit_map.clear()
        for unit in self._global_units:
            self._name_unit_map.add_mapping(unit.unit_name, unit)
        