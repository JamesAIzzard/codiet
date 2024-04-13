from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView
from codiet.models.ingredient import Ingredient
from codiet.utils.search import filter_text


class IngredientNutrientsEditorCtrl:
    """Controller for the IngredientNutrientsEditorView."""

    def __init__(self, view: IngredientNutrientsEditorView):
        self.view = view

        # Init the list of all nutrient names on the model
        self.all_nutrient_names: list[str] = []

        self.view.txt_filter.textChanged.connect(self.on_nutrient_filter_changed)
        self.view.btn_clear_filter.clicked.connect(self.on_clear_filter_clicked)

    @property
    def filtered_nutrients(self) -> list[str]:
        """Returns a list of nutrients that match the filter."""
        # Grab the filter text
        search_term = self.view.txt_filter.text().lower()
        # Strip whitespace
        search_term = search_term.strip()
        # If filter is empty, return all nutrients
        if not search_term:
            return self.all_nutrient_names
        else:
            # Filter the nutrients
            return filter_text(search_term, self.all_nutrient_names, 3)

    def set_model(self, ingredient: Ingredient) -> None:
        """Sets the ingredient model."""
        # Store the reference to the model
        self.ingredient = ingredient
        # Remove all nutrients from the view
        self.view.remove_all_nutrients()
        # Load all nutrient names into the cache
        self.all_nutrient_names = list(self.ingredient.nutrients.keys())
        # Update the view with each of these nutrient names
        for nutrient in self.all_nutrient_names:
            self.add_nutrient(nutrient)
        # Populate the view with all of the nutrient data
        for nutrient_name in self.ingredient.populated_nutrients:
            self.view.nutrient_widgets[nutrient_name].update_nutrient_mass(
                self.ingredient.nutrients[nutrient_name]["ntr_qty_value"]
            )
            self.view.nutrient_widgets[nutrient_name].update_nutrient_mass_units(
                self.ingredient.nutrients[nutrient_name]["ntr_qty_unit"]
            )
            self.view.nutrient_widgets[nutrient_name].update_ingredient_mass(
                self.ingredient.nutrients[nutrient_name]["ing_qty_value"]
            )
            self.view.nutrient_widgets[nutrient_name].update_ingredient_mass_units(
                self.ingredient.nutrients[nutrient_name]["ing_qty_unit"]
            )

    def add_nutrient(self, nutrient_name: str) -> None:
        """Adds a nutrient to the editor list, and connects up the signals."""
        # Update the view
        self.view._add_nutrient(nutrient_name)
        # Update the values on the widget
        self.view.nutrient_widgets[nutrient_name].update_nutrient_mass(
            self.ingredient.nutrients[nutrient_name]["ntr_qty_value"]
        )
        self.view.nutrient_widgets[nutrient_name].update_nutrient_mass_units(
            self.ingredient.nutrients[nutrient_name]["ntr_qty_unit"]
        )
        self.view.nutrient_widgets[nutrient_name].update_ingredient_mass(
            self.ingredient.nutrients[nutrient_name]["ing_qty_value"]
        )
        self.view.nutrient_widgets[nutrient_name].update_ingredient_mass_units(
            self.ingredient.nutrients[nutrient_name]["ing_qty_unit"]
        )
        # Connect the signals on the widget to the handlers
        widget = self.view.nutrient_widgets[nutrient_name]
        widget.txt_nutrient_mass.textChanged.connect(
            lambda mass, name=nutrient_name: self.on_nutrient_mass_changed(name, mass)
        )
        widget.cmb_mass_units.currentTextChanged.connect(
            lambda units, name=nutrient_name: self.on_nutrient_mass_units_changed(
                name, units
            )
        )
        widget.txt_ingredient_mass.textChanged.connect(
            lambda mass, name=nutrient_name: self.on_ingredient_mass_changed(name, mass)
        )
        widget.cmb_ingredient_mass_units.currentTextChanged.connect(
            lambda units, name=nutrient_name: self.on_ingredient_mass_units_changed(
                name, units
            )
        )

    def update_nutrient_visibility(self) -> None:
        """Updates the visibility of nutrients based on the filter and hide completed settings."""
        # Start by removing all nutrients
        self.view.remove_all_nutrients()
        # Grab the filtered nutrients
        filtered_nutrients = self.filtered_nutrients
        # Show all fitlered nutrients
        for nutrient in filtered_nutrients:
            self.add_nutrient(nutrient)

    def on_nutrient_mass_changed(self, nutrient_name: str, mass: float) -> None:
        """Updates the nutrient mass on the ingredient."""
        # Update the nutrient mass on the ingredient
        self.ingredient.update_nutrient_quantity(nutrient_name, ntr_qty_value=mass)

    def on_nutrient_mass_units_changed(self, nutrient_name: str, units: str) -> None:
        """Updates the nutrient mass units on the ingredient."""
        # Update the nutrient mass units on the ingredient
        self.ingredient.update_nutrient_quantity(nutrient_name, ntr_qty_unit=units)

    def on_ingredient_mass_changed(self, nutrient_name: str, mass: float) -> None:
        """Updates the ingredient mass on the ingredient."""
        # Update the ingredient mass on the ingredient
        self.ingredient.update_nutrient_quantity(nutrient_name, ing_qty_value=mass)

    def on_ingredient_mass_units_changed(self, nutrient_name: str, units: str) -> None:
        """Updates the ingredient mass units on the ingredient."""
        # Update the ingredient mass units on the ingredient
        self.ingredient.update_nutrient_quantity(nutrient_name, ing_qty_unit=units)

    def on_hide_completed_changed(self) -> None:
        """Filters the nutrient list based on the 'Hide Completed' checkbox."""
        self.update_nutrient_visibility()

    def on_nutrient_filter_changed(self) -> None:
        """Filters the nutrient list based on the filter text."""
        self.update_nutrient_visibility()

    def on_clear_filter_clicked(self) -> None:
        """Clears the nutrient filter."""
        self.view.txt_filter.clear()
        self.update_nutrient_visibility()
