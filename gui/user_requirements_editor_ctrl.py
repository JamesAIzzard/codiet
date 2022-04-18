import model, gui

class UserRequirementsEditorCtrl(gui.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out the view type for intellisense
        self.view: gui.UserRequirementsEditorView

        # Init the controller for the flag editor
        self.flag_selector_ctrl = gui.FlagSelectorCtrl(
            view=self.view.wg_flag_selector,
            on_flag_adoption_callback=self.on_user_flag_adopted,
            on_flag_removal_callback=self.on_user_flag_removal
        )

    def on_user_flag_adopted(self, flag_str) -> None:
        """Handler for adoption of user flag."""
        pass

    def on_user_flag_removal(self, flag_str) -> None:
        """Handler for removal of user flag."""
        pass
   