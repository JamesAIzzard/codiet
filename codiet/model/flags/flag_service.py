from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model import SingletonRegister
    from codiet.model.flags import Flag, FlagFactory


class FlagService:

    _flag_factory: "FlagFactory"
    _singleton_register: "SingletonRegister"

    def initialise(
        self, flag_factory: "FlagFactory", singleton_register: "SingletonRegister"
    ) -> "FlagService":
        self._flag_factory = flag_factory
        self._singleton_register = singleton_register
        return self

    def merge_flag_lists(self, flag_lists: list[dict[str, "Flag"]]) -> dict[str, "Flag"]:
        merged_flags = {}

        for index, flag_set in enumerate(flag_lists):
            for flag_name, flag in flag_set.items():
                if flag_name not in merged_flags:
                    merged_flags[flag_name] = self._initialise_merged_flag(flag, index == 0)
                else:
                    self._update_merged_flag(merged_flags[flag_name], flag)

        return merged_flags

    def _initialise_merged_flag(self, flag: "Flag", is_first_set: bool) -> "Flag":
        if is_first_set:
            return flag
        return self._flag_factory.create_flag(flag.name, None)

    def _update_merged_flag(self, merged_flag: "Flag", new_flag: "Flag") -> None:
        if merged_flag.value is None:
            return
        elif new_flag.value is None:
            merged_flag.value = None
        elif merged_flag.value is True and new_flag.value is False:
            merged_flag.value = False
        # If they match or merged_flag is False, leave as is

    def infer_undefined_flag_values(
        self, merged_flags: dict[str, "Flag"]
    ) -> dict[str, "Flag"]:
        raise NotImplementedError
