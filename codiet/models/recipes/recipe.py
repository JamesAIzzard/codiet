from codiet.models.ingredients.ingredient_quantity import IngredientQuantity
from codiet.models.entity_serve_time_window import EntityServeTimeWindow
from codiet.models.tags.entity_tag import EntityTag
from codiet.db.stored_entity import StoredEntity

class Recipe(StoredEntity):
    def __init__(
            self, 
            name: str, 
            description: str | None = None,
            instructions: str | None = None,
            use_as_ingredient: bool = False,
            ingredient_quantities: list[IngredientQuantity]|None = None,
            serve_time_windows: list[EntityServeTimeWindow]|None = None,
            tags: list[EntityTag]|None = None,
            *args, **kwargs
        ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)
        self._name = name
        self._use_as_ingredient = use_as_ingredient
        self._description = description
        self._instructions = instructions
        self._ingredient_quantities = ingredient_quantities if ingredient_quantities is not None else []
        self._serve_time_windows = serve_time_windows if serve_time_windows is not None else []
        self._tags = tags if tags is not None else []

    @property
    def name(self) -> str:
        """Get the name of the recipe."""
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the recipe."""
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
    def ingredient_quantities(self) -> list[IngredientQuantity]:
        """Get the ingredients for the recipe."""
        return self._ingredient_quantities

    @property
    def serve_time_windows(self) -> list[EntityServeTimeWindow]:
        """Get the serve times for the recipe."""
        return self._serve_time_windows

    @property
    def tags(self) -> list[EntityTag]:
        """Get the recipe tags for the recipe."""
        return self._tags

    def add_ingredient_quantities(self, ingredient_quantities: list[IngredientQuantity]) -> None:
        """Add a list of ingredients to the recipe."""
        for ingredient_quantity in ingredient_quantities:
            # Raise an exception if this ingredient is already in the recipe
            # or if there is an ingredient quantity with the same id in the recipe
            for ingredient_qty in self._ingredient_quantities:
                if ingredient_qty.ingredient_id == ingredient_quantity.ingredient_id:
                    raise KeyError("Ingredient already in recipe")
                if ingredient_qty.id == ingredient_quantity.id:
                    raise KeyError("Ingredient quantity ID already in recipe")
    
            # Go ahead and add it
            self._ingredient_quantities.append(ingredient_quantity)

    def remove_ingredient_quantities(self, ingredient_quantity_ids: list[int]) -> None:
        """Remove a list of ingredients from the recipe."""
        for ingredient_quantity_id in ingredient_quantity_ids:
            # Work through the ingredients and remove the one with the given ID
            for ingredient_qty in self._ingredient_quantities:
                if ingredient_qty.id == ingredient_quantity_id:
                    self._ingredient_quantities.remove(ingredient_qty)
                    break
            else:
                # Raise an exception if the ingredient quantity is not found
                raise ValueError(f"Ingredient quantity with ID {ingredient_quantity_id} not found.")

    def add_serve_time_windows(self, serve_time_windows:list[EntityServeTimeWindow]) -> None:
        """Add a list of serve time windows to the recipe"""
        for window in serve_time_windows:
            # Raise an exception if the window is either a subset or superset of an existing window in the recipe
            for existing_window in self._serve_time_windows:
                if existing_window.is_superset_of(window):
                    raise ValueError("Window is a subset of an existing window in the recipe")
                if existing_window.is_subset_of(window):
                    raise ValueError("Window is a superset of an existing window in the recipe")
            # Raise an exception if the window's ID is not None and is already in the recipe
            if window.id is not None:
                for existing_window in self._serve_time_windows:
                    if existing_window.id == window.id:
                        raise KeyError("Window ID already in recipe")
            # Add the serve time to the recipe
            self._serve_time_windows.append(window)

    def remove_serve_time_windows(self, serve_time_window_ids: list[int]) -> None:
        """Remove a serve time from the recipe."""
        # Remove the serve time from the recipe
        for serve_time_window_id in serve_time_window_ids:
            for serve_time_window in self._serve_time_windows:
                if serve_time_window.id == serve_time_window_id:
                    self._serve_time_windows.remove(serve_time_window)
                    break
            else:
                # Raise an exception if the serve time window is not found
                raise ValueError(f"Serve time window with ID {serve_time_window_id} not found.")

    def add_tags(self, tags:list[EntityTag]) -> None:
        """Add recipe tags to the recipe."""
        for tag in tags:
            # Raise an exception if the tag is already in the recipe
            for existing_tag in self._tags:
                if existing_tag.id == tag.id:
                    raise KeyError("Tag already in recipe")
            # Add the tag to the recipe
            self._tags.append(tag)

    def remove_tags(self, tag_ids:list[int]) -> None:
        """Remove a recipe tags from the recipe."""
        for tag_id in tag_ids:
            # Remove the tag from the recipe
            for tag in self._tags:
                if tag.id == tag_id:
                    self._tags.remove(tag)
                    break
            else:
                # Raise an exception if the tag is not found
                raise ValueError(f"Tag with ID {tag_id} not found.")
