from typing import TYPE_CHECKING, Collection
from collections import deque

from codiet.utils import MUC, IUC
from codiet.model.domain_service import UsesDomainService
from codiet.model.quantities import Quantity

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion

class UnitSystem(UsesDomainService):
    """Models a system of units and conversions associated with an entity."""

    def __init__(
        self,
        entity_unit_conversions: Collection['UnitConversion']|None = None
    ):
        super().__init__()
        self._entity_unit_conversions = MUC(entity_unit_conversions) or MUC['UnitConversion']()
        self._graph: dict['Unit', dict['Unit', float]] = {}
        self._path_cache: dict[tuple['Unit', 'Unit'], list[tuple['Unit', 'Unit']]] = {}
        self._update()

    @property
    def available_units(self) -> IUC['Unit']:
        """Retrieves all available units."""
        return IUC(self._get_available_units())

    @property
    def entity_unit_conversions(self) -> IUC['UnitConversion']:
        """Retrieves the entity unit conversions."""
        return IUC(self._entity_unit_conversions)

    def check_unit_available(self, unit: 'Unit') -> bool:
        """Checks if a unit is available in the system."""
        return unit in self.available_units

    def add_entity_unit_conversion(self, unit_conversion: 'UnitConversion'):
        """Adds entity unit conversions to the existing list."""
        self._entity_unit_conversions.add(unit_conversion)
        self._update()

    def remove_entity_unit_conversion(self, entity_unit_conversion: 'UnitConversion'):
        """Removes entity unit conversions from the existing list."""
        self._entity_unit_conversions.remove(entity_unit_conversion)
        self._update()

    def can_convert_units(self, from_unit: 'Unit', to_unit: 'Unit') -> bool:
        """Checks if two units can be converted between."""
        try:
            self._find_conversion_path(from_unit, to_unit)
            return True
        except ValueError:
            return False

    def convert_quantity(self, quantity: Quantity, to_unit: 'Unit') -> Quantity:
        """
        Converts a quantity from one unit to another.

        Raises:
            ValueError: If no conversion path is found between the given units.
        """
        if quantity.unit == to_unit:
            return quantity

        conversion_factor = self._get_conversion_factor(quantity.unit, to_unit)
        converted_value = quantity.value * conversion_factor if quantity.value is not None else None
        return Quantity(unit=to_unit, value=converted_value)

    def _get_conversion_factor(self, from_unit: 'Unit', to_unit: 'Unit') -> float:
        """
        Calculates the conversion factor between two units.
        To go from 'from_unit' to 'to_unit', we multiply the first unit qty by the factor.

        Raises:
            ValueError: If no conversion path is found between the given units.
        """
        path = self._find_conversion_path(from_unit, to_unit)
        factor = 1.0
        for u1, u2 in path:
            factor *= self._graph[u1][u2]
        return factor

    def _get_available_units(self, root_unit: 'Unit|None' = None) -> IUC['Unit']:
        """
        Retrieves all available units starting from a root unit.
        If the root unit is None, the root unit is assumed to be grams.
        """
        if root_unit is None:
            root_unit = self.domain_service.gram

        visited = set()
        queue = deque([root_unit])
        available_units = []

        while queue:
            unit = queue.popleft()
            if unit not in visited:
                visited.add(unit)
                available_units.append(unit)
                queue.extend(set(self._graph.get(unit, {}).keys()) - visited) # type: ignore

        return IUC(available_units)

    def _clear_path_cache(self):
        """Clears the conversion path cache."""
        self._path_cache.clear()

    def _find_conversion_path(self, from_unit: 'Unit', to_unit: 'Unit') -> list[tuple['Unit', 'Unit']]:
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

        raise ValueError(f"No conversion path found between {from_unit.name} and {to_unit.name}")

    def _update(self):
        """Updates the object to reflect the latest units and conversions."""
        self._graph.clear()
        self._path_cache.clear()
        all_conversions = list(self.domain_service.global_unit_conversions) + list(self._entity_unit_conversions)

        for conv in all_conversions:
            if conv.is_defined:
                from_unit, to_unit = conv.quantities[0].unit, conv.quantities[1].unit
                ratio = conv.quantities[1].value / conv.quantities[0].value if conv.quantities[0].value else 0

                if from_unit not in self._graph:
                    self._graph[from_unit] = {}
                if to_unit not in self._graph:
                    self._graph[to_unit] = {}

                self._graph[from_unit][to_unit] = ratio
                self._graph[to_unit][from_unit] = 1 / ratio