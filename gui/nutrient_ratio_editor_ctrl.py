import gui, data

class NutrientRatioEditorCtrl(gui.CodietCtrl):
    def __init__(self, 
        nutrient_str: str,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Stash the nutrient name
        self.nutrient_name = nutrient_str

        # Call out the view type for intellisense
        self.view: gui.NutrientRatioEditorView

        # Initial setup
        # Initially put basic mass units in the dropdowns
        mass_units = data.quantity.get_mass_units()
        gui.utils.cmb_add_items_once(
            self.view.cmb_ingredient_qty_unit, mass_units
        )
        gui.utils.cmb_add_items_once(
            self.view.cmb_nutrient_mass_unit, mass_units
        )