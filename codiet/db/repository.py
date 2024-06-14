"""This module contains the Repository class, which is responsible for interacting with the database.
Since the methods are tightly coupled to the database, the API should be kept as narrow as possible.
"""

import sqlite3

from codiet.exceptions import ingredient_exceptions as ingredient_exceptions


class Repository:
    def __init__(self, db):
        self._db = db

    @property
    def connection(self) -> sqlite3.Connection:
        """Returns the connection to the database."""
        return self._db.connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        """Returns the cursor for the database."""
        return self._db.cursor

    def fetch_flag_id(self, name: str) -> int:
        """Returns the ID of the given flag name."""
        return self._db.execute(
            """
            SELECT flag_id FROM global_flag_list WHERE flag_name = ?;
        """,
            (name,),
        ).fetchone()[0]

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

    def fetch_leaf_nutrient_id_from_name(self, name: str) -> int:
        """Returns the ID of the leaf nutrient associated with the given name."""
        return self._db.execute(
            """
            SELECT nutrient_id FROM global_leaf_nutrients WHERE nutrient_name = ?;
        """,
            (name,),
        ).fetchone()[0]
    
    def fetch_leaf_nutrient_name_from_id(self, id: int) -> str:
        """Returns the name of the leaf nutrient associated with the given ID."""
        return self._db.execute(
            """
            SELECT nutrient_name FROM global_leaf_nutrients WHERE nutrient_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_ingredient_name(self, id: int) -> str:
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

    def fetch_ingredient_description(self, id: int) -> str | None:
        """Returns the description of the ingredient associated with the given ID."""
        return self._db.execute(
            """
            SELECT ingredient_description FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()[0]

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

    def fetch_custom_units_by_ingredient_id(self, ingredient_id: int) -> list[dict]:
        """Returns a list of custom measurements for the given ingredient ID."""
        rows = self._db.execute(
            """
            SELECT custom_unit_id, unit_name, custom_unit_qty, std_unit_qty, std_unit_name
            FROM ingredient_custom_units
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchall()
        return [
            {
                "custom_unit_id": row[0],
                "unit_name": row[1],
                "custom_unit_qty": row[2],
                "std_unit_qty": row[3],
                "std_unit_name": row[4],
            }
            for row in rows
        ]

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

    def fetch_ingredient_gi(self, id: int) -> float | None:
        """Returns the GI of the ingredient associated with the given ID."""
        return self._db.execute(
            """
            SELECT ingredient_gi FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_ingredient_nutrient_quantities(self, ingredient_id: int) -> dict[int, dict]:
        """Returns a dict of nutrients for the given ingredient ID."""
        rows = self._db.execute(
            """
            SELECT nutrient_id, ntr_mass_unit, ntr_mass_value, ing_qty_unit, ing_qty_value
            FROM ingredient_nutrients
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchall()
        return {
            row[0]: {
                "ntr_mass_unit": row[1],
                "ntr_mass_value": row[2],
                "ing_qty_unit": row[3],
                "ing_qty_value": row[4],
            }
            for row in rows
        }

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

    def fetch_recipe_description(self, id: int) -> str | None:
        """Returns the description of the recipe associated with the given ID."""
        return self._db.execute(
            """
            SELECT recipe_description FROM recipe_base WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_recipe_instructions(self, id: int) -> str | None:
        """Returns the instructions of the recipe associated with the given ID."""
        return self._db.execute(
            """
            SELECT recipe_instructions FROM recipe_base WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_recipe_ingredients(self, recipe_id: int) -> dict[int, dict]:
        """Returns the ingredients of the recipe associated with the given ID."""
        rows = self._db.execute(
            """
            SELECT ingredient_id, qty_value, qty_unit, qty_tol_upper, qty_tol_lower
            FROM recipe_ingredients
            WHERE recipe_id = ?;
        """,
            (recipe_id,),
        ).fetchall()
        return {
            row[0]: {
                "qty_value": row[1],
                "qty_unit": row[2],
                "qty_utol": row[3],
                "qty_ltol": row[4],
            }
            for row in rows
        }

    def fetch_recipe_serve_times(self, id: int) -> list[str]:
        """Returns the serve times of the recipe associated with the given ID."""
        rows = self._db.execute(
            """
            SELECT serve_time_window FROM recipe_serve_times WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchall()
        return [row[0] for row in rows]

    def fetch_all_global_recipe_tags(self) -> list[str]:
        """Returns a list of all global recipe tags in the database."""
        rows = self._db.execute(
            """
            SELECT recipe_tag_name FROM global_recipe_tags;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def fetch_recipe_tags_for_recipe(self, recipe_id: int) -> list[str]:
        """Returns a list of all recipe tags for the given recipe ID."""
        rows = self._db.execute(
            """
            SELECT recipe_tag_name
            FROM global_recipe_tags
            JOIN recipe_tags ON global_recipe_tags.recipe_tag_id = recipe_tags.recipe_tag_id
            WHERE recipe_id = ?;
        """,
            (recipe_id,),
        ).fetchall()
        return [row[0] for row in rows]

    def insert_global_flag(self, name: str) -> int:
        """Adds a flag to the global flag table and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO global_flag_list (flag_name) VALUES (?);
        """,
            (name,),
        )
        return cursor.lastrowid

    def insert_global_leaf_nutrient(
        self, name: str, parent_id: int | None = None
    ) -> int:
        """Adds a nutrient to the global leaf nutrient table and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO global_leaf_nutrients (nutrient_name, parent_id) VALUES (?, ?);
            """,
            (name, parent_id),
        )
        return cursor.lastrowid

    def insert_global_group_nutrient(
        self, name: str, parent_id: int | None = None
    ) -> int:
        """Adds a nutrient to the global group nutrient table and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO global_group_nutrients (nutrient_name, parent_id) VALUES (?, ?);
            """,
            (name, parent_id),
        )
        return cursor.lastrowid

    def insert_global_group_nutrient_alias(
        self, alias: str, primary_nutrient_id: int
    ) -> None:
        """Adds an alias into the global group nutrient alias table."""
        self._db.execute(
            """
            INSERT INTO nutrient_alias (nutrient_alias, primary_nutrient_id) VALUES (?, ?);
        """,
            (alias, primary_nutrient_id),
        )

    def insert_global_leaf_nutrient_alias(
        self, alias: str, primary_nutrient_id: int
    ) -> None:
        """Adds an alias into the global leaf nutrient alias table."""
        self._db.execute(
            """
            INSERT INTO nutrient_alias (nutrient_alias, primary_nutrient_id) VALUES (?, ?);
        """,
            (alias, primary_nutrient_id),
        )

    def insert_ingredient_name(self, name: str) -> int:
        """Adds an ingredient name to the database and returns the ID."""
        cost_unit = "GBP" # NOTE: One day if we want to support other currencies, this will need to be a parameter.
        try:
            cursor = self._db.execute(
                """
                INSERT INTO ingredient_base (ingredient_name, cost_unit) VALUES (?, ?);
                """,
                (name, cost_unit),
            )
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ingredient_exceptions.IngredientNameExistsError(name)
            else:
                raise e

    def insert_custom_unit(
        self,
        ingredient_id: int,
        unit_name: str,
    ) -> int:
        """Adds a custom measurement to the database and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO ingredient_custom_units (ingredient_id, unit_name) VALUES (?, ?);
        """,
            (ingredient_id, unit_name),
        )
        return cursor.lastrowid

    def insert_ingredient_nutrient_quantity(self, ingredient_id: int, nutrient_id:int) -> None:
        """Adds a nutrient quantity to the ingredient."""
        self._db.execute(
            """
            INSERT INTO ingredient_nutrients (ingredient_id, nutrient_id) VALUES (?, ?);
        """,
            (ingredient_id, nutrient_id),
        )

    def insert_recipe_name(self, name: str) -> int:
        """Adds a recipe name to the database and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO recipe_base (recipe_name) VALUES (?);
        """,
            (name,),
        )
        return cursor.lastrowid

    def insert_global_recipe_tag(self, name: str) -> int:
        """Adds a recipe tag to the global recipe tag table and returns the ID."""
        cursor = self._db.execute(
            """
            INSERT INTO global_recipe_tags (recipe_tag_name) VALUES (?);
        """,
            (name,),
        )
        return cursor.lastrowid

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

    def update_ingredient_cost(
        self,
        ingredient_id: int,
        cost_value: float | None,
        cost_unit: str,
        cost_qty_unit: str | None,
        cost_qty_value: float | None,
    ) -> None:
        """Updates the cost data of the ingredient associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_base
            SET cost_value = ?, cost_unit = ?, cost_qty_unit = ?, cost_qty_value = ?
            WHERE ingredient_id = ?;
        """,
            (cost_value, cost_unit, cost_qty_unit, cost_qty_value, ingredient_id),
        )

    def update_custom_measurement(
        self,
        unit_id: int,
        custom_unit_qty: float | None,
        std_unit_qty: float | None,
        std_unit_name: str,
    ) -> None:
        """Updates the custom measurement associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_custom_units
            SET custom_unit_qty = ?, std_unit_qty = ?, std_unit_name = ?
            WHERE custom_unit_id = ?;
        """,
            (custom_unit_qty, std_unit_qty, std_unit_name, unit_id),
        )

    def update_ingredient_flag(self, ingredient_id: int, flag: str, value: bool) -> None:
        """Updates the flag for the ingredient associated with the given ID."""
        # Get the flag ID
        flag_id = self.fetch_flag_id(flag)
        # Clear the existing flag
        self._db.execute(
            """
            DELETE FROM ingredient_flags WHERE ingredient_id = ? AND flag_id = ?;
        """,
            (ingredient_id, flag_id),
        )
        # Add the new flag
        self._db.execute(
            """
            INSERT INTO ingredient_flags (ingredient_id, flag_id, flag_value) VALUES (?, ?, ?);
        """,
            (ingredient_id, flag_id, value),
        )

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

    def update_ingredient_nutrient_quantity(
        self,
        ingredient_id: int,
        global_nutrient_id: int,
        ntr_mass_unit: str,
        ntr_mass_value: float | None,
        ing_qty_unit: str,
        ing_qty_value: float | None,
    ) -> None:
        """Updates the nutrient quantity of the ingredient associated with the given ID."""
        self._db.execute(
            """
            UPDATE ingredient_nutrients
            SET ntr_mass_unit = ?, ntr_mass_value = ?, ing_qty_unit = ?, ing_qty_value = ?
            WHERE ingredient_id = ? AND nutrient_id = ?;
        """,
            (ntr_mass_unit, ntr_mass_value, ing_qty_unit, ing_qty_value, ingredient_id, global_nutrient_id),
        )

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

    def update_recipe_description(
        self, recipe_id: int, description: str | None
    ) -> None:
        """Updates the description of the recipe associated with the given ID."""
        self._db.execute(
            """
            UPDATE recipe_base
            SET recipe_description = ?
            WHERE recipe_id = ?;
        """,
            (description, recipe_id),
        )

    def update_recipe_instructions(
        self, recipe_id: int, instructions: str | None
    ) -> None:
        """Updates the instructions of the recipe associated with the given ID."""
        self._db.execute(
            """
            UPDATE recipe_base
            SET recipe_instructions = ?
            WHERE recipe_id = ?;
        """,
            (instructions, recipe_id),
        )

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
        for ingredient_id, data in ingredients.items():
            # Add the ingredient
            self._db.execute(
                """
                INSERT INTO recipe_ingredients (recipe_id, ingredient_id, qty_value, qty_unit, qty_tol_upper, qty_tol_lower)
                VALUES (?, ?, ?, ?, ?, ?);
            """,
                (
                    recipe_id,
                    ingredient_id,
                    data["qty_value"],
                    data["qty_unit"],
                    data["qty_utol"],
                    data["qty_ltol"],
                ),
            )

    def update_recipe_serve_times(self, recipe_id: int, serve_times: list[str]) -> None:
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

    def update_recipe_tags(self, recipe_id: int, recipe_tags: list[str]) -> None:
        """Updates the recipe tags of the recipe associated with the given ID."""
        # Clear the existing recipe tags
        self._db.execute(
            """
            DELETE FROM recipe_tags WHERE recipe_id = ?;
        """,
            (recipe_id,),
        )
        # Add the new recipe tags
        for tag in recipe_tags:
            # Get the tag ID
            tag_id = self._db.execute(
                """
                SELECT recipe_tag_id FROM global_recipe_tags WHERE recipe_tag_name = ?;
            """,
                (tag,),
            ).fetchone()[0]
            # Add the tag
            self._db.execute(
                """
                INSERT INTO recipe_tags (recipe_id, recipe_tag_id)
                VALUES (?, ?);
            """,
                (recipe_id, tag_id),
            )

    def delete_ingredient_by_name(self, ingredient_name: str) -> None:
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

    def delete_custom_unit(self, measurement_id:int) -> None:
        """Deletes the given custom measurement from the database."""
        self._db.execute(
            """
            DELETE FROM ingredient_custom_units
            WHERE custom_unit_id = ?;
            """,
            (measurement_id,),
        )

    def delete_recipe_by_name(self, recipe_name: str) -> None:
        """Deletes the given recipe from the database."""
        # Grab the ID of the recipe
        recipe_id = self.fetch_recipe_id(recipe_name)

        # Remove all entries against the ID from all recipe tables.
        queries = [
            """
            DELETE FROM recipe_base
            WHERE recipe_id = ?;
            """,
            """
            DELETE FROM recipe_ingredients
            WHERE recipe_id = ?;
            """,
            """
            DELETE FROM recipe_serve_times
            WHERE recipe_id = ?;
            """,
            """
            DELETE FROM recipe_tags
            WHERE recipe_id = ?;
            """,
        ]
        try:
            for query in queries:
                self._db.execute(query, (recipe_id,))
                self._db.commit()
        except Exception as e:
            self._db.connection.rollback()
            raise e
