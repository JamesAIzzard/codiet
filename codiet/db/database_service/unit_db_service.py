from typing import overload

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

        # Create the caches
        self._units: frozenset[Unit]|None = None
        self._mass_units: frozenset[Unit]|None = None
        self._volume_units: frozenset[Unit]|None = None
        self._grouping_units: frozenset[Unit]|None = None
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
    def gram(self) -> Unit:
        """Returns the gram unit."""
        if self._gram is None:
            self._gram = self.get_units_by_name("gram")
        return self._gram

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
    
    @property
    def global_unit_conversions(self) -> frozenset[UnitConversion]:
        """Returns all the global unit conversions."""
        if self._global_unit_conversions is None:
            self._global_unit_conversions = self.read_all_global_unit_conversions()
        return self._global_unit_conversions

    @overload
    def get_units_by_name(self, unit_names: str) -> Unit:
        ...
    @overload
    def get_units_by_name(self, unit_names: tuple[str, ...]) -> tuple[Unit, ...]:
        ...
    def get_units_by_name(self, unit_names: str|tuple[str, ...]) -> Unit|tuple[Unit, ...]:
        """Retrieves a unit by its name."""
        # Single use case
        if isinstance(unit_names, str):
            return self._get_unit_by_name(unit_names)
        # Multiple use case
        else:
            return tuple(self._get_unit_by_name(unit_name) for unit_name in unit_names)

    @overload
    def get_units_by_id(self, unit_id:int) -> Unit:
        ...
    @overload
    def get_units_by_id(self, unit_id:tuple[int, ...]) -> tuple[Unit, ...]:
        ...
    def get_units_by_id(self, unit_id:int|tuple[int, ...]) -> Unit|tuple[Unit, ...]:
        """Retrieves units by their id."""
        # Single use case
        if isinstance(unit_id, int):
            for unit in self.units:
                if unit.id == unit_id:
                    return unit
            raise KeyError(f"Unit with id {unit_id} not found.")
        # Multiple use case
        else:
            return tuple([unit for unit_id in unit_id for unit in self.units if unit.id == unit_id])

    @overload
    def get_global_unit_conversions_by_units(self, units: tuple[Unit, Unit]) -> UnitConversion:
        ...
    @overload
    def get_global_unit_conversions_by_units(self, units: tuple[tuple[Unit, Unit], ...]) -> tuple[UnitConversion, ...]:
        ...
    def get_global_unit_conversions_by_units(self, units: tuple[Unit, Unit]|tuple[tuple[Unit, Unit], ...]) -> UnitConversion|tuple[UnitConversion, ...]:
        """Retrieves unit conversions by their units."""
        # Single use case
        if isinstance(units[0], Unit):
            for unit_conversion in self.global_unit_conversions:
                if unit_conversion.from_unit == units[0] and unit_conversion.to_unit == units[1]:
                    return unit_conversion
            raise KeyError(f"Unit conversion with units {units} not found.")
        # Multiple use case
        else:
            return tuple(unit_conversion for unit in units for unit_conversion in self.global_unit_conversions if (unit_conversion.from_unit, unit_conversion.to_unit) == unit)

    @overload
    def get_global_unit_conversions_by_id(self, id:int) -> UnitConversion:
        ...
    @overload
    def get_global_unit_conversions_by_id(self, id:tuple[int, ...]) -> tuple[UnitConversion, ...]:
        ...
    def get_global_unit_conversions_by_id(self, id:int|tuple[int, ...]) -> UnitConversion|tuple[UnitConversion, ...]:
        """Retrieves unit conversions by their id."""
        # Single use case
        if isinstance(id, int):
            for unit_conversion in self.global_unit_conversions:
                if unit_conversion.id == id:
                    return unit_conversion
            raise KeyError(f"Unit conversion with id {id} not found.")
        # Multiple use case
        else:
            unit_conversions = []
            for unit_conversion in self.global_unit_conversions:
                if unit_conversion.id in id:
                    unit_conversions.append(unit_conversion)
            return tuple(unit_conversions)

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

    def create_global_unit_conversions(self, unit_conversions: set[UnitConversion]) -> frozenset[UnitConversion]:
        """Insert a set of global unit conversions into the database."""
        # Init return dict
        persisted_unit_conversions = []

        # For each unit conversion
        for unit_conversion in unit_conversions:

            # Confirm that both from and to units are persisted
            assert unit_conversion.from_unit.id is not None
            assert unit_conversion.to_unit.id is not None

            # Insert the unit conversion into the database
            unit_conversion_id = self._repository.units.create_global_unit_conversion(
                from_unit_id=unit_conversion.from_unit.id,
                to_unit_id=unit_conversion.to_unit.id,
                from_unit_qty=unit_conversion.from_unit_qty,
                to_unit_qty=unit_conversion.to_unit_qty,
            )

            # Update the id
            unit_conversion.id = unit_conversion_id

            persisted_unit_conversions.append(unit_conversion)

            # Recache the global unit conversions
            self._reset_global_unit_conversions_cache()

            # Emit the signal
            self.unitConversionsUpdated.emit()

        return frozenset(persisted_unit_conversions)

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

    def read_all_global_unit_conversions(self) -> frozenset[UnitConversion]:
        """Returns all the global unit conversions."""
        unit_conversions = set()
        
        # Read the global unit conversions
        global_unit_conversions = self._repository.units.read_all_global_unit_conversions()
        
        for global_unit_conversion in global_unit_conversions:
            # Construct the UnitConversion object
            unit_conversion = UnitConversion(
                from_unit=self.get_units_by_id(global_unit_conversion['from_unit_id']),
                to_unit=self.get_units_by_id(global_unit_conversion['to_unit_id']),
                from_unit_qty=global_unit_conversion['from_unit_qty'],
                to_unit_qty=global_unit_conversion['to_unit_qty'],
                id=global_unit_conversion['id']
            )
            
            unit_conversions.add(unit_conversion)
        
        # Return the set as a frozenset
        return frozenset(unit_conversions)

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

    def update_global_unit_conversions(self, unit_conversions: set[UnitConversion]) -> None:
        """Update a set of global unit conversions in the database."""
        # For each unit conversion
        for unit_conversion in unit_conversions:

            # Check the unit conversion id is set
            if unit_conversion.id is None:
                raise ValueError("ID must be set for update.")
            
            # Confirm that both from and to units are persisted
            assert unit_conversion.from_unit.id is not None
            assert unit_conversion.to_unit.id is not None

            # Update the unit conversion
            self._repository.units.update_global_unit_conversion(
                unit_conversion_id=unit_conversion.id,
                from_unit_id=unit_conversion.from_unit.id,
                to_unit_id=unit_conversion.to_unit.id,
                from_unit_qty=unit_conversion.from_unit_qty,
                to_unit_qty=unit_conversion.to_unit_qty,
            )

            # Recache the global unit conversions
            self._reset_global_unit_conversions_cache()

            # Emit the signal
            self.unitConversionsUpdated.emit()

    def delete_units(self, units: Unit|set[Unit]) -> None:
        """Delete a set of units from the database."""
        # Convert to set if provided as a single Unit
        if not isinstance(units, set):
            units = set([units])

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

    def delete_global_unit_conversions(self, unit_conversions: set[UnitConversion]) -> None:
        """Delete a set of global unit conversions from the database."""
        # For each unit conversion
        for unit_conversion in unit_conversions:

            # Check the unit conversion id is set
            if unit_conversion.id is None:
                raise ValueError("ID must be set for deletion.")
            
            # Delete the unit conversion
            self._repository.units.delete_global_unit_conversion(unit_conversion.id)

            # Recache the global unit conversions
            self._reset_global_unit_conversions_cache()

            # Emit the signal
            self.unitConversionsUpdated.emit()

    def _get_unit_by_name(self, unit_name:str) -> Unit:
        """Retrieves a unit by its name."""    
        for unit in self.units:
            if unit._unit_name == unit_name:
                return unit
        raise KeyError(f"Unit with name {unit_name} not found.")

    def _reset_units_cache(self) -> None:
        """Rebuilds the cached units."""
        # Reset them all to None
        self._unit_id_name_map = None
        self._units = None
        self._mass_units = None
        self._volume_units = None
        self._grouping_units = None

    def _reset_global_unit_conversions_cache(self) -> None:
        """Rebuilds the cached global unit conversions."""
        self._global_unit_conversions = None