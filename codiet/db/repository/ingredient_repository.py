from codiet.db.repository.repository_base import RepositoryBase

class IngredientRepository(RepositoryBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def create_ingredient_base(
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
    
    def read_all_ingredient_names(self) -> dict[int, str]:
        """Returns a dictionary of all ingredient names and their IDs."""
        with self.get_cursor() as cursor:
            cursor.execute("SELECT id, name FROM ingredient_base;")
            return {row[0]: row[1] for row in cursor.fetchall()}
        
    def read_ingredient_base(self, ingredient_id: int) -> dict:
        """Returns the ingredient with the given ID.
        Returns:
            {
                'id': int,
                'name': str,
                'description': str|None,
                'gi': float|None,
                'cost_value': float|None,
                'cost_unit_id': int|None,
                'cost_qty_unit_id': int|None,
                'cost_qty_value': float|None,
                'standard_unit_id': int|None,
            }
        """
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, description, gi, cost_value, cost_unit_id, cost_qty_unit_id, cost_qty_value, standard_unit_id
                FROM ingredient_base
                WHERE id = ?;
                """,
                (ingredient_id,),
            )
            return cursor.fetchone()