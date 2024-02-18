from PyQt6.QtCore import Qt

from codiet.db.database_service import DatabaseService
from codiet.views.flag_editor_view import FlagEditorView


class FlagEditorCtrl:
    def __init__(self, view: FlagEditorView, db_service: DatabaseService):
        self.view = view
        self.db_service = db_service

        # Grab a list of all flags
        self.flags = self.db_service.get_all_flags()
        # Work through each flag and populate the list
        for flag in self.flags:
            # Capitalise each word in the flag name
            flag = flag.title()
            self.view.add_flag_to_list(flag)

        # Connect the buttons to the controller methods
        self.view.btn_select_all.clicked.connect(self.select_all_flags)
        self.view.btn_deselect_all.clicked.connect(self.deselect_all_flags)
        self.view.btn_invert_selection.clicked.connect(self.invert_selection)
        self.view.btn_clear_selection.clicked.connect(self.clear_selection)


    def select_flag(self, flag: str):
        '''Update the flag to be selected.'''
        self.view.select_flag(flag)

    def deselect_flag(self, flag: str):
        '''Update the flag to be deselected.'''
        self.view.deselect_flag(flag)

    def select_all_flags(self):
        '''Select all flags.'''
        for flag in self.flags:
            self.view.select_flag(flag)

    def deselect_all_flags(self):
        '''Deselect all flags.'''
        for flag in self.flags:
            self.view.deselect_flag(flag)

    def invert_selection(self):
        '''Invert the selection of all flags.'''
        for flag in self.flags:
            self.view.invert_flag_selection(flag)

    def clear_selection(self):
        '''Clear the selection of all flags.'''
        for flag in self.flags:
            self.view.deselect_flag(flag)