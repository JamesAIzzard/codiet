from PyQt6.QtCore import pyqtSignal

from codiet.db.database_service.database_service_base import DatabaseServiceBase
from codiet.utils.map import Map
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion

class UnitDBService(DatabaseServiceBase):
    """Service for interacting with the unit database."""

    unitsUpdated = pyqtSignal()
    unitConversionsUpdated = pyqtSignal()

    def __init__(self, *args, **kwargs):
        """Initialise the unit database service."""
        super().__init__(*args, **kwargs)

        # Cache the unit id-name map
        self._unit_id_name_map: Map[int, str]|None = None

        # Cache a full list of global units, and global mass units
        self._units: frozenset[Unit]|None = None
        self._mass_units: frozenset[Unit]|None = None
        self._volume_units: frozenset[Unit]|None = None
        self._grouping_units: frozenset[Unit]|None = None

        # Cache a full list of global unit conversions
        self._global_unit_conversions: frozenset[UnitConversion]|None = None

        # Cache the gram id. This the base unit, and used all over.
        self._gram: Unit|None = None

    @property
    def unit_id_name_map(self) -> Map[int, str]:
        """Return the unit ID to name map."""
        if self._unit_id_name_map is None:
            self._unit_id_name_map = Map[int, str]()
            for unit in self.units:
                assert unit.id is not None
                self._unit_id_name_map[unit.id] = unit._unit_name
        return self._unit_id_name_map

    @property
    def units(self) -> frozenset[Unit]:
        """Returns all the units."""
        if self._units is None:
            self._units = self.read_all_units()
        return self._units
    
    @property
    def mass_units(self) -> frozenset[Unit]:
        """Returns all the mass units."""
        if self._mass_units is None:
            self._mass_units = frozenset([unit for unit in self.units if unit._type == "mass"])
        return self._mass_units
    
    @property
    def volume_units(self) -> frozenset[Unit]:
        """Returns all the volume units."""
        if self._volume_units is None:
            self._volume_units = frozenset([unit for unit in self.units if unit._type == "volume"])
        return self._volume_units
    
    @property
    def grouping_units(self) -> frozenset[Unit]:
        """Returns all the grouping units."""
        if self._grouping_units is None:
            self._grouping_units = frozenset([unit for unit in self.units if unit._type == "grouping"])
        return self._grouping_units
    
    def get_unit_by_name(self, unit_name:str) -> Unit:
        """Retrieves a unit by its name."""
        for unit in self.units:
            if unit._unit_name == unit_name:
                return unit
        raise KeyError(f"Unit with name {unit_name} not found.")

    def create_units(self, units: set[Unit]) -> frozenset[Unit]:
        """Insert a set of units into the database."""
        # Init return dict
        persisted_units = []

        # For each unit
        for unit in units:

            # Insert the unit name into the database
            unit_id = self._repository.units.create_unit_base(
                unit_name=unit._unit_name,
                unit_type=unit._type,
                single_display_name=unit._single_display_name,
                plural_display_name=unit._plural_display_name,
            )

            # Update the id
            unit.id = unit_id

            # Insert the aliases for the unit
            for alias in unit._aliases:
                self._repository.units.create_unit_alias(
                    alias=alias,
                    primary_unit_id=unit_id,
                )    

            persisted_units.append(unit)

            # Recache the units
            self._reset_units_cache()

            # Emit the signal
            self.unitsUpdated.emit()

        return frozenset(persisted_units)

    def read_all_units(self) -> frozenset[Unit]:
        """Returns all the units."""
        units = set()
        
        # Read the unit bases
        unit_bases = self._repository.units.read_all_unit_bases()
        
        for unit_base in unit_bases:
            # Read the unit aliases for each unit base
            aliases = self._repository.units.read_unit_aliases(unit_base['id'])
            
            # Construct the Unit object
            unit = Unit(
                unit_name=unit_base['unit_name'],
                single_display_name=unit_base['single_display_name'],
                plural_display_name=unit_base['plural_display_name'],
                type=unit_base['unit_type'],
                aliases=set(aliases.values()),
                id=unit_base['id']
            )
            
            units.add(unit)
        
        # Return the set as a frozenset
        return frozenset(units)

    def update_units(self, units: set[Unit]) -> None:
        """Update a set of units in the database."""
        # For each unit
        for unit in units:

            # Check the unit id is set
            if unit.id is None:
                raise ValueError("ID must be set for update.")

            # Update the unit base
            self._repository.units.update_unit_base(
                unit_id=unit.id,
                unit_name=unit._unit_name,
                single_display_name=unit._single_display_name,
                plural_display_name=unit._plural_display_name,
                unit_type=unit._type,
            )

            # Update the aliases for the unit
            existing_aliases = self._repository.units.read_unit_aliases(unit.id)
            for alias in unit._aliases:
                if alias not in existing_aliases.values():
                    self._repository.units.create_unit_alias(
                        alias=alias,
                        primary_unit_id=unit.id,
                    )
            for alias_id, alias in existing_aliases.items():
                if alias not in unit._aliases:
                    self._repository.units.delete_unit_alias(alias_id)

            # Recache the units
            self._reset_units_cache()

            # Emit the signal
            self.unitsUpdated.emit()

    def delete_units(self, units: set[Unit]) -> None:
        """Delete a set of units from the database."""
        # For each unit
        for unit in units:

            # Check the unit id is set
            if unit.id is None:
                raise ValueError("ID must be set for deletion.")

            # Delete the unit base
            self._repository.units.delete_unit_base(unit.id)

            # Delete the aliases for the unit
            existing_aliases = self._repository.units.read_unit_aliases(unit.id)
            for alias_id in existing_aliases.keys():
                self._repository.units.delete_unit_alias(alias_id)

            # Recache the units
            self._reset_units_cache()

            # Emit the signal
            self.unitsUpdated.emit()

    def _reset_units_cache(self) -> None:
        """Rebuilds the cached units."""
        # Reset them all to None
        self._unit_id_name_map = None
        self._units = None
        self._mass_units = None
        self._volume_units = None
        self._grouping_units = None

        self._units = self.read_all_units()