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
        """Initialise the unit.
        Args:
            id (int): The unique ID of the unit.
            unit_name (str): The name of the unit.
            single_display_name (str): The singular display name of the unit.
            plural_display_name (str): The plural display name of the unit.
            type (str): The type of the unit.
            aliases (list[str]): The aliases of the unit.
        """
        self.id = id
        self.unit_name = unit_name
        self.single_display_name = single_display_name
        self.plural_display_name = plural_display_name
        self.type = type
        self.aliases = aliases or [] # Default to an empty list if None