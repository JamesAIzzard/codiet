from codiet.models.ingredients.ingredient_quantity import IngredientQuantity
from codiet.models.time.recipe_serve_time_window import RecipeServeTimeWindow
from codiet.models.tags.recipe_tag import RecipeTag
from codiet.db.stored_entity import StoredEntity

class Recipe(StoredEntity):
    def __init__(
            self, 
            name: str, 
            description: str | None = None,
            instructions: str | None = None,
            use_as_ingredient: bool = False,
            ingredient_quantities: set[IngredientQuantity]|None = None,
            serve_time_windows: set[RecipeServeTimeWindow]|None = None,
            tags: set[RecipeTag]|None = None,
            *args, **kwargs
        ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)
        self._name = name
        self._use_as_ingredient = use_as_ingredient
        self._description = description
        self._instructions = instructions
        self._ingredient_quantities = ingredient_quantities if ingredient_quantities is not None else set()
        self._serve_time_windows = serve_time_windows if serve_time_windows is not None else set()
        self._tags = tags if tags is not None else set()

    @property
    def name(self) -> str:
        """Get the name of the recipe."""
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the recipe."""
        # Raise an exception if the name is None or just whitespace
        if name is None or name.strip() == "":
            raise ValueError("Name cannot be None or empty.")
        self._name = name

    @property
    def use_as_ingredient(self) -> bool:
        """Get whether the recipe is used as an ingredient."""
        return self._use_as_ingredient
    
    @use_as_ingredient.setter
    def use_as_ingredient(self, use_as_ingredient: bool) -> None:
        """Set whether the recipe is used as an ingredient."""
        self._use_as_ingredient = use_as_ingredient

    @property
    def description(self) -> str | None:
        """Get the description of the recipe."""
        return self._description
    
    @description.setter
    def description(self, description: str | None) -> None:
        """Set the description of the recipe."""
        self._description = description

    @property
    def instructions(self) -> str | None:
        """Get the instructions for the recipe."""
        return self._instructions
    
    @instructions.setter
    def instructions(self, instructions: str | None) -> None:
        """Set the instructions for the recipe."""
        self._instructions = instructions

    @property
    def ingredient_quantities(self) -> frozenset[IngredientQuantity]:
        """Get the ingredients for the recipe."""
        return frozenset(self._ingredient_quantities)

    @property
    def serve_time_windows(self) -> frozenset[RecipeServeTimeWindow]:
        """Get the serve times for the recipe."""
        return frozenset(self._serve_time_windows)

    @property
    def tags(self) -> frozenset[RecipeTag]:
        """Get the recipe tags for the recipe."""
        return frozenset(self._tags)

    def get_ingredient_quantity(self, ingredient_name:str) -> IngredientQuantity:
        """Get an ingredient quantity by its name."""
        for ingredient_quantity in self._ingredient_quantities:
            if ingredient_quantity.ingredient.name == ingredient_name:
                return ingredient_quantity
        raise ValueError(f"Ingredient quantity with name {ingredient_name} not found.")

    def update_ingredient_quantities(self, ingredient_quantities: set[IngredientQuantity]) -> None:
        """Update the ingredients in the recipe."""
        for iq in ingredient_quantities:
            if iq in self._ingredient_quantities:
                self._ingredient_quantities.remove(iq)
            self._ingredient_quantities.add(iq)

    def remove_ingredient_quantities(self, ingredient_quantities:set[IngredientQuantity]) -> None:
        """Remove a list of ingredients from the recipe."""
        for iq in ingredient_quantities:

            # Work through the ingredients and remove the one with the given ID
            for ingredient_qty in self._ingredient_quantities:

                if ingredient_qty == iq:
                    self._ingredient_quantities.remove(ingredient_qty)
                    break

    def update_serve_time_windows(self, serve_time_windows: set[RecipeServeTimeWindow]) -> None:
        """Update the serve times for the recipe."""
        for stw in serve_time_windows:
            if stw in self._serve_time_windows:
                self._serve_time_windows.remove(stw)
            self._serve_time_windows.add(stw)

    def remove_serve_time_windows(self, serve_time_windows:set[RecipeServeTimeWindow]) -> None:
        """Remove a list of serve times from the recipe."""
        for stw in serve_time_windows:

            # Work through the serve times and remove the one with the given ID
            for serve_time_window in self._serve_time_windows:

                if serve_time_window == stw:
                    self._serve_time_windows.remove(serve_time_window)           

    def update_tags(self, tags: set[RecipeTag]) -> None:
        """Update the tags for the recipe."""
        for tag in tags:
            if tag in self._tags:
                self._tags.remove(tag)
            self._tags.add(tag)

    def remove_tags(self, tags: set[RecipeTag]) -> None:
        """Remove a list of tags from the recipe."""
        for tag in tags:

            # Work through the tags and remove the one with the given ID
            for recipe_tag in self._tags:

                if recipe_tag == tag:
                    self._tags.remove(recipe_tag)
            
    def __eq__(self, other):
        """Check if two recipes are equal."""
        if not isinstance(other, Recipe):
            return False
        if self.id is None and self.name is None:
            raise ValueError("Recipe must have an ID or a name for comparison.")
        if self.id is None or other.id is None:
            return self.name == other.name
        return self.id == other.id
    
    def __hash__(self):
        """Hash the recipe."""
        return hash((self.id, self.name))
