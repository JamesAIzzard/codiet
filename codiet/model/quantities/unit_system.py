from typing import TYPE_CHECKING, Collection, Callable
from collections import deque

from codiet.utils import MUC, IUC
from codiet.model.quantities import Quantity

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion

class ConversionUnavailableError(ValueError):
    def __init__(self, from_unit_name: str, to_unit_name: str):
        super().__init__(f"No conversion available from {from_unit_name} to {to_unit_name}")

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
        
        converted_value = quantity.value * conversion_factor if quantity.value is not None else None

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
        
        return IUC(self._breadth_first_search(root_unit))

    def _breadth_first_search(self, start_unit: "Unit") -> list["Unit"]:
        visited = set()
        queue = deque([start_unit])
        available_units = []

        while queue:
            unit = queue.popleft()
            if unit not in visited:
                visited.add(unit)
                available_units.append(unit)
                self._enqueue_unvisited_neighbors(unit, visited, queue)

        return available_units

    def _enqueue_unvisited_neighbors(self, unit: "Unit", visited: set["Unit"], queue: deque["Unit"]):
        neighbors = set(self._conversion_graph.get(unit, {}).keys()) - visited
        queue.extend(neighbors)

    def _find_conversion_path(self, from_unit: "Unit", to_unit: "Unit") -> list[tuple["Unit", "Unit"]] | None:
        cache_key = (from_unit, to_unit)
        if cache_key in self._conversion_path_cache:
            return self._conversion_path_cache[cache_key]

        path = self._breadth_first_search_path(from_unit, to_unit)
        self._conversion_path_cache[cache_key] = path # type: ignore
        return path

    def _breadth_first_search_path(self, start: "Unit", end: "Unit") -> list[tuple["Unit", "Unit"]] | None:
        queue = deque([(start, [])])
        visited = set()

        while queue:
            current_unit, path = queue.popleft()
            if current_unit == end:
                return path

            if current_unit not in visited:
                visited.add(current_unit)
                self._enqueue_unvisited_paths(current_unit, path, visited, queue)

        return None

    def _enqueue_unvisited_paths(self, unit: "Unit", path: list[tuple["Unit", "Unit"]], 
                                 visited: set["Unit"], queue: deque[tuple["Unit", list[tuple["Unit", "Unit"]]]]):
        for next_unit in self._conversion_graph.get(unit, {}):
            if next_unit not in visited:
                new_path = path + [(unit, next_unit)]
                queue.append((next_unit, new_path))

    def _rebuild_conversion_graph(self):
        self._clear_graph_and_cache()
        all_conversions = self._get_all_conversions()
        self._add_conversions_to_graph(all_conversions)

    def _clear_graph_and_cache(self):
        self._conversion_graph.clear()
        self._conversion_path_cache.clear()

    def _get_all_conversions(self) -> list["UnitConversion"]:
        return list(self._get_global_unit_conversions()) + list(self._entity_unit_conversions)

    def _add_conversions_to_graph(self, conversions: list["UnitConversion"]):
        for conv in conversions:
            if conv.is_defined:
                self._add_conversion_to_graph(conv)

    def _add_conversion_to_graph(self, conversion: "UnitConversion"):
        from_unit, to_unit = conversion.quantities[0].unit, conversion.quantities[1].unit
        ratio = self._calculate_conversion_ratio(conversion)
        self._add_bidirectional_conversion(from_unit, to_unit, ratio)

    def _calculate_conversion_ratio(self, conversion: "UnitConversion") -> float:
        return (conversion.quantities[1].value / conversion.quantities[0].value
                if conversion.quantities[0].value else 0)

    def _add_bidirectional_conversion(self, from_unit: "Unit", to_unit: "Unit", ratio: float):
        self._conversion_graph.setdefault(from_unit, {})[to_unit] = ratio
        self._conversion_graph.setdefault(to_unit, {})[from_unit] = 1 / ratio