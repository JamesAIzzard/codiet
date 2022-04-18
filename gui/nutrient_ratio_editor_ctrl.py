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
        self.view.set_nutrient_mass_units(data.get_mass_units())
        self.view.set_ingredient_qty_units(data.get_mass_units())