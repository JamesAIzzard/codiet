import codiet
import app

class NutrientRatioEditorCtrl(app.CodietCtrl):
    def __init__(self, 
        nutrient_str: str,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Stash the nutrient name
        self.nutrient_name = nutrient_str

        # Call out the view type for intellisense
        self.view: app.NutrientRatioEditorView

        # Initial setup
        # Initially put basic mass units in the dropdowns
        mass_units = list(codiet.get_mass_units().keys())
        self.view.cmb_ingredient_qty_unit.add_items_once(mass_units)
        self.view.cmb_nutrient_mass_unit.add_items_once(mass_units)