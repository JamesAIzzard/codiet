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

    def merge_flag_lists(
        self, flag_lists: list[dict[str, "Flag"]]
    ) -> dict[str, "Flag"]:
        merged_flags = {}

        first_flag_set = True

        for flag_set in flag_lists:
            for flag_name, flag in flag_set.items():
                # If the flag isn't present, but we are on the first set, just add it with
                # the value it has, otherise, add it with a value of None
                if flag_name not in merged_flags:
                    if first_flag_set:
                        merged_flags[flag_name] = flag
                    else:
                        merged_flags[flag_name] = self._flag_factory.create_flag(
                            flag_name, None
                        )
                else:
                    current_merged_flag = merged_flags[flag_name]

                    if current_merged_flag.value is None:
                        continue  # Skip to next flag, it's already indeterminate
                    elif flag.value is None:
                        current_merged_flag.value = None  # Set to indeterminate
                    elif current_merged_flag.value is False and flag.value is True:
                        current_merged_flag.value = (
                            False  # Existing False flags prevent the merge being True
                        )
                    elif current_merged_flag.value is True and flag.value is False:
                        current_merged_flag.value = False
                    # If they match, leave as is
            first_flag_set = False

        return merged_flags

    def infer_undefined_flag_values(
        self, merged_flags: dict[str, "Flag"]
    ) -> dict[str, "Flag"]:
        raise NotImplementedError
