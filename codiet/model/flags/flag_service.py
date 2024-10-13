from typing import TYPE_CHECKING, Callable, Optional, Collection

from codiet.utils.unique_dict import FrozenUniqueDict as FUD

if TYPE_CHECKING:
    from codiet.model.flags import Flag, FlagDefinition


class FlagService:
    _create_flag: Callable[[str, Optional[bool]], "Flag"]
    _get_flag_definition: Callable[[str], "FlagDefinition"]
    _get_all_global_flag_names: Callable[[], Collection[str]]

    def initialise(
        self,
        create_flag: Callable[[str, Optional[bool]], "Flag"],
        get_flag_definition: Callable[[str], "FlagDefinition"],
        get_all_flag_names: Callable[[], Collection[str]],
    ) -> "FlagService":
        self._create_flag = create_flag
        self._get_flag_definition = get_flag_definition
        self._get_all_global_flag_names = get_all_flag_names
        return self

    def merge_flag_lists(
        self, flag_lists: list[dict[str, "Flag"]]
    ) -> dict[str, "Flag"]:
        if not flag_lists:
            return {}

        merged_flags = flag_lists[0].copy() # Start with the first list of flags

        for flag_set in flag_lists[1:]:
            for flag_name, flag in flag_set.items():
                if flag_name not in merged_flags:
                    merged_flags[flag_name] = self._create_flag(flag_name, None)
                else:
                    self.merge_flag_values(merged_flags[flag_name], flag)

        return merged_flags

    def merge_flag_values(self, primary_flag: "Flag", update_flag: "Flag") -> None:
        if primary_flag.value is None:
            return
        if update_flag.value is None:
            primary_flag.value = None
        elif primary_flag.value is True and update_flag.value is False:
            primary_flag.value = False

    def get_inferred_from_flags(
        self,
        starting_flags: dict[str, "Flag"],
        is_nutrient_present: Callable[[str], bool],
    ) -> FUD[str, "Flag"]:
        inferred_flags: dict[str, "Flag"] = {}

        defined_flags = self.remove_undefined_flags(starting_flags)

        for flag in defined_flags.values():
            inferred_flags.update(
                self.get_inferred_from_flag(flag, is_nutrient_present)
            )

        return FUD(inferred_flags)

    def get_inferred_from_flag(
        self,
        flag: "Flag",
        is_nutrient_present: Callable[[str], bool],
    ) -> dict[str, "Flag"]:
        inferred_flags: dict[str, "Flag"] = {}

        definition = self._get_flag_definition(flag.name)

        if flag.value is True:
            for flag_name in definition.if_true_implies_true:
                inferred_flags[flag_name] = self._create_flag(flag_name, True)

            for flag_name in definition.if_true_implies_false:
                inferred_flags[flag_name] = self._create_flag(flag_name, False)

        elif flag.value is False:
            for flag_name in definition.if_false_implies_true:
                inferred_flags[flag_name] = self._create_flag(flag_name, True)

            for flag_name in definition.if_false_implies_false:
                inferred_flags[flag_name] = self._create_flag(flag_name, False)

        return inferred_flags

    def is_flag_defined(self, flags: dict[str, "Flag"], flag_name: str) -> bool:
        return flag_name in flags and flags[flag_name].value is not None

    def add_undefined_flags(self, flags: dict[str, "Flag"]) -> dict[str, "Flag"]:
        all_flags = flags.copy()

        for flag_name in self._get_all_global_flag_names():
            if flag_name not in all_flags:
                all_flags[flag_name] = self._create_flag(flag_name, None)

        return all_flags

    def remove_undefined_flags(
        self, flags: dict[str, "Flag"]
    ) -> dict[str, "Flag"]:
        return {name: flag for name, flag in flags.items() if flag.value is not None}
