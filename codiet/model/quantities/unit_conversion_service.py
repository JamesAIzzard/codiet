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
                combined_conversions[key] = combined_conversions.get(key)

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
        instance_unit_conversons: dict[frozenset[str], "UnitConversion"] | None = None,
    ) -> "Quantity":
        from_unit_name = quantity.unit.name

        # Combine global and instance unit conversions
        combined_conversions = self.global_unit_conversions.copy()
        if instance_unit_conversons:
            for key, conversion in instance_unit_conversons.items():
                combined_conversions[key] = conversion

        # BFS to find the shortest path of conversions
        queue: Deque["Quantity"] = deque([quantity])
        paths: Dict[str, "Quantity"] = {from_unit_name: quantity}

        while queue:
            current_quantity = queue.popleft()
            current_unit_name = current_quantity.unit.name

            if current_unit_name == to_unit_name:
                return current_quantity

            for conversion_key, conversion in combined_conversions.items():
                if current_unit_name in conversion_key:
                    next_unit_name = next(iter(conversion_key - {current_unit_name}))
                    if next_unit_name not in paths:
                        next_quantity = conversion.convert_from(current_quantity)
                        paths[next_unit_name] = next_quantity
                        queue.append(next_quantity)

        raise ConversionUnavailableError(from_unit_name, to_unit_name)
