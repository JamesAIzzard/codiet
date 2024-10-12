from typing import TYPE_CHECKING, Callable, Optional, Collection

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
        merged_flags = {}

        for index, flag_set in enumerate(flag_lists):
            for flag_name, flag in flag_set.items():
                if flag_name not in merged_flags:
                    merged_flags[flag_name] = self._initialise_merged_flag(
                        flag, index == 0
                    )
                else:
                    self._update_merged_flag(merged_flags[flag_name], flag)

        return merged_flags

    def infer_undefined_flags(
        self,
        starting_flags: dict[str, "Flag"],
        is_nutrient_present: Callable[[str], bool],
    ) -> dict[str, "Flag"]:
        all_flags = self.add_undefined_flags(starting_flags)

        defined_flags = self.remove_undefined_flags(all_flags)

        for flag_name, flag in defined_flags.items():
            definition = self._get_flag_definition(flag_name)

            implied_true = definition.get_names_implied_true(
                flag.value, is_nutrient_present # type: ignore
            )
            implied_false = definition.get_names_implied_false(
                flag.value, is_nutrient_present # type: ignore
            )

            for implied_flag_name in implied_true:
                all_flags[implied_flag_name].value = True

            for implied_flag_name in implied_false:
                all_flags[implied_flag_name].value = False

        return all_flags

    def _initialise_merged_flag(self, flag: "Flag", is_first_set: bool) -> "Flag":
        if is_first_set:
            return flag
        return self._create_flag(flag.name, None)

    def _update_merged_flag(self, merged_flag: "Flag", new_flag: "Flag") -> None:
        if merged_flag.value is None:
            return
        elif new_flag.value is None:
            merged_flag.value = None
        elif merged_flag.value is True and new_flag.value is False:
            merged_flag.value = False
        # If they match or merged_flag is False, leave as is
    
    def add_undefined_flags(self, flags: dict[str, "Flag"]) -> dict[str, "Flag"]:
        all_flags = dict(flags)

        for flag_name in self._get_all_global_flag_names():
            if flag_name not in all_flags:
                all_flags[flag_name] = self._create_flag(flag_name, None)

        return all_flags
    
    def remove_undefined_flags(
        self, flags: dict[str, "Flag"]
    ) -> dict[str, "Flag"]:
        return {name: flag for name, flag in flags.items() if flag.value is not None}
