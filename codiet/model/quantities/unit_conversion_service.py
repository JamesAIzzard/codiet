from typing import TYPE_CHECKING, Collection, Callable, Deque, Mapping
from collections import deque

from codiet.utils import IUC
from codiet.exceptions.quantities import ConversionUnavailableError

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion, Quantity


class UnitConversionService:
    def __init__(self):
        self._create_quantity: Callable[[str, float], "Quantity"]
        self._get_unit: Callable[[str], "Unit"]
        self._get_all_global_unit_conversions: Callable[
            [], Mapping[frozenset[str], "UnitConversion"]
        ]

    def initialise(
        self,
        create_quantity: Callable[[str, float], "Quantity"],
        get_unit: Callable[[str], "Unit"],
        get_all_global_unit_conversions: Callable[
            [], Mapping[frozenset[str], "UnitConversion"]
        ],
    ):
        self._create_quantity = create_quantity
        self._get_unit = get_unit
        self._get_all_global_unit_conversions = get_all_global_unit_conversions

    def get_available_unit_names(
        self,
        starting_unit_name: str | None = None,
        instance_unit_conversion_names: Collection[frozenset[str]] | None = None,
    ) -> IUC[str]:
        if starting_unit_name is None:
            starting_unit_name = "gram"

        combined_conversions = self._get_all_global_unit_conversions()
        if instance_unit_conversion_names:
            for key in instance_unit_conversion_names:
                combined_conversions[key] = combined_conversions.get(key)  # type: ignore

        # BFS to find all reachable units
        queue: Deque[str] = deque([starting_unit_name])
        visited: set[str] = set()

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
        instance_unit_conversions: (
            Mapping[frozenset[str], "UnitConversion"] | None
        ) = None,
    ) -> "Quantity":
        from_unit_name = quantity.unit.name

        # Combine global and instance unit conversions
        combined_conversions = dict(self._get_all_global_unit_conversions())
        if instance_unit_conversions:
            combined_conversions.update(instance_unit_conversions)

        # BFS to find the shortest path of conversions
        queue: Deque[tuple["Quantity", float]] = deque([(quantity, 1.0)])
        visited: dict[str, float] = {from_unit_name: 1.0}

        while queue:
            current_quantity, cumulative_ratio = queue.popleft()
            current_unit_name = current_quantity.unit.name

            if current_unit_name == to_unit_name:
                return self._create_quantity(
                    to_unit_name, quantity.value * cumulative_ratio
                )

            for conversion_key, conversion in combined_conversions.items():
                if current_unit_name in conversion_key:
                    next_unit_name = next(iter(conversion_key - {current_unit_name}))
                    if next_unit_name not in visited:
                        if conversion._from_quantity.unit.name == current_unit_name:
                            ratio = conversion._forwards_ratio
                        else:
                            ratio = 1 / conversion._forwards_ratio
                        next_ratio = cumulative_ratio * ratio
                        visited[next_unit_name] = next_ratio
                        next_quantity = self._create_quantity(
                            next_unit_name, quantity.value * next_ratio
                        )
                        queue.append((next_quantity, next_ratio))

        raise ConversionUnavailableError(from_unit_name, to_unit_name)

    def convert_to_grams(
        self,
        quantity: "Quantity",
        instance_unit_conversions: Mapping[frozenset[str], "UnitConversion"]|None=None,
    ) -> "Quantity":
        return self.convert_quantity(
            quantity=quantity,
            to_unit_name="gram",
            instance_unit_conversions=instance_unit_conversions,
        )
