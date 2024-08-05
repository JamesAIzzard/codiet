from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import DatabaseService
from codiet.db.repository import Repository
from codiet.utils.map import Map
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion

class UnitDBService():
    """Service for interacting with the unit database."""

    def __init__(self, repository: Repository, db_service: 'DatabaseService', *args, **kwargs):
        """Initialise the unit database service."""
        super().__init__(*args, **kwargs)

        # Stash the repository
        self._repository = repository
        self._database_service = db_service

        # Cache the unit id-name map
        self._unit_id_name_map: Map[int, str]|None = None

        # Cache a full list of global units, and global mass units
        self._global_units: dict[int, Unit]|None = None
        self._global_mass_units: dict[int, Unit]|None = None

        # Cache a full list of global unit conversions
        self._global_unit_conversions: dict[int, UnitConversion]|None = None

        # Cache the gram id. This the base unit, and used all over.
        self._gram_id: int|None = None

    @property
    def unit_id_name_map(self) -> Map[int, str]:
        """Return the unit ID to name map."""
        if self._unit_id_name_map is None:
            self._cache_unit_id_name_map()
        return self._unit_id_name_map # type: ignore # Checked in the if statement

    @property
    def gram_id(self) -> int:
        """Returns the ID of the gram unit."""
        if self._gram_id is None:
            self._gram_id = self.unit_id_name_map.get_key("gram")
        return self._gram_id    

    @property
    def global_units(self) -> dict[int, Unit]:
        """Returns all the global units."""
        if self._global_units is None:
            self._global_units = self.read_all_global_units()
        return self._global_units
    
    @property
    def global_mass_units(self) -> dict[int, Unit]:
        """Returns all the global mass units."""
        if self._global_mass_units is None:
            self._global_mass_units = self.read_all_global_mass_units()
        return self._global_mass_units
    
    @property
    def global_unit_conversions(self) -> dict[int, UnitConversion]:
        """Returns all the global unit conversions."""
        if self._global_unit_conversions is None:
            self._global_unit_conversions = self.read_all_global_unit_conversions()
        return self._global_unit_conversions

    def create_global_units(self, units: list[Unit]) -> dict[int, Unit]:
        """Insert a dictionary of global units into the database.

        Args:
            units (list[Unit]): The units to insert into the database.
        """
        # Init return dict
        persisted_units = {}

        # For each unit
        for unit in units:

            # Insert the unit name into the database
            unit_id = self._repository.create_global_unit(
                unit_name=unit._unit_name,
                unit_type=unit._type,
                single_display_name=unit._single_display_name,
                plural_display_name=unit._plural_display_name,
            )

            # Update thie id
            unit.id = unit_id

            # Insert the aliases for the unit
            for alias in unit._aliases:
                self._repository.create_global_unit_alias(
                    alias=alias,
                    unit_id=unit_id,
                )    

            persisted_units[unit.id] = unit

        return persisted_units

    def create_ingredient_unit_conversions(self, unit_conversions:list[IngredientUnitConversion]) -> dict[int, IngredientUnitConversion]:
        """Creates unit conversions for the given ingredient.
        Args:
            unit_conversions (list[EntityUnitConversion]): The unit conversions to create.
        Returns:
            dict[int, EntityUnitConversion]: A dictionary of the created unit conversions, where the key is the
            id of each specific unit conversion.
        """
        # Grab a list of all existing unit conversions
        existing_conversions = self.read_all_global_unit_conversions()
        # For each of the new ones, check equality with existing ones
        for unit_conversion in unit_conversions:
            for existing_conversion in existing_conversions.values():
                if unit_conversion == existing_conversion:
                    raise KeyError("Unit conversion already exists.")

        # Init a dict to hold the unit conversions
        persisted_unit_conversions = {}

        # For each unit conversion
        for unit_conversion in unit_conversions:
                
                # Check the parent entity id is set
                if unit_conversion.entity_id is None:
                    raise ValueError("Entity ID must be set.")

                # Insert the unit conversion into the database
                conversion_id = self._repository.create_ingredient_unit_conversion(
                    ingredient_id=unit_conversion.entity_id,
                    from_unit_id=unit_conversion.from_unit_id,
                    from_unit_qty=unit_conversion.from_unit_qty,
                    to_unit_id=unit_conversion.to_unit_id,
                    to_unit_qty=unit_conversion.to_unit_qty,
                )
    
                # Update the id
                unit_conversion.id = conversion_id
    
                persisted_unit_conversions[unit_conversion.id] = unit_conversion

        return persisted_unit_conversions

    def read_all_global_units(self) -> dict[int, Unit]:
        """Returns all the global units.
        Returns:
            dict[int, Unit]: A dictionary of global units, where the key is the
            id of each specific unit.
        """
        # Fetch the data for all the units
        all_units_data = self._repository.read_all_global_units()
        # Init a dict to hold the units
        units = {}
        # Cycle through the raw data
        for unit_id, unit_data in all_units_data.items():
            # Create a new unit
            units[unit_id] = Unit(
                id=unit_id,
                unit_name=unit_data["unit_name"],
                single_display_name=unit_data["single_display_name"],
                plural_display_name=unit_data["plural_display_name"],
                type=unit_data["unit_type"],
                aliases=unit_data["aliases"],
            )
        return units

    def read_all_global_mass_units(self) -> dict[int, Unit]:
        """Returns all the global mass units.
        Returns:
            dict[int, Unit]: A dictionary of global mass units, where the key is the
            id of each specific mass unit.
        """
        # Filter out only the mass units
        mass_units = {unit_id: unit for unit_id, unit in self.global_units.items() if unit._type == "mass"}
        # Return
        return mass_units

    def read_all_global_unit_conversions(self) -> dict[int, UnitConversion]:
        """Returns all the global unit conversions.
        Returns:
            dict[int, UnitConversion]: A dictionary of global unit conversions, where the key is the
            id of each specific unit conversion.
        """
        # Fetch the raw data from the repo
        raw_conversion_data = self._repository.read_all_global_unit_conversions()
        # Init a dict to hold the unit conversions
        conversions = {}
        # Cycle through the raw data
        for conversion_id, conversion_data in raw_conversion_data.items():
            # Create a new unit conversion
            conversions[conversion_id] = UnitConversion(
                id=conversion_id,
                from_unit_id=conversion_data["from_unit_id"], # type: ignore
                to_unit_id=conversion_data["to_unit_id"], # type: ignore
                from_unit_qty=conversion_data["from_unit_qty"],
                to_unit_qty=conversion_data["to_unit_qty"],
            )
        return conversions

    def read_ingredient_unit_conversions(
        self, ingredient_id: int
    ) -> dict[int, IngredientUnitConversion]:
        """Returns a list of unit conversions for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            dict[int, EntityUnitConversion]: A dictionary of unit conversions, where the key is the
            id of each specific unit conversion.
        """
        # Init a list to hold the custom units
        conversions = {}
        
        # Fetch the raw data from the repo
        raw_conversion_data = self._repository.read_ingredient_unit_conversions(
            ingredient_id
        )

        # Cycle through the raw data
        for conversion_id, conversion_data in raw_conversion_data.items():
            # Create a new custom unit
            conversions[conversion_id] = IngredientUnitConversion(
                entity_id=ingredient_id,
                id=conversion_id,
                from_unit_id=conversion_data["from_unit_id"],
                from_unit_qty=conversion_data["from_unit_qty"],
                to_unit_id=conversion_data["to_unit_id"],
                to_unit_qty=conversion_data["to_unit_qty"],
            )
        return conversions

    def update_ingredient_unit_conversion(self, unit_conversion: IngredientUnitConversion) -> None:
        """Updates the unit conversion in the database."""
        # Raise an exception if the id is None
        if unit_conversion.id is None:
            raise ValueError("ID must be set.")

        self._repository.update_ingredient_unit_conversion(
            ingredient_unit_id=unit_conversion.id,
            from_unit_id=unit_conversion.from_unit_id,
            from_unit_qty=unit_conversion.from_unit_qty,
            to_unit_id=unit_conversion.to_unit_id,
            to_unit_qty=unit_conversion.to_unit_qty,
        )

    def delete_ingredient_unit_conversions(self, ingredient_id: int) -> None:
        """Deletes all the unit conversions for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        """
        # Read all of the unit conversions
        unit_conversions = self._repository.read_ingredient_unit_conversions(ingredient_id)
        
        # Delete each unit conversion
        for id in unit_conversions.keys():
            self._repository.delete_ingredient_unit_conversion(id)

    def _cache_unit_id_name_map(self) -> None:
        """Re(generates) the cached unit ID to name map
        Emits the signal for the unit ID to name map change.

        Returns:
            Map: A map associating unit ID's with names.
        """
        # If the map is None, create it
        if self._unit_id_name_map is None:
            self._unit_id_name_map = Map[int, str](one_to_one=True)
        # Fetch all the units
        units = self._repository.read_all_global_units()
        # Clear the map
        self._unit_id_name_map.clear()
        # Add each unit to the map
        for unit_id, unit_data in units.items():
            self._unit_id_name_map.add_mapping(key=unit_id, value=unit_data["unit_name"])