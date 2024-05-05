import sqlite3

from codiet.exceptions import ingredient_exceptions as ingredient_exceptions

class Repository:
    def __init__(self, db):
        self._db = db

    def fetch_flag_id(self, name: str) -> int:
        """Returns the ID of the given flag name."""
        return self._db.execute(
            """
            SELECT flag_id FROM global_flag_list WHERE flag_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def insert_global_flag(self, name: str) -> int:
        """Adds a flag to the global flag table and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO global_flag_list (flag_name) VALUES (?);
        """,
            (name,),
        )
        return cursor.lastrowid

    def fetch_all_global_flag_names(self) -> list[str]:
        """Returns a list of all global flags in the database."""
        rows = self._db.execute(
            """
            SELECT flag_name FROM global_flag_list;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def fetch_all_group_nutrient_names(self) -> list[str]:
        """Returns all of the group nutrient (primary - not aliases) names in the database."""
        rows = self._db.execute(
            """
            SELECT nutrient_name FROM global_group_nutrients;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def fetch_all_leaf_nutrient_names(self) -> list[str]:
        """Returns all of the leaf nutrient (primary - not aliases) names in the database."""
        rows = self._db.execute(
            """
            SELECT nutrient_name FROM global_leaf_nutrients;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def insert_global_leaf_nutrient(self, name: str, parent_id: int | None = None) -> int:
        """Adds a nutrient to the global leaf nutrient table and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO global_leaf_nutrients (nutrient_name, parent_id) VALUES (?, ?);
            """,
            (name, parent_id),
        )
        return cursor.lastrowid

    def insert_global_group_nutrient(self, name: str, parent_id: int | None = None) -> int:
        """Adds a nutrient to the global group nutrient table and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO global_group_nutrients (nutrient_name, parent_id) VALUES (?, ?);
            """,
            (name, parent_id),
        )
        return cursor.lastrowid

    def insert_global_group_nutrient_alias(self, alias: str, primary_nutrient_id: int) -> None:
        """Adds an alias into the global group nutrient alias table."""
        self._db.execute(
            """
            INSERT INTO nutrient_alias (nutrient_alias, primary_nutrient_id) VALUES (?, ?);
        """,
            (alias, primary_nutrient_id),
        )

    def insert_global_leaf_nutrient_alias(self, alias: str, primary_nutrient_id: int) -> None:
        """Adds an alias into the global leaf nutrient alias table."""
        self._db.execute(
            """
            INSERT INTO nutrient_alias (nutrient_alias, primary_nutrient_id) VALUES (?, ?);
        """,
            (alias, primary_nutrient_id),
        )

    def fetch_ingredient_name(self, id:int) -> str:
        """Returns the name of the ingredient associated with the given ID."""
        return self._db.execute(
            """
            SELECT ingredient_name FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_ingredient_id_by_name(self, name: str) -> int:
        """Returns the ID of the ingredient associated with the given name."""
        return self._db.execute(
            """
            SELECT ingredient_id FROM ingredient_base WHERE ingredient_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def fetch_all_ingredient_names(self) -> list[str]:
        """Returns a list of all the ingredient names in the database."""
        rows = self._db.execute(
            """
            SELECT ingredient_name FROM ingredient_base;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def insert_ingredient_name(self, name: str) -> None:
        """Adds an ingredient name to the database."""
        try:
            self._db.execute(
                """
                INSERT INTO ingredient_base (ingredient_name) VALUES (?);
            """,
                (name,),
            )
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ingredient_exceptions.IngredientNameExistsError(name)
            else:
                raise e

    def update_ingredient_name(self, ingredient_id: int, name: str) -> None:
        """Updates the name of the ingredient associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_base
            SET ingredient_name = ?
            WHERE ingredient_id = ?;
        """,
            (name, ingredient_id),
        )

    def fetch_ingredient_description(self, id: int) -> str | None:
        """Returns the description of the ingredient associated with the given ID."""
        return self._db.execute(
            """
            SELECT ingredient_description FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def update_ingredient_description(
        self, ingredient_id: int, description: str | None
    ) -> None:
        """Updates the description of the ingredient associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_base
            SET ingredient_description = ?
            WHERE ingredient_id = ?;
            """,
            (description, ingredient_id),
        )

    def fetch_ingredient_cost(self, id: int) -> tuple[float | None, str, float | None]:
        """Returns the cost data of the ingredient associated with the given ID."""
        return self._db.execute(
            """
            SELECT cost_value, cost_qty_unit, cost_qty_value
            FROM ingredient_base
            WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()

    def update_ingredient_cost(
        self,
        ingredient_id: int,
        cost_value: float | None,
        cost_unit: str | None,
        qty_unit: str | None,
        qty_value: float | None,
    ) -> None:
        """Updates the cost data of the ingredient associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_base
            SET cost_value = ?, cost_unit = ?, cost_qty_unit = ?, cost_qty_value = ?
            WHERE ingredient_id = ?;
        """,
            (cost_value, cost_unit, qty_unit, qty_value, ingredient_id),
        )

    def fetch_ingredient_density(self, id: int) -> tuple[str, float | None, str, float | None]:
        """Returns the density data of the ingredient associated with the given ID."""
        return self._db.execute(
            """
            SELECT density_mass_unit, density_mass_value, density_vol_unit, density_vol_value
            FROM ingredient_base
            WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()

    def update_ingredient_density(
        self,
        ingredient_id: int,
        dens_mass_unit: str,
        dens_mass_value: float | None,
        dens_vol_unit: str,
        dens_vol_value: float | None,
    ) -> None:
        """Updates the density data of the ingredient associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_base
            SET density_mass_unit = ?, density_mass_value = ?, density_vol_unit = ?, density_vol_value = ?
            WHERE ingredient_id = ?;
        """,
            (
                dens_mass_unit,
                dens_mass_value,
                dens_vol_unit,
                dens_vol_value,
                ingredient_id,
            ),
        )

    def fetch_ingredient_pc_mass(self, id: int) -> tuple[float | None, str, float | None]:
        """Returns the piece mass data of the ingredient associated with the given ID."""
        return self._db.execute(
            """
            SELECT pc_qty, pc_mass_unit, pc_mass_value
            FROM ingredient_base
            WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()

    def update_ingredient_pc_mass(
        self,
        ingredient_id: int,
        pc_qty: float | None,
        pc_mass_unit: str | None,
        pc_mass_value: float | None,
    ) -> None:
        """Updates the piece mass data of the ingredient associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_base
            SET pc_qty = ?, pc_mass_unit = ?, pc_mass_value = ?
            WHERE ingredient_id = ?;
        """,
            (pc_qty, pc_mass_unit, pc_mass_value, ingredient_id),
        )

    def fetch_ingredient_flags(self, id: int) -> dict[str, int]:
        """Returns the flags of the ingredient associated with the given ID.
        SQLite stores flags as integers, where 0 is False and 1 is True.
        """
        rows = self._db.execute(
            """
            SELECT flag_name, flag_value
            FROM global_flag_list
            JOIN ingredient_flags ON global_flag_list.flag_id = ingredient_flags.flag_id
            WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchall()
        return {row[0]: row[1] for row in rows}

    def update_ingredient_flags(
        self, ingredient_id: int, flags: dict[str, bool]
    ) -> None:
        """Updates the flags for the ingredient associated with the given ID."""
        # Clear the existing flags
        self._db.execute(
            """
            DELETE FROM ingredient_flags WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        )
        # Add the new flags
        for flag, value in flags.items():
            flag_id = self.fetch_flag_id(flag)
            self._db.execute(
                """
                INSERT INTO ingredient_flags (ingredient_id, flag_id, flag_value) VALUES (?, ?, ?);
            """,
                (ingredient_id, flag_id, value),
            )

    def fetch_ingredient_gi(self, id: int) -> float | None:
        """Returns the GI of the ingredient associated with the given ID."""
        return self._db.execute(
            """
            SELECT ingredient_gi FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def update_ingredient_gi(self, ingredient_id: int, gi: float | None) -> None:
        """Updates the GI of the ingredient associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_base
            SET ingredient_gi = ?
            WHERE ingredient_id = ?;
        """,
            (gi, ingredient_id),
        )

    def update_ingredient_nutrients(
        self,
        ingredient_id: int,
        nutrients: dict[str, dict],
    ) -> None:
        """Updates the nutrients of the ingredient associated with the given ID."""
        # Clear the existing nutrients
        self._db.execute(
            """
            DELETE FROM ingredient_nutrients WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        )
        # Add the new nutrients
        for nutrient, data in nutrients.items():
            # Get the nutrient ID
            nutrient_id = self._db.execute(
                """
                SELECT nutrient_id FROM global_leaf_nutrients WHERE nutrient_name = ?;
            """,
                (nutrient,),
            ).fetchone()[0]
            # Add the nutrient
            self._db.execute(
                """
                INSERT INTO ingredient_nutrients (ingredient_id, nutrient_id, ntr_qty_unit, ntr_qty_value, ing_qty_unit, ing_qty_value)
                VALUES (?, ?, ?, ?, ?, ?);
            """,
                (
                    ingredient_id,
                    nutrient_id,
                    data["ntr_qty_unit"],
                    data["ntr_qty_value"],
                    data["ing_qty_unit"],
                    data["ing_qty_value"],
                ),
            )

    def fetch_ingredient_nutrients(
        self, ingredient_id: int
    ) -> dict[str, dict]:
        """Returns a dict of nutrients for the given ingredient ID."""
        rows = self._db.execute(
            """
            SELECT nutrient_name, ntr_qty_unit, ntr_qty_value, ing_qty_unit, ing_qty_value
            FROM global_leaf_nutrients
            JOIN ingredient_nutrients ON global_leaf_nutrients.nutrient_id = ingredient_nutrients.nutrient_id
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchall()
        return {
            row[0]: {
                "ntr_qty_unit": row[1],
                "ntr_qty_value": row[2],
                "ing_qty_unit": row[3],
                "ing_qty_value": row[4],
            }
            for row in rows
        }

    def delete_ingredient(self, ingredient_name: str) -> None:
        """Deletes the given ingredient from the database."""
        # Grab the ID of the ingredient
        ingredient_id = self.fetch_ingredient_id_by_name(ingredient_name)

        # Remove all entries against the ID from all ingredient tables.
        queries = [
            """
            DELETE FROM ingredient_base
            WHERE ingredient_id = ?;
            """,
            """
            DELETE FROM ingredient_nutrients
            WHERE ingredient_id = ?;
            """,
            """
            DELETE FROM ingredient_flags
            WHERE ingredient_id = ?;
            """,
        ]
        try:
            for query in queries:
                self._db.execute(query, (ingredient_id,))
                self._db.commit()
        except Exception as e:
            self._db.connection.rollback()
            raise e
        
    def insert_recipe_name(self, name: str) -> int:
        """Adds a recipe name to the database and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO recipe_base (recipe_name) VALUES (?);
        """,
            (name,),
        )
        return cursor.lastrowid
    
    def fetch_recipe_name(self, id: int) -> str:
        """Returns the name of the recipe associated with the given ID."""
        return self._db.execute(
            """
            SELECT recipe_name FROM recipe_base WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_recipe_id(self, name: str) -> int:
        """Returns the ID of the recipe associated with the given name."""
        return self._db.execute(
            """
            SELECT recipe_id FROM recipe_base WHERE recipe_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def fetch_all_recipe_names(self) -> list[str]:
        """Returns a list of all the recipe names in the database."""
        rows = self._db.execute(
            """
            SELECT recipe_name FROM recipe_base;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def update_recipe_name(self, recipe_id: int, name: str) -> None:
        """Updates the name of the recipe associated with the given ID."""
        self._db.execute(
            """
            UPDATE recipe_base
            SET recipe_name = ?
            WHERE recipe_id = ?;
        """,
            (name, recipe_id),
        )

    def fetch_recipe_description(self, id: int) -> str | None:
        """Returns the description of the recipe associated with the given ID."""
        return self._db.execute(
            """
            SELECT recipe_description FROM recipe_base WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def update_recipe_description(self, recipe_id: int, description: str | None) -> None:
        """Updates the description of the recipe associated with the given ID."""
        self._db.execute(
            """
            UPDATE recipe_base
            SET recipe_description = ?
            WHERE recipe_id = ?;
        """,
            (description, recipe_id),
        )

    def fetch_recipe_instructions(self, id: int) -> str | None:
        """Returns the instructions of the recipe associated with the given ID."""
        return self._db.execute(
            """
            SELECT recipe_instructions FROM recipe_base WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def update_recipe_instructions(self, recipe_id: int, instructions: str | None) -> None:
        """Updates the instructions of the recipe associated with the given ID."""
        self._db.execute(
            """
            UPDATE recipe_base
            SET recipe_instructions = ?
            WHERE recipe_id = ?;
        """,
            (instructions, recipe_id),
        )

    def fetch_recipe_ingredients(self, id: int) -> dict[str, dict]:
        """Returns the ingredients of the recipe associated with the given ID."""
        rows = self._db.execute(
            """
            SELECT ingredient_name, qty, qty_unit, qty_utol, qty_ltol
            FROM ingredient_base
            JOIN recipe_ingredients ON ingredient_base.ingredient_id = recipe_ingredients.ingredient_id
            WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchall()
        return {
            row[0]: {
                "qty": row[1],
                "qty_unit": row[2],
                "qty_utol": row[3],
                "qty_ltol": row[4],
            }
            for row in rows
        }

    def update_recipe_ingredients(
        self, recipe_id: int, ingredients: dict[str, dict]
    ) -> None:
        """Updates the ingredients of the recipe associated with the given ID."""
        # Clear the existing ingredients
        self._db.execute(
            """
            DELETE FROM recipe_ingredients WHERE recipe_id = ?;
        """,
            (recipe_id,),
        )
        # Add the new ingredients
        for ingredient, data in ingredients.items():
            # Get the ingredient ID from the name
            ingredient_id = self._db.execute(
                """
                SELECT ingredient_id FROM ingredient_base WHERE ingredient_name = ?;
            """,
                (ingredient,),
            ).fetchone()[0]
            # Add the ingredient
            self._db.execute(
                """
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id, qty, qty_unit, qty_utol, qty_ltol)
                VALUES (?, ?, ?, ?, ?, ?);
            """,
                (
                    recipe_id,
                    ingredient_id,
                    data["qty"],
                    data["qty_unit"],
                    data["qty_utol"],
                    data["qty_ltol"],
                ),
            )

    def fetch_recipe_serve_times(self, id: int) -> list[str]:
        """Returns the serve times of the recipe associated with the given ID."""
        rows = self._db.execute(
            """
            SELECT serve_time_window FROM recipe_serve_times WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchall()
        return [row[0] for row in rows]

    def update_recipe_serve_times(
        self, recipe_id: int, serve_times: list[str]
    ) -> None:
        """Updates the serve times of the recipe associated with the given ID."""
        # Clear the existing serve times
        self._db.execute(
            """
            DELETE FROM recipe_serve_times WHERE recipe_id = ?;
        """,
            (recipe_id,),
        )
        # Add the new serve times
        for serve_time in serve_times:
            # Add the serve time
            self._db.execute(
                """
                INSERT INTO recipe_serve_times (recipe_id, serve_time_window)
                VALUES (?, ?);
            """,
                (recipe_id, serve_time),
            )

    def update_recipe_types(
        self, recipe_id: int, recipe_types: list[str]
    ) -> None:
        """Updates the recipe types of the recipe associated with the given ID."""
        # Clear the existing recipe types
        self._db.execute(
            """
            DELETE FROM recipe_types WHERE recipe_id = ?;
        """,
            (recipe_id,),
        )
        # Add the new recipe types
        for recipe_type in recipe_types:
            # Add the recipe type
            self._db.execute(
                """
                INSERT INTO recipe_types (recipe_id, recipe_type)
                VALUES (?, ?);
            """,
                (recipe_id, recipe_type),
            )

    def insert_global_recipe_type(self, name: str) -> int:
        """Adds a recipe type to the global recipe type table and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO global_recipe_types (recipe_type_name) VALUES (?);
        """,
            (name,),
        )
        return cursor.lastrowid
    
    def fetch_all_global_recipe_types(self) -> list[str]:
        """Returns a list of all global recipe types in the database."""
        rows = self._db.execute(
            """
            SELECT recipe_type_name FROM global_recipe_types;
        """
        ).fetchall()
        return [row[0] for row in rows]
    
    def fetch_recipe_types_for_recipe(self, recipe_id: int) -> list[str]:
        """Returns a list of all recipe types for the given recipe ID."""
        rows = self._db.execute(
            """
            SELECT recipe_type_name
            FROM global_recipe_types
            JOIN recipe_types ON global_recipe_types.recipe_type_id = recipe_types.recipe_type_id
            WHERE recipe_id = ?;
        """,
            (recipe_id,),
        ).fetchall()
        return [row[0] for row in rows]