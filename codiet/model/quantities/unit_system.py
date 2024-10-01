from typing import TYPE_CHECKING, Collection
from collections import deque

from codiet.utils import MUC, IUC
from codiet.data import DatabaseService
from codiet.model.quantities import Quantity

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion

class UnitSystem():

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
        return IUC(self._get_available_units())

    @property
    def entity_unit_conversions(self) -> IUC['UnitConversion']:
        return IUC(self._entity_unit_conversions)

    def check_unit_available(self, unit: 'Unit') -> bool:
        return unit in self.available_units

    def add_entity_unit_conversion(self, unit_conversion: 'UnitConversion'):
        self._entity_unit_conversions.add(unit_conversion)
        self._update()

    def remove_entity_unit_conversion(self, entity_unit_conversion: 'UnitConversion'):
        self._entity_unit_conversions.remove(entity_unit_conversion)
        self._update()

    def can_convert_units(self, from_unit: 'Unit', to_unit: 'Unit') -> bool:
        try:
            self._find_conversion_path(from_unit, to_unit)
            return True
        except ValueError:
            return False

    def convert_quantity(self, quantity: Quantity, to_unit: 'Unit') -> Quantity:
        if quantity.unit == to_unit:
            return quantity

        conversion_factor = self._get_conversion_factor(quantity.unit, to_unit)
        converted_value = quantity.value * conversion_factor if quantity.value is not None else None
        return Quantity(unit=to_unit, value=converted_value)

    def _get_conversion_factor(self, from_unit: 'Unit', to_unit: 'Unit') -> float:
        path = self._find_conversion_path(from_unit, to_unit)
        factor = 1.0
        for u1, u2 in path:
            factor *= self._graph[u1][u2]
        return factor

    def _get_available_units(self, root_unit: 'Unit|None' = None) -> IUC['Unit']:
        if root_unit is None:
            root_unit = DatabaseService().read_unit("gram")

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
        self._path_cache.clear()

    def _find_conversion_path(self, from_unit: 'Unit', to_unit: 'Unit') -> list[tuple['Unit', 'Unit']]:
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
        self._graph.clear()
        self._path_cache.clear()
        global_unit_conversion_names = DatabaseService().read_all_global_unit_conversion_names()
        global_unit_conversions = []
        for conversion_name in global_unit_conversion_names:
            global_unit_conversions.append(DatabaseService().read_global_unit_conversion(conversion_name))
        all_conversions = global_unit_conversions + list(self._entity_unit_conversions)
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