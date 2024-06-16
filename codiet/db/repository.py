"""
This module contains the Repository class, which is responsible for interacting with the database.
Since the methods are tightly coupled to the database, the API should be kept as narrow as possible.
"""

import sqlite3
from typing import Generator
from contextlib import contextmanager

from codiet.db.database import Database
from codiet.exceptions import ingredient_exceptions as ingredient_exceptions


class Repository:
    def __init__(self, database: Database):
        self.database = database

    @property
    def connection(self) -> sqlite3.Connection:
        """Return a connection to the database."""
        return self.database.connection

    def close_connection(self) -> None:
        """Close the connection to the database."""
        self.database.connection.close()

    @contextmanager
    def get_cursor(self) -> Generator[sqlite3.Cursor, None, None]:
        """Return a cursor for the database connection."""
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def insert_global_unit(
        self, 
        unit_name: str, 
        plural_name: str, 
        unit_type: str,
        aliases: list[str]|None = None,
        conversions: dict[int, float]|None = None
    ) -> int:
        """Adds a unit to the global unit table and returns the ID."""
        # Add the global unit to the base table
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO global_units (unit_name, plural_name, unit_type) VALUES (?, ?, ?);
            """,
                (unit_name, plural_name, unit_type),
            )
            # Get the ID of the unit
            id = cursor.lastrowid
        assert id is not None
        # Add any aliases
        if aliases:
            for alias in aliases:
                self.insert_global_unit_alias(alias=alias, parent_id=id)
        # Add any conversions
        if conversions:
            for to_unit_id, conversion_factor in conversions.items():
                self.insert_global_unit_conversion(from_unit_id=id, to_unit_id=to_unit_id, conversion_factor=conversion_factor)
        return id

    def insert_global_unit_alias(self, alias: str, parent_id: int) -> int:
        """Adds an alias to the global unit alias table and returns the ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO global_unit_aliases (alias, primary_unit_id) VALUES (?, ?);
            """,
                (alias, parent_id),
            )
            id = cursor.lastrowid
        assert id is not None
        return id

    def insert_global_unit_conversion(self, from_unit_id: int, to_unit_id: int, conversion_factor: float) -> int:
        """Adds a conversion to the global unit conversion table and returns the ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO global_unit_conversions (from_unit_id, to_unit_id, conversion_factor) VALUES (?, ?, ?);
            """,
                (from_unit_id, to_unit_id, conversion_factor),
            )
            id = cursor.lastrowid
        assert id is not None
        return id

    def insert_global_flag(self, flag_name: str) -> int:
        """Adds a flag to the global flag table and returns the ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO global_flags (flag_name) VALUES (?);
            """,
                (flag_name,),
            )
            assert cursor.lastrowid is not None
            return cursor.lastrowid

    def insert_global_nutrient(
        self, name: str, parent_id: int | None = None
    ) -> int:
        """Adds a nutrient to the global leaf nutrient table and returns the ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO global_nutrients (nutrient_name, parent_id) VALUES (?, ?);
                """,
                (name, parent_id),
            )
            id = cursor.lastrowid
        assert id is not None
        return id

    def insert_nutrient_alias(
        self, alias: str, primary_nutrient_id: int
    ) -> None:
        """Adds an alias into the global group nutrient alias table."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO nutrient_aliases (nutrient_alias, primary_nutrient_id) VALUES (?, ?);
            """,
                (alias, primary_nutrient_id),
            )

    def insert_ingredient_name(self, name: str) -> int:
        """Adds an ingredient name to the database and returns the ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ingredients (ingredient_name) VALUES (?);
            """,
                (name,),
            )
            id = cursor.lastrowid
        assert id is not None 
        return id

    def insert_ingredient_nutrient_quantity(
        self, ingredient_id: int, nutrient_id: int
    ) -> None:
        """Adds a nutrient quantity to the ingredient."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ingredient_nutrients (ingredient_id, nutrient_id) VALUES (?, ?);
            """,
                (ingredient_id, nutrient_id),
            )

    def insert_recipe_name(self, name: str) -> int:
        """Adds a recipe name to the database and returns the ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO recipes (recipe_name) VALUES (?);
            """,
                (name,),
            )
            id = cursor.lastrowid
        assert id is not None
        return id

    def insert_global_recipe_tag(self, tag_name: str) -> int:
        """Adds a recipe tag to the global recipe tag table and returns the ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO global_recipe_tags (recipe_tag_name) VALUES (?);
            """,
                (tag_name,),
            )
            id = cursor.lastrowid
        assert id is not None
        return id

    def update_ingredient_name(self, ingredient_id: int, name: str) -> None:
        """Updates the name of the ingredient associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingredients
                SET ingredient_name = ?
                WHERE id = ?;
            """,
                (name, ingredient_id),
            )

    def update_ingredient_description(
        self, ingredient_id: int, description: str | None
    ) -> None:
        """Updates the description of the ingredient associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingredients
                SET ingredient_description = ?
                WHERE id = ?;
                """,
                (description, ingredient_id),
            )

    def update_ingredient_cost(
        self,
        ingredient_id: int,
        cost_value: float | None,
        cost_qty_unit: str | None,
        cost_qty_value: float | None,
    ) -> None:
        cost_unit = "GBP" # Hardcoded for now
        """Updates the cost data of the ingredient associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingredients
                SET cost_value = ?, cost_qty_unit = ?, cost_qty_value = ?
                WHERE id = ?;
            """,
                (cost_value, cost_qty_unit, cost_qty_value, ingredient_id),
            )

    def update_ingredient_flag(
        self, ingredient_id: int, flag_id: int, value: bool|None
    ) -> None:
        """Update (or insert if not exists) the flag for the ingredient associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT OR REPLACE INTO ingredient_flags (ingredient_id, flag_id, flag_value)
                VALUES (?, ?, ?);
            """,
                (ingredient_id, flag_id, value),
            )

    def update_ingredient_gi(self, ingredient_id: int, gi: float | None) -> None:
        """Updates the GI of the ingredient associated with the given ID."""
        self.database.execute(
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
        self.database.execute(
            """
            UPDATE ingredient_nutrients
            SET ntr_mass_unit = ?, ntr_mass_value = ?, ing_qty_unit = ?, ing_qty_value = ?
            WHERE ingredient_id = ? AND nutrient_id = ?;
        """,
            (
                ntr_mass_unit,
                ntr_mass_value,
                ing_qty_unit,
                ing_qty_value,
                ingredient_id,
                global_nutrient_id,
            ),
        )

    def update_recipe_name(self, recipe_id: int, name: str) -> None:
        """Updates the name of the recipe associated with the given ID."""
        self.database.execute(
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
        self.database.execute(
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
        self.database.execute(
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
        self.database.execute(
            """
            DELETE FROM recipe_ingredients WHERE recipe_id = ?;
        """,
            (recipe_id,),
        )
        # Add the new ingredients
        for ingredient_id, data in ingredients.items():
            # Add the ingredient
            self.database.execute(
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
        self.database.execute(
            """
            DELETE FROM recipe_serve_times WHERE recipe_id = ?;
        """,
            (recipe_id,),
        )
        # Add the new serve times
        for serve_time in serve_times:
            # Add the serve time
            self.database.execute(
                """
                INSERT INTO recipe_serve_times (recipe_id, serve_time_window)
                VALUES (?, ?);
            """,
                (recipe_id, serve_time),
            )

    def update_recipe_tags(self, recipe_id: int, recipe_tags: list[str]) -> None:
        """Updates the recipe tags of the recipe associated with the given ID."""
        # Clear the existing recipe tags
        self.database.execute(
            """
            DELETE FROM recipe_tags WHERE recipe_id = ?;
        """,
            (recipe_id,),
        )
        # Add the new recipe tags
        for tag in recipe_tags:
            # Get the tag ID
            tag_id = self.database.execute(
                """
                SELECT recipe_tag_id FROM global_recipe_tags WHERE recipe_tag_name = ?;
            """,
                (tag,),
            ).fetchone()[0]
            # Add the tag
            self.database.execute(
                """
                INSERT INTO recipe_tags (recipe_id, recipe_tag_id)
                VALUES (?, ?);
            """,
                (recipe_id, tag_id),
            )

    def fetch_all_global_units(self) -> dict[int, dict]:
        """Returns a dictionary of all global units in the database."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, unit_name, plural_name, unit_type FROM global_units;
            """
            ).fetchall()
        return {
            row[0]: {
                "unit_name": row[1],
                "plural_name": row[2],
                "unit_type": row[3],
                "aliases": self.fetch_global_unit_aliases(row[0]),
                "conversions": self.fetch_global_unit_conversions(row[0]),
            }
            for row in rows
        }
    
    def fetch_global_unit_aliases(self, unit_id: int) -> list[str]:
        """Returns a list of aliases for the given global unit ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT alias FROM global_unit_aliases WHERE primary_unit_id = ?;
            """,
                (unit_id,),
            ).fetchall()
        return [row[0] for row in rows]
    
    def fetch_global_unit_conversions(self, unit_id: int) -> dict[int, float]:
        """Returns a dictionary of conversions for the given global unit ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT to_unit_id, conversion_factor FROM global_unit_conversions WHERE from_unit_id = ?;
            """,
                (unit_id,),
            ).fetchall()
        return {row[0]: row[1] for row in rows}

    def fetch_all_global_unit_names(self) -> list[str]:
        """Returns a list of all global units in the database."""
        rows = self.database.execute(
            """
            SELECT unit_name FROM global_units;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def fetch_flag_id(self, name: str) -> int:
        """Returns the ID of the given flag name."""
        return self.database.execute(
            """
            SELECT flag_id FROM global_flag_list WHERE flag_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def fetch_all_global_flags(self) -> list[str]:
        """Returns a list of all global flags in the database."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT flag_name FROM global_flags;
            """
            ).fetchall()
            return [row[0] for row in rows]

    def fetch_all_global_nutrients(self) -> dict[int, dict]:
        """
        Retrieve all group nutrient names from the database.
    
        This method returns a dictionary where each key is a nutrient ID and the value is another dictionary with the following structure:
        {
            'nutrient_name': str,
            'aliases': list[str],
            'parent_id': int | None
        }
    
        Note:
            The nutrient names returned are primary names, not aliases.
    
        Returns:
            dict: A dictionary mapping nutrient IDs to their respective details.
        """
        with self.get_cursor() as cursor:
            base_rows = cursor.execute(
                """
                SELECT id, nutrient_name, parent_id FROM global_nutrients;
            """
            ).fetchall()
            alias_rows = cursor.execute(
                """
                SELECT primary_nutrient_id, nutrient_alias FROM nutrient_aliases;
            """
            ).fetchall()
        aliases = {row[0]: row[1] for row in alias_rows}
        return {
            row[0]: {
                "nutrient_name": row[1],
                "aliases": [aliases.get(row[0])] if aliases.get(row[0]) else [],
                "parent_id": row[2],
            }
            for row in base_rows
        }

    def fetch_ingredient_name(self, id: int) -> str:
        """Returns the name of the ingredient associated with the given ID."""
        return self.database.execute(
            """
            SELECT ingredient_name FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_ingredient_id_by_name(self, name: str) -> int:
        """Returns the ID of the ingredient associated with the given name."""
        return self.database.execute(
            """
            SELECT ingredient_id FROM ingredient_base WHERE ingredient_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def fetch_all_ingredient_names(self) -> list[str]:
        """Returns a list of all the ingredient names in the database."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT ingredient_name FROM ingredients;
            """
            ).fetchall()
        return [row[0] for row in rows]

    def fetch_ingredient_description(self, id: int) -> str | None:
        """Returns the description of the ingredient associated with the given ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT ingredient_description FROM ingredients WHERE id = ?;
            """,
                (id,),
            ).fetchall()
        return rows[0][0] if rows else None

    def fetch_ingredient_cost(self, id: int) -> dict:
        """
        Return the cost data of the ingredient associated with the given ID.

        The data structure returned is a dictionary:
        {
            'cost_value': float | None,
            'cost_qty_unit': str,
            'cost_qty_value': float | None
        }

        Parameters:
        id (int): The ID of the ingredient.

        Returns:
        dict: A dictionary containing the cost data of the ingredient.
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT cost_value, cost_qty_unit, cost_qty_value
                FROM ingredients
                WHERE id = ?;
            """,
                (id,),
            ).fetchall()
        return {
            "cost_value": rows[0][0],
            "cost_qty_unit": rows[0][1],
            "cost_qty_value": rows[0][2],
        }

    def fetch_custom_units_by_ingredient_id(self, ingredient_id: int) -> list[dict]:
        """Returns a list of custom measurements for the given ingredient ID."""
        rows = self.database.execute(
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

    def fetch_ingredient_flags(self, ingredient_id: int) -> dict[int, bool|None]:
        """
        Return the flags of the ingredient associated with the given ingredient ID.
    
        SQLite stores flags as integers, where 0 is False and 1 is True.
        The data structure returned is a dictionary:
        {
            flag_id: flag_value
        }
    
        Args:
            id (int): The ID of the ingredient.
    
        Returns:
            dict: A dictionary mapping flag IDs to their values.
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT flag_id, flag_value FROM ingredient_flags WHERE ingredient_id = ?;
            """,
                (ingredient_id,),
            ).fetchall()
        result = {}
        for row in rows:
            if row[1] is None:
                result[row[0]] = None
            else:
                result[row[0]] = bool(row[1])
        return result

    def fetch_ingredient_gi(self, id: int) -> float | None:
        """Returns the GI of the ingredient associated with the given ID."""
        return self.database.execute(
            """
            SELECT ingredient_gi FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_ingredient_nutrient_quantities(
        self, ingredient_id: int
    ) -> dict[int, dict]:
        """Returns a dict of nutrients for the given ingredient ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
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
        return self.database.execute(
            """
            SELECT recipe_name FROM recipe_base WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_recipe_id(self, name: str) -> int:
        """Returns the ID of the recipe associated with the given name."""
        return self.database.execute(
            """
            SELECT recipe_id FROM recipe_base WHERE recipe_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def fetch_all_recipe_names(self) -> list[str]:
        """Returns a list of all the recipe names in the database."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT recipe_name FROM recipes;
            """
            ).fetchall()
        return [row[0] for row in rows]

    def fetch_recipe_description(self, id: int) -> str | None:
        """Returns the description of the recipe associated with the given ID."""
        return self.database.execute(
            """
            SELECT recipe_description FROM recipe_base WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_recipe_instructions(self, id: int) -> str | None:
        """Returns the instructions of the recipe associated with the given ID."""
        return self.database.execute(
            """
            SELECT recipe_instructions FROM recipe_base WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchone()[0]

    def fetch_recipe_ingredients(self, recipe_id: int) -> dict[int, dict]:
        """Returns the ingredients of the recipe associated with the given ID."""
        rows = self.database.execute(
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
        rows = self.database.execute(
            """
            SELECT serve_time_window FROM recipe_serve_times WHERE recipe_id = ?;
        """,
            (id,),
        ).fetchall()
        return [row[0] for row in rows]

    def fetch_all_global_recipe_tags(self) -> list[str]:
        """Returns a list of all global recipe tags in the database."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT recipe_tag_name FROM global_recipe_tags;
            """
            ).fetchall()
        return [row[0] for row in rows]

    def fetch_recipe_tags_for_recipe(self, recipe_id: int) -> list[str]:
        """Returns a list of all recipe tags for the given recipe ID."""
        rows = self.database.execute(
            """
            SELECT recipe_tag_name
            FROM global_recipe_tags
            JOIN recipe_tags ON global_recipe_tags.recipe_tag_id = recipe_tags.recipe_tag_id
            WHERE recipe_id = ?;
        """,
            (recipe_id,),
        ).fetchall()
        return [row[0] for row in rows]

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
                self.database.execute(query, (ingredient_id,))
                self.database.commit()
        except Exception as e:
            self.database.connection.rollback()
            raise e

    def delete_custom_unit(self, measurement_id: int) -> None:
        """Deletes the given custom measurement from the database."""
        self.database.execute(
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
                self.database.execute(query, (recipe_id,))
                self.database.commit()
        except Exception as e:
            self.database.connection.rollback()
            raise e
