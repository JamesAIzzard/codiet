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

