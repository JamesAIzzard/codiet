from codiet.db.repository.repository_base import RepositoryBase

class IngredientRepository(RepositoryBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def create_ingredient(
        self,
        ingredient_name: str,
        ingredient_description: str|None = None,
        ingredient_gi: float|None = None,
        cost_value: float|None = None,
        cost_qty_unit_id: int|None = None,
        cost_qty_value: float|None = None,
        standard_unit_id: int|None = None,
    ) -> int:
        """Adds an ingredient to the ingredient table and returns the ID."""
        # Set the cost_unit_id for now to None as it is not used
        cost_unit_id = None

        with self.get_cursor() as cursor:
                
                cursor.execute(
                    """
                    INSERT INTO ingredient_base (name, description, gi, cost_value, cost_unit_id, cost_qty_unit_id, cost_qty_value, standard_unit_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                    (ingredient_name, ingredient_description, ingredient_gi, cost_value, cost_unit_id, cost_qty_unit_id, cost_qty_value, standard_unit_id),
                )
    
                # Get the ID of the ingredient
                id = cursor.lastrowid

        assert id is not None

        return id