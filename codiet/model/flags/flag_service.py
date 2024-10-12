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

    def populate_implied_flags(
        self, defined_flags: dict[str, "Flag"]
    ) -> dict[str, "Flag"]:

        undefined_flags = self.get_undefined_flags(defined_flags)

        for defined_flag_name, defined_flag in defined_flags.items():
            flag_definition = self._get_flag_definition(defined_flag_name)
            if defined_flag.value is True:
                for implied_flag_name in flag_definition.implies:
                    if implied_flag_name in undefined_flags:
                        undefined_flags[implied_flag_name].value = True

        defined_flags.update(undefined_flags)
        return defined_flags

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
    
    def get_undefined_flags(self, flags: dict[str, "Flag"]) -> dict[str, "Flag"]:
        global_flag_names = self._get_all_global_flag_names()

        undefined_flags = {}

        for global_flag_name in global_flag_names:
            if global_flag_name not in flags:
                undefined_flags[global_flag_name] = self._create_flag(global_flag_name, None)

        return undefined_flags
