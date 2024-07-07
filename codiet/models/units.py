class Unit:
    """Models a measurement unit."""

    def __init__(
        self,
        id: int,
        unit_name: str,
        single_display_name: str,
        plural_display_name: str,
        type: str,
        aliases: list[str]|None = None
    ):
        self.id = id
        self.unit_name = unit_name
        self.single_display_name = single_display_name
        self.plural_display_name = plural_display_name
        self.type = type
        self.aliases = aliases or [] # Default to an empty list if None

class UnitConversion:
    """Models the conversion between two units."""

    def __init__(
            self, 
            id:int, 
            from_unit_id: int, 
            to_unit_id: int, 
            from_unit_qty: float|None = None,
            to_unit_qty: float|None = None,
        ):
        """
        Initialise the UnitConversion object.

        Args:
            id (int): The id of the conversion.
            from_unit_id (int): The id of the unit to convert from.
            to_unit_id (int): The id of the unit to convert to.
            from_unit_qty (float, optional): The quantity of the from unit. Defaults to None.
            to_unit_qty (float, optional): The quantity of the to unit. Defaults to None.
        """
        self.id = id
        self.from_unit_id = from_unit_id
        self.from_unit_qty = from_unit_qty
        self.to_unit_id = to_unit_id
        self.to_unit_qty = to_unit_qty

    def __eq__(self, other):
        if not isinstance(other, UnitConversion):
            return NotImplemented
        return (self.from_unit_id, self.to_unit_id) == (other.from_unit_id, other.to_unit_id) or \
               (self.from_unit_id, self.to_unit_id) == (other.to_unit_id, other.from_unit_id)

    @property
    def is_populated(self) -> bool:
        """Returns True if the conversion is populated."""
        return self.from_unit_qty is not None and self.to_unit_qty is not None

    @property
    def ratio(self) -> float:
        """Returns the ratio between the two units."""
        # Raise an exception if either id or qty is None
        if self.is_populated is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return self.to_unit_qty / self.from_unit_qty # type: ignore
    
    def convert_from_to(self, qty: float) -> float:
        """Converts a quantity from the from unit to the to unit."""
        # Raise an exception if either id or qty is None
        if self.is_populated is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return qty * self.ratio
    
    def convert_to_from(self, qty: float) -> float:
        """Converts a quantity from the to unit to the from unit."""
        # Raise an exception if either id or qty is None
        if self.is_populated is False:
            raise ValueError("Both from_unit_qty and to_unit_qty must be set.")
        return qty / self.ratio

class IngredientUnitConversion(UnitConversion):
    """Models the conversion between two units specifically associated with an ingredient."""

    def __init__(
        self,
        ingredient_id: int,
        *args, **kwargs
    ):
        """Initializes the IngredientUnitConversion object.
        Extends the UnitConversion object with an ingredient_id.
        Args:
            id (int): The id of the conversion.
            ingredient_id (int): The id of the ingredient.
            from_unit_id (int): The id of the unit to convert from.
            to_unit_id (int): The id of the unit to convert to.
            from_unit_qty (float): The quantity of the from unit.
            to_unit_qty (float): The quantity of the to unit.
        """
        super().__init__(*args, **kwargs)
        self.ingredient_id = ingredient_id

class IngredientUnitsSystem:
    """
    Represents a system for managing ingredient units and conversions.
    """

    def __init__(
        self,
        global_units: dict[int, Unit],
        global_unit_conversions: dict[int, UnitConversion],
        ingredient_unit_conversions: dict[int, IngredientUnitConversion]
    ):
        """
        Initialises the IngredientUnitsSystem object.

        Args:
            global_units (dict[int, Unit]): A dictionary mapping unit IDs to global units.
            global_unit_conversions (dict[int, UnitConversion]): A dictionary mapping conversion IDs to global unit conversions.
            ingredient_unit_conversions (dict[int, IngredientUnitConversion]): A dictionary mapping conversion IDs to ingredient unit conversions.
        """
        self.global_units = global_units
        self.global_unit_conversions = global_unit_conversions
        self.ingredient_unit_conversions = ingredient_unit_conversions
        self.graph: dict[int, dict[int, float]] = {}
        self.path_cache: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self._build_graph()

    def _build_graph(self):
        """
        Builds the graph representation of unit conversions.
        """
        self.graph.clear()
        self.path_cache.clear()
        all_conversions = list(self.global_unit_conversions.values()) + list(self.ingredient_unit_conversions.values())

        for conv in all_conversions:
            if conv.from_unit_id not in self.graph:
                self.graph[conv.from_unit_id] = {}
            if conv.to_unit_id not in self.graph:
                self.graph[conv.to_unit_id] = {}
            
            self.graph[conv.from_unit_id][conv.to_unit_id] = conv.ratio
            self.graph[conv.to_unit_id][conv.from_unit_id] = 1 / conv.ratio

    def update_graph(
        self,
        global_unit_conversions: dict[int, UnitConversion] | None = None,
        ingredient_unit_conversions: dict[int, IngredientUnitConversion] | None = None
    ):
        """
        Updates the graph representation of unit conversions.

        Args:
            global_unit_conversions (dict[int, UnitConversion] | None): A dictionary mapping conversion IDs to global unit conversions. If None, the existing global unit conversions will not be updated.
            ingredient_unit_conversions (dict[int, IngredientUnitConversion] | None): A dictionary mapping conversion IDs to ingredient unit conversions. If None, the existing ingredient unit conversions will not be updated.
        """
        if global_unit_conversions is not None:
            self.global_unit_conversions = global_unit_conversions
        if ingredient_unit_conversions is not None:
            self.ingredient_unit_conversions = ingredient_unit_conversions
        self._build_graph()

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
        if cache_key in self.path_cache:
            return self.path_cache[cache_key]

        queue = [(from_unit_id, [])]
        visited = set()

        while queue:
            current_unit_id, path = queue.pop(0)
            
            if current_unit_id == to_unit_id:
                self.path_cache[cache_key] = path
                return path

            if current_unit_id in visited:
                continue

            visited.add(current_unit_id)

            for next_unit_id in self.graph.get(current_unit_id, {}):
                if next_unit_id not in visited:
                    queue.append((next_unit_id, path + [(current_unit_id, next_unit_id)]))

        raise ValueError(f"No conversion path found from unit ID {from_unit_id} to unit ID {to_unit_id}")

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
            factor *= self.graph[start][end]

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

    def get_available_units(self, root_unit_id: int) -> dict[int, Unit]:
        """
        Retrieves all available units starting from a root unit ID.

        Args:
            root_unit_id (int): The ID of the root unit.

        Returns:
            Dict[int, Unit]: A dictionary mapping unit IDs to units.
        """
        available_units = {}
        stack = [root_unit_id]
        visited = set()

        while stack:
            current_unit_id = stack.pop()
            if current_unit_id in visited:
                continue

            visited.add(current_unit_id)
            available_units[current_unit_id] = self.global_units[current_unit_id]

            for next_unit_id in self.graph.get(current_unit_id, {}):
                if next_unit_id not in visited:
                    stack.append(next_unit_id)

        return available_units

    def clear_path_cache(self):
        """
        Clears the conversion path cache.
        """
        self.path_cache.clear()

def get_available_units(
        root_unit: Unit,
        global_units: dict[int, Unit],
        global_unit_conversions: dict[int, UnitConversion],
        ingredient_unit_conversions: dict[int, IngredientUnitConversion],
) -> dict[int, Unit]:
    """Returns a list of units which are available to use on an ingredient.
    First builds a graph, where the nodes are global units and the edges are conversions.
    Then, starting at the root unit, traverses the graph to find all reachable units. Returns a
    dictionary of unit ids to units.
    Args:
        root_unit (Unit): The starting unit for conversion.
        global_units (dict[int, Unit]): The global units.
            int: The global unit ID.
            Unit: The global unit.
        global_unit_conversions (dict[int, UnitConversion]): The global unit conversions.
            int: The global unit conversion ID.
            UnitConversion: The global unit conversion.
        ingredient_unit_conversions (dict[int, IngredientUnitConversion]): The ingredient unit conversions.
            int: The ingredient unit conversion ID.
            IngredientUnitConversion: The ingredient unit conversion.
    Returns:
        dict[int, Unit]: The available units.
            int: The global unit ID.
            Unit: The global unit.
    """
    # Build the graph
    graph = {unit.id: [] for unit in global_units.values()}
    
    for unit_conversion in global_unit_conversions.values():
        graph[unit_conversion.from_unit_id].append(unit_conversion.to_unit_id)
        graph[unit_conversion.to_unit_id].append(unit_conversion.from_unit_id)
    
    for unit_conversion in ingredient_unit_conversions.values():
        graph[unit_conversion.from_unit_id].append(unit_conversion.to_unit_id)
        graph[unit_conversion.to_unit_id].append(unit_conversion.from_unit_id)
    
    # Traverse the graph using DFS to find all reachable units
    reachable_units = set()
    stack = [root_unit.id]
    
    while stack:
        unit_id = stack.pop()
        if unit_id in reachable_units:
            continue
        reachable_units.add(unit_id)
        stack.extend(graph[unit_id])
    
    return {unit_id: unit for unit_id, unit in global_units.items() if unit_id in reachable_units}

def convert_units(
    quantity: float,
    from_unit_id: int,
    to_unit_id: int,
    global_unit_conversions: dict[int, UnitConversion],
    ingredient_unit_conversions: dict[int, IngredientUnitConversion]
) -> float:
    """
    Converts a quantity from one unit to another using available conversions.

    Args:
        quantity (float): The quantity to convert.
        from_unit_id (int): The ID of the unit to convert from.
        to_unit_id (int): The ID of the unit to convert to.
        global_unit_conversions (dict[int, UnitConversion]): The global unit conversions.
        ingredient_unit_conversions (dict[int, IngredientUnitConversion]): The ingredient-specific unit conversions.

    Returns:
        float: The converted quantity.

    Raises:
        ValueError: If no conversion path is found between the units.
    """
    conversion_factor = _get_unit_conversion_factor(
        from_unit_id,
        to_unit_id,
        global_unit_conversions,
        ingredient_unit_conversions
    )
    return quantity * conversion_factor

def _get_unit_conversion_factor(
    from_unit_id: int,
    to_unit_id: int,
    global_unit_conversions: dict[int, UnitConversion],
    ingredient_unit_conversions: dict[int, IngredientUnitConversion]
) -> float:
    """
    Calculates the conversion factor between two units using available conversions.

    Args:
        from_unit_id (int): The ID of the unit to convert from.
        to_unit_id (int): The ID of the unit to convert to.
        global_unit_conversions (dict[int, UnitConversion]): The global unit conversions.
        ingredient_unit_conversions (dict[int, IngredientUnitConversion]): The ingredient-specific unit conversions.

    Returns:
        float: The conversion factor from the 'from' unit to the 'to' unit.

    Raises:
        ValueError: If no conversion path is found between the units.
    """
    # Check if units are the same
    if from_unit_id == to_unit_id:
        return 1.0

    # Combine global and ingredient-specific conversions
    all_conversions = list(global_unit_conversions.values()) + list(ingredient_unit_conversions.values())

    # Build a graph of unit connections
    graph = {}
    for conv in all_conversions:
        if conv.from_unit_id not in graph:
            graph[conv.from_unit_id] = {}
        if conv.to_unit_id not in graph:
            graph[conv.to_unit_id] = {}
        graph[conv.from_unit_id][conv.to_unit_id] = conv
        graph[conv.to_unit_id][conv.from_unit_id] = conv

    # Perform BFS to find the shortest conversion path
    queue = [(from_unit_id, 1.0, [])]
    visited = set()

    while queue:
        current_unit_id, current_factor, path = queue.pop(0)
        
        if current_unit_id == to_unit_id:
            return current_factor

        if current_unit_id in visited:
            continue

        visited.add(current_unit_id)

        for next_unit_id, conversion in graph.get(current_unit_id, {}).items():
            if next_unit_id not in visited:
                new_factor = current_factor
                if conversion.from_unit_id == current_unit_id:
                    new_factor *= conversion.ratio
                else:
                    new_factor /= conversion.ratio
                queue.append((next_unit_id, new_factor, path + [conversion]))

    raise ValueError(f"No conversion path found from unit ID {from_unit_id} to unit ID {to_unit_id}")
