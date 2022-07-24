import typing

from PyQt6 import QtWidgets, uic

import app
import codiet


class IngredientEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out active elements for intellisense
        self.txt_ingredient_name: app.CodietLineEdit
        self.txt_cost: app.CodietNumberLineEdit
        self.txt_cost_qty: app.CodietNumberLineEdit
        self.cmb_cost_units: app.CodietComboBox
        self.txt_dens_vol: app.CodietNumberLineEdit
        self.cmb_dens_vol_units: app.CodietComboBox
        self.txt_dens_mass: app.CodietNumberLineEdit
        self.cmb_dens_mass_units: app.CodietComboBox
        self.txt_num_pieces: app.CodietNumberLineEdit
        self.txt_mass_pieces: app.CodietNumberLineEdit
        self.cmb_mass_pieces_units: app.CodietComboBox
        self.wg_flag_selector: app.FlagSelectorView
        self.txt_gi: app.CodietNumberLineEdit
        self.scl_nutrients: QtWidgets.QWidget
        self.lyt_flags: QtWidgets.QVBoxLayout
        self.lyt_nutrients: QtWidgets.QVBoxLayout
        self.btn_save_ingredient: QtWidgets.QPushButton
        self.wg_ingredient_search: app.SearchWidgetView

        # Create a dict to store the nutrient editor views
        self.nutrient_editor_views: typing.Dict[str, app.NutrientRatioEditorView] = {}

        # Load in the ui file
        uic.load_ui.loadUi("app/ingredient_editor.ui", self)

        # Set the validators to catch basic errors
        self.txt_cost.setValidator(app.PositiveFloatValidator())
        self.txt_cost_qty.setValidator(app.PositiveFloatValidator())
        self.txt_dens_vol.setValidator(app.PositiveFloatValidator())
        self.txt_dens_mass.setValidator(app.PositiveFloatValidator())
        self.txt_num_pieces.setValidator(app.PositiveFloatValidator())
        self.txt_mass_pieces.setValidator(app.PositiveFloatValidator())
        self.txt_gi.setValidator(app.Float0To100Validator())


    @property
    def cost_is_defined(self) -> bool:
        """Returns True/False to indicate if the cost fields are defined."""
        if self.txt_cost.text() is None:
            return False
        if self.txt_cost_qty.text() is None:
            return False
        return True

    @property
    def dens_is_defined(self) -> bool:
        """Returns True/False to indicate if the density is defined."""
        if self.txt_dens_vol.text() is None:
            return False
        elif self.txt_dens_mass.text() is None:
            return False
        else:
            return True

    @property
    def piece_mass_is_defined(self) -> bool:
        """Returns True/False to indicate if peice mass is defined."""
        if self.txt_num_pieces.text() is None:
            return False
        elif self.txt_mass_pieces.text() is None:
            return False
        else:
            return True

    @property
    def all_nutrient_fields_filled(self) -> bool:
        """Returns True/False to indicate if all the nutrients have been defined.
        Note:
            This doesn't do any checks to ensure that this is the full list of adopted nutrients.
            It just checks that all nutrient lines on the form have been populated.
        """
        for view in self.nutrient_editor_views.values():
            if not view.nutrient_ratio_defined:
                return False
        # All were defined
        return True

    @property
    def all_nutrient_ratio_data(self) -> typing.Dict[str, codiet.NutrientRatioData]:
        """Returns the nutrients data."""
        nutrient_ratio_data = {}
        for nut_name, nr_widget in self.nutrient_editor_views.items():
            nutrient_ratio_data[nut_name] = self.get_nutrient_ratio_data(nut_name)
        return nutrient_ratio_data

    def get_nutrient_ratio_data(self, nutrient_name) -> codiet.NutrientRatioData:
        nr_widget = self.nutrient_editor_views[nutrient_name]
        return {
            "nutrient_mass": nr_widget.txt_nutrient_mass.text(),
            "nutrient_mass_unit": nr_widget.cmb_nutrient_mass_unit.currentText(),
            "ingredient_qty": nr_widget.txt_ingredient_qty.text(),
            "ingredient_qty_unit": nr_widget.cmb_ingredient_qty_unit.currentText(),
        }

    def add_nutrient_widget(
        self, nutrient_name: str, view: app.NutrientRatioEditorView
    ) -> None:
        """Adds a nutrient ratio editor widget view."""
        # Stash the view instance
        self.nutrient_editor_views[nutrient_name] = view
        # Insert the view
        self.lyt_nutrients.addWidget(view)
