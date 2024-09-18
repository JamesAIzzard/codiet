"""Defines the service for interacting with the unit database."""
from typing import Collection, TYPE_CHECKING

from PyQt6.QtCore import pyqtSignal

from codiet.utils import Map, IUC
from codiet.db.database_service.database_service_base import DatabaseServiceBase
from codiet.model.quantities import Unit, UnitConversion

if TYPE_CHECKING:
    from codiet.model.ingredients import Ingredient

class UnitDBService(DatabaseServiceBase):
    """Service for interacting with the unit database."""

    unitsChanged = pyqtSignal()
    globalUnitConversionsChanged = pyqtSignal()
    ingredientUnitConversionChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        """Initialise the unit database service."""
        super().__init__(*args, **kwargs)

        # Cache the unit id-name map
        self._unit_id_name_map: Map[int, str]|None = None

        # Create the caches
        self._units: IUC[Unit]|None = None
        self._mass_units: IUC[Unit]|None = None
        self._volume_units: IUC[Unit]|None = None
        self._grouping_units: IUC[Unit]|None = None
        self._global_unit_conversions: IUC[UnitConversion]|None = None

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
    def units(self) -> IUC[Unit]:
        """Returns all the units."""
        if self._units is None:
            self._units = self.read_all_units()
        return self._units
    
    @property
    def gram(self) -> Unit:
        """Returns the gram unit."""
        if self._gram is None:
            self._gram = self.get_unit_by_name("gram")
        return self._gram

    @property
    def mass_units(self) -> IUC[Unit]:
        """Returns all the mass units."""
        if self._mass_units is None:
            self._mass_units = IUC([unit for unit in self.units if unit._type == "mass"])
        return self._mass_units
    
    @property
    def volume_units(self) -> IUC[Unit]:
        """Returns all the volume units."""
        if self._volume_units is None:
            self._volume_units = IUC([unit for unit in self.units if unit._type == "volume"])
        return self._volume_units
    
    @property
    def grouping_units(self) -> IUC[Unit]:
        """Returns all the grouping units."""
        if self._grouping_units is None:
            self._grouping_units = IUC([unit for unit in self.units if unit._type == "grouping"])
        return self._grouping_units
    
    @property
    def global_unit_conversions(self) -> IUC[UnitConversion]:
        """Returns all the global unit conversions."""
        if self._global_unit_conversions is None:
            self._global_unit_conversions = self.read_all_global_unit_conversions()
        return self._global_unit_conversions

    def get_unit_by_name(self, unit_name: str) -> Unit:
        """Retrieves a single unit by its name."""
        for unit in self.units:
            if unit._unit_name == unit_name:
                return unit
        raise KeyError(f"Unit with name {unit_name} not found.")

    def get_units_by_name(self, unit_names: Collection[str]) -> IUC[Unit]:
        """Retrieves multiple units by their names."""
        return IUC(self.get_unit_by_name(unit_name) for unit_name in unit_names)

    def get_unit_by_id(self, unit_id: int) -> Unit:
        """Retrieves a single unit by its id."""
        for unit in self.units:
            if unit.id == unit_id:
                return unit
        raise KeyError(f"Unit with id {unit_id} not found.")

    def get_units_by_id(self, unit_ids: Collection[int]) -> IUC[Unit]:
        """Retrieves multiple units by their ids."""
        units = []
        for unit_id in unit_ids:
            units.append(self.get_unit_by_id(unit_id))
        return IUC(units)

    def get_global_unit_conversion_by_units(self, from_unit: Unit, to_unit: Unit) -> UnitConversion:
        """Retrieves a single unit conversion by its units."""
        for unit_conversion in self.global_unit_conversions:
            if unit_conversion.from_unit == from_unit and unit_conversion.to_unit == to_unit:
                return unit_conversion
            elif unit_conversion.from_unit == to_unit and unit_conversion.to_unit == from_unit:
                return unit_conversion
        raise KeyError(f"Unit conversion from {from_unit} to {to_unit} not found.")

    def get_global_unit_conversions_by_units(self, unit_pairs: Collection[tuple[Unit, Unit]]) -> IUC[UnitConversion]:
        """Retrieves multiple unit conversions by their units."""
        return IUC(self.get_global_unit_conversion_by_units(from_unit, to_unit) 
                     for from_unit, to_unit in unit_pairs)

    def get_global_unit_conversion_by_id(self, id: int) -> UnitConversion:
        """Retrieves a single unit conversion by its id."""
        for unit_conversion in self.global_unit_conversions:
            if unit_conversion.id == id:
                return unit_conversion
        raise KeyError(f"Unit conversion with id {id} not found.")

    def get_global_unit_conversions_by_id(self, ids: Collection[int]) -> IUC[UnitConversion]:
        """Retrieves multiple unit conversions by their ids."""
        return IUC(self.get_global_unit_conversion_by_id(id) for id in ids)
    
    def create_unit(self, unit: Unit, _signal:bool=True) -> Unit:
        """Insert a unit into the database."""
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

        if _signal:
            # Recache the units
            self._reset_units_cache()
            # Emit the signal
            self.unitsChanged.emit()

        return unit

    def create_units(self, units: Collection[Unit]) -> IUC[Unit]:
        """Insert a set of units into the database."""
        # Init return dict
        persisted_units = []

        # For each unit
        for unit in units:

            self.create_unit(unit, _signal=False)    

            persisted_units.append(unit)

            # Recache the units
            self._reset_units_cache()

            # Emit the signal
            self.unitsChanged.emit()

        return IUC(persisted_units)

    def create_global_unit_conversion(self, unit_conversion: UnitConversion, _signal:bool=True) -> UnitConversion:
        """Insert a global unit conversion into the database."""
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

        if _signal:
            # Recache the global unit conversions
            self._reset_global_unit_conversions_cache()

            # Emit the signal
            self.globalUnitConversionsChanged.emit()

        return unit_conversion

    def create_global_unit_conversions(self, unit_conversions: Collection[UnitConversion]) -> IUC[UnitConversion]:
        """Insert a set of global unit conversions into the database."""
        # Init return dict
        persisted_unit_conversions = []

        # For each unit conversion
        for unit_conversion in unit_conversions:
                
                conversion = self.create_global_unit_conversion(unit_conversion, _signal=False)
    
                persisted_unit_conversions.append(conversion)

        return IUC(persisted_unit_conversions)

    def create_ingredient_unit_conversion(self, ingredient_unit_conversion: UnitConversion) -> UnitConversion:
        """Insert a set of ingredient unit conversions into the database."""

        # Confirm that both from and to units are persisted
        assert ingredient_unit_conversion.from_unit.id is not None
        assert ingredient_unit_conversion.to_unit.id is not None
        # Confirm the unit is peristed
        assert ingredient_unit_conversion.ingredient.id is not None

        # Insert the ingredient unit conversion into the database
        ingredient_unit_conversion_id = self._repository.units.create_ingredient_unit_conversion(
            from_unit_id=ingredient_unit_conversion.from_unit.id,
            to_unit_id=ingredient_unit_conversion.to_unit.id,
            from_unit_qty=ingredient_unit_conversion.from_unit_qty,
            to_unit_qty=ingredient_unit_conversion.to_unit_qty,
            ingredient_id=ingredient_unit_conversion.ingredient.id,
        )

        # Update the id
        ingredient_unit_conversion.id = ingredient_unit_conversion_id

        return ingredient_unit_conversion

    def create_ingredient_unit_conversions(self, ingredient_unit_conversions: Collection[UnitConversion]) -> IUC[UnitConversion]:
        """Insert a set of ingredient unit conversions into the database."""
        # Init return dict
        persisted_ingredient_unit_conversions = []

        # For each unit conversion
        for ingredient_unit_conversion in ingredient_unit_conversions:

            conversion = self.create_ingredient_unit_conversion(ingredient_unit_conversion)

            persisted_ingredient_unit_conversions.append(conversion)

        return IUC(persisted_ingredient_unit_conversions)

    def read_all_units(self) -> IUC[Unit]:
        """Returns all the units."""
        units = []
        
        # Read the unit bases
        unit_bases = self._repository.units.read_all_unit_bases()
        
        for unit_base in unit_bases:
            # Read the unit aliases for each unit base
            aliases = self._repository.units.read_unit_aliases(unit_base['id'])
            
            # Construct the Unit object
            unit = Unit(
                name=unit_base['unit_name'],
                singular_abbreviation=unit_base['single_display_name'],
                plural_abbreviation=unit_base['plural_display_name'],
                type=unit_base['unit_type'],
                aliases=set(aliases.values()),
                id=unit_base['id']
            )
            
            units.append(unit)
        
        # Return the set as a frozenset
        return IUC(units)

    def read_all_global_unit_conversions(self) -> IUC[UnitConversion]:
        """Returns all the global unit conversions."""
        unit_conversions = []
        
        # Read the global unit conversions
        global_unit_conversions_data = self._repository.units.read_all_global_unit_conversions()
        
        for row in global_unit_conversions_data:
            # Construct the UnitConversion object
            unit_conversion = UnitConversion(
                from_unit=self.get_unit_by_id(row['from_unit_id']),
                to_unit=self.get_unit_by_id(row['to_unit_id']),
                from_unit_qty=row['from_unit_qty'],
                to_unit_qty=row['to_unit_qty'],
                id=row['id']
            )
            
            unit_conversions.append(unit_conversion)
        
        # Return the set as a frozenset
        return IUC(unit_conversions)

    def read_ingredient_unit_conversions(self, ingredient: 'Ingredient') -> IUC[UnitConversion]:
        """Returns all the ingredient unit conversions for an ingredient."""
        ingredient_unit_conversions = []

        # Assert the ingredient id is set
        assert ingredient.id is not None
        
        # Read the ingredient unit conversions
        ingredient_unit_conversions_data = self._repository.units.read_ingredient_unit_conversions(ingredient.id)
        
        for uc_id, uc_data in ingredient_unit_conversions_data.items():
            # Construct the IngredientUnitConversion object
            unit_conversion = UnitConversion(
                from_unit=self.get_unit_by_id(uc_data['from_unit_id']),
                to_unit=self.get_unit_by_id(uc_data['to_unit_id']),
                from_unit_qty=uc_data['from_unit_qty'],
                to_unit_qty=uc_data['to_unit_qty'],
                ingredient=ingredient,
                id=uc_id
            )
            
            ingredient_unit_conversions.append(unit_conversion)
        
        return IUC(ingredient_unit_conversions)

    def update_unit(self, unit: Unit, _signal:bool=True) -> None:
        """Update a unit in the database."""
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

        if _signal:
            # Recache the units
            self._reset_units_cache()
            # Emit the signal
            self.unitsChanged.emit()

    def update_units(self, units: Collection[Unit]) -> None:
        """Update a set of units in the database."""
        # For each unit
        for unit in units:

            self.update_unit(unit, _signal=False)

        # Recache the units and signal the change
        self._reset_units_cache()
        self.unitsChanged.emit()

    def update_global_unit_conversion(self, unit_conversion: UnitConversion, _signal:bool=True) -> None:
        """Update a global unit conversion in the database."""
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

        if _signal:
            # Recache the global unit conversions
            self._reset_global_unit_conversions_cache()

            # Emit the signal
            self.globalUnitConversionsChanged

    def update_global_unit_conversions(self, unit_conversions: Collection[UnitConversion]) -> None:
        """Update a collection of global unit conversions in the database."""
        # For each unit conversion
        for unit_conversion in unit_conversions:
            self.update_global_unit_conversion(unit_conversion, _signal=False)

        # Recache the global unit conversions and signal the change
        self._reset_global_unit_conversions_cache()
        self.globalUnitConversionsChanged.emit()

    def update_ingredient_unit_conversion(self, ingredient_unit_conversion: UnitConversion, _signal:bool=True) -> None:
        """Update an ingredient unit conversion in the database."""
        # Check the unit conversion id is set
        if ingredient_unit_conversion.id is None:
            raise ValueError("ID must be set for update.")
        
        # Confirm that both from and to units are persisted
        assert ingredient_unit_conversion.from_unit.id is not None
        assert ingredient_unit_conversion.to_unit.id is not None
        # Confirm the unit is peristed
        assert ingredient_unit_conversion.ingredient.id is not None

        # Update the unit conversion
        self._repository.units.update_ingredient_unit_conversion(
            unit_conversion_id=ingredient_unit_conversion.id,
            from_unit_id=ingredient_unit_conversion.from_unit.id,
            to_unit_id=ingredient_unit_conversion.to_unit.id,
            from_unit_qty=ingredient_unit_conversion.from_unit_qty,
            to_unit_qty=ingredient_unit_conversion.to_unit_qty,
        )

        if _signal:
            self.ingredientUnitConversionChanged.emit()

    def update_ingredient_unit_conversions(self, ingredient_unit_conversions: Collection[UnitConversion]) -> None:
        """Update a set of ingredient unit conversions in the database."""
        for ingredient_unit_conversion in ingredient_unit_conversions:
            self.update_ingredient_unit_conversion(ingredient_unit_conversion, _signal=False)
    
        self.ingredientUnitConversionChanged.emit()

    def delete_unit(self, unit: Unit, _signal:bool=True) -> None:
        """Delete a unit from the database."""
        # Check the unit id is set
        if unit.id is None:
            raise ValueError("ID must be set for deletion.")

        # Delete the unit base
        self._repository.units.delete_unit_base(unit.id)

        # Delete the aliases for the unit
        existing_aliases = self._repository.units.read_unit_aliases(unit.id)
        for alias_id in existing_aliases.keys():
            self._repository.units.delete_unit_alias(alias_id)

        if _signal:
            # Recache the units
            self._reset_units_cache()
            # Emit the signal
            self.unitsChanged.emit()

    def delete_units(self, units: Collection[Unit]) -> None:
        """Delete a set of units from the database."""
        # For each unit
        for unit in units:
            self.delete_unit(unit, _signal=False)

        self._reset_units_cache()
        self.unitsChanged.emit()

    def delete_global_unit_conversion(self, unit_conversion: UnitConversion, _signal:bool=True) -> None:
        """Delete a global unit conversion from the database."""
        # Check the unit conversion id is set
        if unit_conversion.id is None:
            raise ValueError("ID must be set for deletion.")
        
        # Delete the unit conversion
        self._repository.units.delete_global_unit_conversion(unit_conversion.id)

        if _signal:
            self._reset_global_unit_conversions_cache()
            self.globalUnitConversionsChanged.emit()

    def delete_global_unit_conversions(self, unit_conversions: Collection[UnitConversion]) -> None:
        """Delete a collection of global unit conversions from the database."""
        # For each unit conversion
        for unit_conversion in unit_conversions:
            self.delete_global_unit_conversion(unit_conversion, _signal=False)

        # Recache the global unit conversions and signal the change
        self._reset_global_unit_conversions_cache()
        self.globalUnitConversionsChanged.emit()

    def delete_ingredient_unit_conversion(self, ingredient_unit_conversion: UnitConversion, _signal:bool=True) -> None:
        """Delete an ingredient unit conversion from the database."""
        # Check the unit conversion id is set
        if ingredient_unit_conversion.id is None:
            raise ValueError("ID must be set for deletion.")
        
        # Delete the unit conversion
        self._repository.units.delete_ingredient_unit_conversion(ingredient_unit_conversion.id)

        if _signal:
            self.ingredientUnitConversionChanged.emit()

    def delete_ingredient_unit_conversions(self, ingredient_unit_conversions: Collection[UnitConversion]) -> None:
        """Delete a set of ingredient unit conversions from the database."""
        # For each unit conversion
        for ingredient_unit_conversion in ingredient_unit_conversions:
            self.delete_ingredient_unit_conversion(ingredient_unit_conversion, _signal=False)

        self.ingredientUnitConversionChanged.emit()

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