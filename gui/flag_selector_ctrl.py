from select import select
from typing import Callable

import gui, data

class FlagSelectorCtrl(gui.CodietCtrl):
    def __init__(self,
        on_flag_adoption_callback: Callable,
        on_flag_removal_callback: Callable,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.view: gui.FlagSelectorView

        # Stash the callbacks
        self.on_flag_adoption_callback = on_flag_adoption_callback
        self.on_flag_removal_callback = on_flag_removal_callback

        # Wire the responses up
        self.view.btn_adopt_flag.clicked.connect(self._on_flag_adoption)
        self.view.btn_remove_flag.clicked.connect(self._on_flag_removal)

        # Load the global flags
        self.set_global_flags()

    def set_global_flags(self) -> None:
        """Loads the global flags into the box."""
        self.view.clear_global_flags()
        self.view.set_global_flags(data.get_flag_strings())

    def _on_flag_adoption(self) -> None:
        """Handler for adoption button press.
        Runs the on_flag_adoption_callback function before changing the list views,
        passing in the currently selected global flag string.
        """
        selected_flag = self.view.selected_global_flag
        if selected_flag is not None and selected_flag not in self.view.all_adopted_flags:
            self.on_flag_adoption_callback(selected_flag)
            self.view.adopt_flag(selected_flag)

    def _on_flag_removal(self) -> None:
        """Handler for removal button press.
        Runs the on_flag_removal_callback function before changing the list views,
        passing in the currently selected adopted flag.
        """
        selected_flag = self.view.selected_adopted_flag
        if selected_flag is not None:
            self.on_flag_removal_callback(selected_flag)
            self.view.remove_flag(selected_flag)