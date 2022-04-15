import model, gui

class UserRequirementsEditorCtrl:
    def __init__(self, view: gui.UserRequirementsEditorView):
        self.view = view

        # Wire the add/remove buttons
        self.view.btn_adopt_flag.clicked.connect(self.on_adopt_flag_click)
        self.view.btn_remove_flag.clicked.connect(self.on_remove_flag_click)

        # Do initial setup on the view
        self.populate_global_flags()
        self.populate_user_flags()

    def on_adopt_flag_click(self):
        """Click handler for the adopt flag button."""
        # Grab the currently selected flag name
        flag_name = model.flags.get_flag_name_from_string(
            self.view.lst_global_flags.currentItem().text()
        )
        # Add the flag to the model user
        model.user.add_global_flag(flag_name)
        # Update the user flags list on the view
        self.populate_user_flags()

    def on_remove_flag_click(self):
        """Click handler for the remove flag button."""
        # Grab the currently selected flag name
        flag_name = model.flags.get_flag_name_from_string(
            self.view.lst_user_flags.currentItem().text()
        )
        # Remove the flag from the model user
        model.user.global_flags.remove(flag_name)
        # Update the user flags list on the view
        self.populate_user_flags()

    def populate_global_flags(self):
        """Uses the flag configs to populate the list of global flags on the view."""
        # Clear the list
        self.view.lst_global_flags.clear()
        # Rebuild the list
        for flag in model.configs.FLAG_CONFIGS.values():
            self.view.lst_global_flags.addItem(flag["string"])

    def populate_user_flags(self):
        """Populates list of user flags on the gui from list on user model."""
        # Clear the list
        self.view.lst_user_flags.clear()
        # Rebuild the list
        for flag in model.user.global_flags:
            self.view.lst_user_flags.addItem(model.configs.FLAG_CONFIGS[flag]["string"])