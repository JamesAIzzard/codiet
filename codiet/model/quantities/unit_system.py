from typing import TYPE_CHECKING, Collection, Callable
from collections import deque

from codiet.utils import MUC, IUC
from codiet.model.quantities import Quantity

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion


class UnitSystem:
    def __init__(
        self,
        get_unit: Callable[[str], "Unit"],
        get_global_unit_conversions: Callable[[], Collection["UnitConversion"]],
        entity_unit_conversions: Collection["UnitConversion"] | None = None,
    ):
        self._get_unit = get_unit
        self._get_global_unit_conversions = get_global_unit_conversions
        self._entity_unit_conversions = (
            MUC(entity_unit_conversions) or MUC["UnitConversion"]()
        )
        self._conversion_graph: dict["Unit", dict["Unit", float]] = {}
        self._conversion_path_cache: dict[
            tuple["Unit", "Unit"], list[tuple["Unit", "Unit"]]
        ] = {}
        self._rebuild_conversion_graph()

    @property
    def available_units(self) -> IUC["Unit"]:
        return IUC(self._find_available_units())

    @property
    def entity_unit_conversions(self) -> IUC["UnitConversion"]:
        return IUC(self._entity_unit_conversions)

    def is_unit_available(
        self, unit_name: str | None = None, unit: "Unit|None" = None
    ) -> bool:
        if unit_name is not None:
            unit = self._get_unit(unit_name)
        return unit in self.available_units

    def add_entity_unit_conversion(self, unit_conversion: "UnitConversion"):
        self._entity_unit_conversions.add(unit_conversion)
        self._rebuild_conversion_graph()

    def remove_entity_unit_conversion(self, entity_unit_conversion: "UnitConversion"):
        self._entity_unit_conversions.remove(entity_unit_conversion)
        self._rebuild_conversion_graph()

    def can_convert_units(self, from_unit_name: str, to_unit_name: str) -> bool:
        from_unit = self._get_unit(from_unit_name)
        to_unit = self._get_unit(to_unit_name)
        return self._find_conversion_path(from_unit, to_unit) is not None

    def convert_quantity(self, quantity: Quantity, to_unit: "Unit|None"=None, to_unit_name:str|None=None) -> Quantity:
        if to_unit_name is not None:
            to_unit = self._get_unit(to_unit_name)
        if to_unit is None:
            raise TypeError("Target unit not specified.")
        
        if quantity.unit == to_unit:
            return quantity

        conversion_factor = self._calculate_conversion_factor(quantity.unit, to_unit)
        
        converted_value = (
            quantity.value * conversion_factor
        )

        return Quantity(unit=to_unit, value=converted_value)

    def _calculate_conversion_factor(self, from_unit: 'Unit', to_unit: 'Unit') -> float:
        path = self._find_conversion_path(from_unit, to_unit)
        if path is None:
            raise ConversionUnavailableError(from_unit.name, to_unit.name)

        factor = 1.0
        for u1, u2 in path:
            factor *= self._conversion_graph[u1][u2]
        return factor

    def _find_available_units(self, root_unit: "Unit | None" = None) -> IUC["Unit"]:
        if root_unit is None:
            root_unit = self._get_unit("gram")

        visited = set()
        queue = deque([root_unit])
        available_units = []

        while queue:
            unit = queue.popleft()
            if unit not in visited:
                visited.add(unit)
                available_units.append(unit)
                queue.extend(set(self._conversion_graph.get(unit, {}).keys()) - visited)

        return IUC(available_units)

    def _find_conversion_path(
        self, from_unit: "Unit", to_unit: "Unit"
    ) -> list[tuple["Unit", "Unit"]] | None:
        cache_key = (from_unit, to_unit)
        if cache_key in self._conversion_path_cache:
            return self._conversion_path_cache[cache_key]

        queue = deque([(from_unit, [])])
        visited = set()

        while queue:
            current_unit, path = queue.popleft()
            if current_unit == to_unit:
                self._conversion_path_cache[cache_key] = path
                return path

            if current_unit not in visited:
                visited.add(current_unit)
                for next_unit in self._conversion_graph.get(current_unit, {}):
                    if next_unit not in visited:
                        new_path = path + [(current_unit, next_unit)]
                        queue.append((next_unit, new_path))

        self._conversion_path_cache[cache_key] = None  # type: ignore
        return None

    def _rebuild_conversion_graph(self):
        self._conversion_graph.clear()
        self._conversion_path_cache.clear()
        all_conversions = list(self._get_global_unit_conversions()) + list(
            self._entity_unit_conversions
        )

        for conv in all_conversions:
            if conv.is_defined:
                self._add_conversion_to_graph(conv)

    def _add_conversion_to_graph(self, conversion: "UnitConversion"):
        from_unit, to_unit = (
            conversion.quantities[0].unit,
            conversion.quantities[1].unit,
        )
        ratio = (
            conversion.quantities[1].value / conversion.quantities[0].value
            if conversion.quantities[0].value
            else 0
        )

        self._conversion_graph.setdefault(from_unit, {})[to_unit] = ratio
        self._conversion_graph.setdefault(to_unit, {})[from_unit] = 1 / ratio

class ConversionUnavailableError(ValueError):
    def __init__(self, from_unit_name: str, to_unit_name: str):
        super().__init__(f"No conversion available from {from_unit_name} to {to_unit_name}")