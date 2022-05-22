import typing

import codiet
from example_app import gui


class FlagSelectorCtrl(gui.CodietCtrl):
    def __init__(self,
        on_flag_adoption_callback: typing.Optional[typing.Callable[[str], None]]=None,
        on_flag_removal_callback: typing.Optional[typing.Callable[[str], None]]=None,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.view: gui.FlagSelectorView

        self.global_flags = {}
        self.adopted_flags = {}

        # Stash the callbacks
        self.on_flag_adoption_callback = on_flag_adoption_callback
        self.on_flag_removal_callback = on_flag_removal_callback

        # Wire the responses up
        self.view.btn_adopt_flag.clicked.connect(self._on_flag_adoption)
        self.view.btn_remove_flag.clicked.connect(self._on_flag_removal)

        # Load the global flags
        self.init_global_flags()


    def init_global_flags(self) -> None:
        """Loads the global flags and populates them on the list."""
        # Init the local cache of global flags
        self.global_flags = codiet.get_flag_names_and_strings()
        # Clear the global flags on the view
        self.view.clear_global_flags()
        # Set the global flags on the view
        self.view.set_global_flags(list(self.global_flags.values()))

    def _on_flag_adoption(self) -> None:
        """Handler for adoption button press.
        Runs the on_flag_adoption_callback function before changing the list views,
        passing in the currently selected global flag string.
        """
        # ID the selected flag string on the view
        selected_flag_string = self.view.selected_global_flag
        # If a flag is selected, and not already adopted
        if (
            selected_flag_string is not None
            and selected_flag_string not in self.view.all_adopted_flags
        ):
            # Grab the flag_name corresponding to the flag_string
            flag_name = codiet.flag_string_to_name(selected_flag_string)
            # Fire the callback if present
            if self.on_flag_adoption_callback is not None:
                self.on_flag_adoption_callback(flag_name)
            # Adopt the flag in the view
            self.view.adopt_flag(selected_flag_string)
            # Add the flag to the adopted list
            self.adopted_flags[flag_name] = selected_flag_string

    def _on_flag_removal(self) -> None:
        """Handler for removal button press.
        Runs the on_flag_removal_callback function before changing the list views,
        passing in the currently selected adopted flag.
        """
        selected_flag_string = self.view.selected_adopted_flag        
        if selected_flag_string is not None:
            # Grab the flag_name corresponding to the flag_string
            flag_name = codiet.flag_string_to_name(selected_flag_string)
            # Fire the callback if present
            if self.on_flag_removal_callback is not None:
                self.on_flag_removal_callback(flag_name)
            # Adopt the flag in the view
            self.view.remove_flag(selected_flag_string)
            # Add the flag to the adopted list
            del self.adopted_flags[flag_name]
