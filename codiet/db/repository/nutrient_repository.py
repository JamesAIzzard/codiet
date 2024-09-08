from codiet.db.repository.repository_base import RepositoryBase

class NutrientRepository(RepositoryBase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def create_global_nutrient(
            self, 
            nutrient_name: str,
            parent_id: int|None
        ) -> int:
        """Adds a nutrient to the nutrient base table and returns the ID."""
        # Add the global nutrient to the base table
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO global_nutrients (nutrient_name, parent_id) VALUES (?, ?);
            """,
                (nutrient_name, parent_id),
            )

            # Get the ID of the nutrient
            id = cursor.lastrowid

        assert id is not None

        return id
    
    def create_global_nutrient_alias(self, alias: str, primary_nutrient_id:int) -> int:
        """Adds an alias to the nutrient alias table."""
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO nutrient_aliases (nutrient_alias, primary_nutrient_id) VALUES (?, ?);
            """,
                (alias, primary_nutrient_id),
            )

            # Get the ID of the nutrient
            id = cursor.lastrowid

        assert id is not None

        return id

    def create_ingredient_nutrient_quantity(
            self,
            ingredient_id: int,
            nutrient_id: int,
            nutrient_mass_unit_id: int,
            nutrient_mass_value: float|None=None,
            ingredient_grams_qty: float|None=None
    ) -> int:
        """Adds a nutrient quantity to the ingredient nutrient quantity table and returns the ID."""
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO ingredient_nutrient_quantities (ingredient_id, nutrient_id, ntr_mass_unit_id, ntr_mass_value, ing_grams_qty) VALUES (?, ?, ?, ?, ?);
            """,
                (ingredient_id, nutrient_id, nutrient_mass_unit_id, nutrient_mass_value, ingredient_grams_qty),
            )

            # Get the ID of the nutrient
            id = cursor.lastrowid

        assert id is not None

        return id

    def read_global_nutrients(self) -> list[dict]:
        """Reads all global nutrients from the database.

        Note:
            We only need to the parent or the child id to for each nutrient to fully
            define the tree. It is nicer to just store a single value, and each nutrent
            can only have a single parent, so it makes sense to store the parent id

        Returns:
            list[dict]: A list of dictionaries containing the global nutrient data.
                [
                    {
                        'id': int, 
                        'nutrient_name': str, 
                        'parent_id': int|None
                    },
                ]
        """
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nutrient_name, parent_id FROM global_nutrients;
                """
            )
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0], 
                    'nutrient_name': row[1], 
                    'parent_id': row[2]
                }
                for row in rows
            ]
        
    def read_global_nutrient_aliases(self, nutrient_id: int) -> list[dict]:
        """Reads all aliases for a global nutrient.
        Args:
            nutrient_id (int): The ID of the global nutrient.
        Returns:
            list[dict]: A list of dictionaries containing the alias data.
                [
                    {
                        'alias_id': int, 
                        'alias': str
                    },
                ]
        """
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nutrient_alias FROM nutrient_aliases WHERE primary_nutrient_id = ?;
                """,
                (nutrient_id,)
            )
            rows = cursor.fetchall()
            return [
                {
                    'alias_id': row[0], 
                    'alias': row[1]
                }
                for row in rows
            ]

        
    def read_ingredient_nutrient_quantities(self, ingredient_id: int) -> list[dict]:
        """Reads all nutrient quantities for an ingredient.
        Args:
            ingredient_id (int): The ID of the ingredient.
        Returns:
            list[dict]: A list of dictionaries containing the nutrient quantity data.
                [
                    {
                        'ingredient_nutrient_id': int,
                        'nutrient_id': int,
                        'nutrient_mass_unit_id': int,
                        'nutrient_mass_value': float|None,
                        'ingredient_grams_qty': float|None
                    },
                ]
        """
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nutrient_id, ntr_mass_unit_id, ntr_mass_value, ing_grams_qty FROM ingredient_nutrient_quantities WHERE ingredient_id = ?;
                """,
                (ingredient_id,)
            )
            rows = cursor.fetchall()
            return [
                {
                    'id': row[0],
                    'nutrient_id': row[1],
                    'nutrient_mass_unit_id': row[2],
                    'nutrient_mass_value': row[3],
                    'ingredient_grams_qty': row[4]
                }
                for row in rows
            ]
        
    def update_ingredient_nutrient_quantity(
                self,
                ingredient_id: int,
                nutrient_id: int,
                nutrient_mass_unit_id: int,
                nutrient_mass_value: float|None=None,
                ingredient_grams_qty: float|None=None
        ) -> None:
            """Updates a nutrient quantity for an ingredient."""
            with self.get_cursor() as cursor:
    
                cursor.execute(
                    """
                    UPDATE ingredient_nutrient_quantities SET ntr_mass_value = ?, ing_grams_qty = ?, ntr_mass_unit_id = ? WHERE ingredient_id = ? AND nutrient_id = ?;
                    """,
                    (nutrient_mass_value, ingredient_grams_qty, nutrient_mass_unit_id, ingredient_id, nutrient_id),
                )
    
                if cursor.rowcount == 0:
                    raise ValueError(f"No ingredient nutrient quantity found for ingredient_id={ingredient_id} and nutrient_id={nutrient_id}")
                
    def delete_ingredient_nutrient_quantity(
                self,
                ingredient_id: int,
                nutrient_id: int
        ) -> None:
            """Deletes a nutrient quantity for an ingredient."""
            with self.get_cursor() as cursor:
    
                cursor.execute(
                    """
                    DELETE FROM ingredient_nutrient_quantities WHERE ingredient_id = ? AND nutrient_id = ?;
                    """,
                    (ingredient_id, nutrient_id),
                )
    
                if cursor.rowcount == 0:
                    raise ValueError(f"No ingredient nutrient quantity found for ingredient_id={ingredient_id} and nutrient_id={nutrient_id}")