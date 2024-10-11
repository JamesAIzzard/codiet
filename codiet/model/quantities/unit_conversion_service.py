from typing import TYPE_CHECKING, Collection, Callable, Deque, Dict, Set
from collections import deque

from codiet.utils import IUC

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion, Quantity


class ConversionUnavailableError(ValueError):
    def __init__(self, from_unit_name: str, to_unit_name: str):
        super().__init__(
            f"No conversion available from {from_unit_name} to {to_unit_name}"
        )


class UnitConversionService:
    def __init__(self):
        self._create_quantity: Callable[[str, float], "Quantity"]
        self._get_unit: Callable[[str], "Unit"]
        self._get_global_unit_conversions: Callable[
            [], dict[frozenset[str], "UnitConversion"]
        ]

        self._global_unit_conversion_cache: (
            dict[frozenset[str], "UnitConversion"] | None
        ) = None

    def initialise(
        self,
        create_quantity: Callable[[str, float], "Quantity"],
        get_unit: Callable[[str], "Unit"],
        get_global_unit_conversions: Callable[
            [], dict[frozenset[str], "UnitConversion"]
        ],
    ):
        self._create_quantity = create_quantity
        self._get_unit = get_unit
        self._get_global_unit_conversions = get_global_unit_conversions

    @property
    def global_unit_conversions(self) -> dict[frozenset[str], "UnitConversion"]:
        if self._global_unit_conversion_cache is None:
            self._global_unit_conversion_cache = self._get_global_unit_conversions()
        return self._global_unit_conversion_cache

    def get_available_unit_names(
        self,
        starting_unit_name: str | None = None,
        instance_unit_conversion_names: Collection[frozenset[str]] | None = None,
    ) -> IUC[str]:
        if starting_unit_name is None:
            starting_unit_name = "gram"

        combined_conversions = self.global_unit_conversions.copy()
        if instance_unit_conversion_names:
            for key in instance_unit_conversion_names:
                combined_conversions[key] = combined_conversions.get(key) # type: ignore

        # BFS to find all reachable units
        queue: Deque[str] = deque([starting_unit_name])
        visited: Set[str] = set()

        while queue:
            current_unit = queue.popleft()
            if current_unit in visited:
                continue
            visited.add(current_unit)

            for conversion_key in combined_conversions:
                if current_unit in conversion_key:
                    next_unit = next(iter(conversion_key - {current_unit}))
                    if next_unit not in visited:
                        queue.append(next_unit)

        return IUC(visited)

    def convert_quantity(
        self,
        quantity: "Quantity",
        to_unit_name: str,
        instance_unit_conversions: dict[frozenset[str], "UnitConversion"] | None = None,
    ) -> "Quantity":
        from_unit_name = quantity.unit.name

        # Combine global and instance unit conversions
        combined_conversions = self.global_unit_conversions.copy()
        if instance_unit_conversions:
            combined_conversions.update(instance_unit_conversions)

        # BFS to find the shortest path of conversions
        queue: Deque[tuple["Quantity", float]] = deque([(quantity, 1.0)])
        visited: Dict[str, float] = {from_unit_name: 1.0}

        while queue:
            current_quantity, cumulative_ratio = queue.popleft()
            current_unit_name = current_quantity.unit.name

            if current_unit_name == to_unit_name:
                return self._create_quantity(to_unit_name, quantity.value * cumulative_ratio)

            for conversion_key, conversion in combined_conversions.items():
                if current_unit_name in conversion_key:
                    next_unit_name = next(iter(conversion_key - {current_unit_name}))
                    if next_unit_name not in visited:
                        next_ratio = cumulative_ratio * self._get_conversion_ratio(conversion, current_unit_name, next_unit_name)
                        visited[next_unit_name] = next_ratio
                        next_quantity = self._create_quantity(next_unit_name, quantity.value * next_ratio)
                        queue.append((next_quantity, next_ratio))

        raise ConversionUnavailableError(from_unit_name, to_unit_name)

    def _get_conversion_ratio(self, conversion: "UnitConversion", from_unit_name: str, to_unit_name: str) -> float:
        quantities = conversion.quantities
        
        if quantities[from_unit_name].value is None or quantities[to_unit_name].value is None:
            raise ValueError("The conversion quantities are not fully defined.")
        
        return quantities[to_unit_name].value / quantities[from_unit_name].value