import typing

import gui, data, model


class IngredientEditorCtrl(gui.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create dict for nutrient editor controllers
        self.nutrient_editor_ctrls: typing.Dict[str, gui.NutrientRatioEditorCtrl] = {}

        # Call out the view type for intellisense
        self.view: gui.IngredientEditorView

        # Init controller for flag selector widget
        self.flag_selector_ctrl = gui.FlagSelectorCtrl(
            view=self.view.wg_flag_selector,
            on_flag_adoption_callback=self.on_flag_adopt,
            on_flag_removal_callback=self.on_flag_remove,
        )

        # Load in a fresh ingredient instance
        self.ingredient = model.ingredients.Ingredient()

        # Initial setup on the form
        # Cache the basic mass units
        mass_units = data.get_mass_units()
        # Do the cost widget setup
        gui.utils.cmb_add_items_once(
            self.view.cmb_cost_units, mass_units
        )
        # Do the bulk widget setup
        gui.utils.cmb_add_items_once(
            self.view.cmb_ref_qty_units, mass_units
        )
        gui.utils.cmb_add_items_once(
            self.view.cmb_mass_pieces_units, mass_units
        )      
        # Do the nutrients widget setup
        nutrients = data.get_adopted_nutrients()
        for nutrient in nutrients:
            self.add_nutrient_ratio_editor(
                nutrient_name=nutrient[0], nutrient_str=nutrient[1]
            )

        # Wire the active elements
        self.view.btn_save_ingredient.clicked.connect(  # type: ignore
            self.on_save_ingredient
        )

    def add_nutrient_ratio_editor(self, nutrient_name: str, nutrient_str: str) -> None:
        """Adds a nutrient ratio editor widget."""
        # Create the view
        view = gui.NutrientRatioEditorView(nutrient_str=nutrient_str)
        ctrl = gui.NutrientRatioEditorCtrl(view=view, nutrient_str=nutrient_str)
        self.nutrient_editor_ctrls[nutrient_name] = ctrl
        self.view.add_nutrient_widget(view)

    def on_flag_adopt(self, flag_str: str) -> None:
        """Handler function for flag adoption."""
        pass

    def on_flag_remove(self, flag_str: str) -> None:
        """Hander function for flag removal."""
        pass

    def on_save_ingredient(self) -> None:
        """Click handler for save ingredient button."""
        # Grab the name from the ingredient lineedit
        self.ingredient.name = self.view.name
        # Convert the cost to a cost per gram
        cost_per_unit = self.view.cost / self.view.cost_mass
        cost_per_gram = model.units.convert_mass(
            starting_units = self.view.cost_units,
            starting_value = self.view.cost
        )
        # Hmmmm, not sure about the best way to do this just yet.
        data.save_ingredient(self.ingredient)