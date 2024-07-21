from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.entity_unit_conversion import EntityUnitConversion

class EntityUnitsSystem:
    """
    Represents a system for managing entity units and conversions.
    """

    def __init__(
        self,
        global_units: dict[int, Unit],
        global_unit_conversions: dict[int, UnitConversion],
        entity_unit_conversions: dict[int, EntityUnitConversion]
    ):
        """
        Initialises the EntityUnitsSystem object.

        Args:
            global_units (dict[int, Unit]): A dictionary mapping unit IDs to global units.
            global_unit_conversions (dict[int, UnitConversion]): A dictionary mapping conversion IDs to global unit conversions.
            entity_unit_conversions (dict[int, EntityUnitConversion]): A dictionary mapping conversion IDs to entity unit conversions.
        """
        self._global_units = global_units
        self._gram_id = next((unit_id for unit_id, unit in global_units.items() if unit.unit_name == "grams"))
        self._global_unit_conversions = global_unit_conversions
        self._entity_unit_conversions = entity_unit_conversions
        self._graph: dict[int, dict[int, float]] = {}
        self._path_cache: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self._build_graph()

    @property
    def global_units(self) -> dict[int, Unit]:
        """
        Retrieves all global units.

        Returns:
            Dict[int, Unit]: A dictionary mapping unit IDs to units.
        """
        return self._global_units
    
    @property
    def gram_id(self) -> int:
        """
        Retrieves the ID of the gram unit.

        Returns:
            int: The ID of the gram unit.
        """
        return self._gram_id
    
    @property
    def global_unit_conversions(self) -> dict[int, UnitConversion]:
        """
        Retrieves all global unit conversions.

        Returns:
            Dict[int, UnitConversion]: A dictionary mapping conversion IDs to global unit conversions.
        """
        return self._global_unit_conversions
    
    @global_unit_conversions.setter
    def global_unit_conversions(self, global_unit_conversions: dict[int, UnitConversion]):
        """
        Sets the global unit conversions.

        Args:
            global_unit_conversions (dict[int, UnitConversion]): A dictionary mapping conversion IDs to global unit conversions.
        """
        self._global_unit_conversions = global_unit_conversions
        self._build_graph()

    @property
    def available_units(self) -> dict[int, Unit]:
        """
        Retrieves all available units, based on a root unit of grams.

        Returns:
            Dict[int, Unit]: A dictionary mapping unit IDs to units.
        """
        return self.get_available_units(self._gram_id)

    @property
    def entity_unit_conversions(self) -> dict[int, EntityUnitConversion]:
        """
        Retrieves all entity unit conversions.

        Returns:
            Dict[int, EntityUnitConversion]: A dictionary mapping conversion IDs to entity unit conversions.
        """
        return self._entity_unit_conversions
    
    @entity_unit_conversions.setter
    def entity_unit_conversions(self, entity_unit_conversions: dict[int, EntityUnitConversion]):
        """
        Sets the entity unit conversions.
        Replaces the previous dict of entity unit conversions with a new one and rebuilds the graph.

        Args:
            entity_unit_conversions (dict[int, EntityUnitConversion]): A dictionary mapping conversion IDs to entity unit conversions.
        """
        self._entity_unit_conversions = entity_unit_conversions
        self._build_graph()

    def can_convert_units(self, from_unit_id: int, to_unit_id: int) -> bool:
        """
        Checks if two units can be converted between.

        Args:
            from_unit_id (int): The ID of the starting unit.
            to_unit_id (int): The ID of the target unit.

        Returns:
            bool: True if the units can be converted between, False otherwise.
        """
        try:
            self._find_conversion_path(from_unit_id, to_unit_id)
            return True
        except ValueError:
            return False

    def get_conversion_factor(self, from_unit_id: int, to_unit_id: int) -> float:
        """
        Calculates the conversion factor between two unit IDs.

        Args:
            from_unit_id (int): The ID of the starting unit.
            to_unit_id (int): The ID of the target unit.

        Returns:
            float: The conversion factor between the two units.

        Raises:
            ValueError: If no conversion path is found between the given unit IDs.
        """
        if from_unit_id == to_unit_id:
            return 1.0

        path = self._find_conversion_path(from_unit_id, to_unit_id)
        factor = 1.0

        for start, end in path:
            factor *= self._graph[start][end]

        return factor

    def convert_units(self, quantity: float, from_unit_id: int, to_unit_id: int) -> float:
        """
        Converts a quantity from one unit to another.

        Args:
            quantity (float): The quantity to be converted.
            from_unit_id (int): The ID of the starting unit.
            to_unit_id (int): The ID of the target unit.

        Returns:
            float: The converted quantity.

        Raises:
            ValueError: If no conversion path is found between the given unit IDs.
        """
        conversion_factor = self.get_conversion_factor(from_unit_id, to_unit_id)
        return quantity * conversion_factor

    def get_available_units(self, root_unit_id: int|None=None) -> dict[int, Unit]:
        """
        Retrieves all available units starting from a root unit ID.
        If the root unit ID is None, the root unit is assumed to be grams.

        Note:
            This is not a property because it allows for a parameter to
            specify the root unit ID from which to start the search.

        Args:
            root_unit_id (int): The ID of the root unit.

        Returns:
            Dict[int, Unit]: A dictionary mapping unit IDs to units.
        """
        if root_unit_id is None:
            root_unit_id = self._gram_id

        available_units = {}
        stack = [root_unit_id]
        visited = set()

        while stack:
            current_unit_id = stack.pop()
            if current_unit_id in visited:
                continue

            visited.add(current_unit_id)
            available_units[current_unit_id] = self._global_units[current_unit_id]

            for next_unit_id in self._graph.get(current_unit_id, {}):
                if next_unit_id not in visited:
                    stack.append(next_unit_id)

        return available_units

    def clear_path_cache(self):
        """
        Clears the conversion path cache.
        """
        self._path_cache.clear()

    def _find_conversion_path(self, from_unit_id: int, to_unit_id: int) -> list[tuple[int, int]]:
        """
        Finds a conversion path between two unit IDs.

        Args:
            from_unit_id (int): The ID of the starting unit.
            to_unit_id (int): The ID of the target unit.

        Returns:
            list[tuple[int, int]]: A list of unit ID pairs representing the conversion path.

        Raises:
            ValueError: If no conversion path is found between the given unit IDs.
        """
        cache_key = (from_unit_id, to_unit_id)
        if cache_key in self._path_cache:
            return self._path_cache[cache_key]

        queue = [(from_unit_id, [])]
        visited = set()

        while queue:
            current_unit_id, path = queue.pop(0)
            
            if current_unit_id == to_unit_id:
                self._path_cache[cache_key] = path
                return path

            if current_unit_id in visited:
                continue

            visited.add(current_unit_id)

            for next_unit_id in self._graph.get(current_unit_id, {}):
                if next_unit_id not in visited:
                    queue.append((next_unit_id, path + [(current_unit_id, next_unit_id)]))

        raise ValueError(f"No conversion path found from unit ID {from_unit_id} to unit ID {to_unit_id}")

    def _build_graph(self):
        """
        Builds the graph representation of unit conversions.
        """
        self._graph.clear()
        self._path_cache.clear()
        all_conversions = list(self._global_unit_conversions.values()) + list(self._entity_unit_conversions.values())

        for conv in all_conversions:
            if conv.from_unit_id not in self._graph:
                self._graph[conv.from_unit_id] = {}
            if conv.to_unit_id not in self._graph:
                self._graph[conv.to_unit_id] = {}
            
            self._graph[conv.from_unit_id][conv.to_unit_id] = conv.ratio
            self._graph[conv.to_unit_id][conv.from_unit_id] = 1 / conv.ratio
