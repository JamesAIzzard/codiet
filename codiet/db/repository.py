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

    def insert_recipe_serve_time_window(self, recipe_id: int, serve_time_window: str) -> int:
        """Adds a serve window to the database and returns the ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO recipe_serve_time_windows (recipe_id, serve_time_window) VALUES (?, ?);
            """,
                (recipe_id, serve_time_window),
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
        cost_qty_unit_id: int | None,
        cost_qty_value: float | None,
    ) -> None:
        """Updates the cost data of the ingredient associated with the given ID."""
        cost_unit_id = 1 # This will refer to currency codes in future.
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingredients
                SET cost_unit_id = ?, cost_value = ?, cost_qty_unit_id = ?, cost_qty_value = ?
                WHERE id = ?;
            """,
                (cost_unit_id, cost_value, cost_qty_unit_id, cost_qty_value, ingredient_id),
            )

    def upsert_ingredient_flag(
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
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingredients
                SET ingredient_gi = ?
                WHERE id = ?;
            """,
                (gi, ingredient_id),
            )

    def upsert_ingredient_nutrient_quantity(
            self,
            ingredient_id: int,
            global_nutrient_id: int,
            ntr_mass_unit_id: int | None,
            ntr_mass_value: float | None,
            ing_qty_unit_id: int | None,
            ing_qty_value: float | None,
        ) -> None:
            """Inserts or updates the nutrient quantity of the ingredient associated with the given ID."""
            with self.get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO ingredient_nutrients
                    (ingredient_id, nutrient_id, ntr_mass_unit_id, ntr_mass_value, ing_qty_unit_id, ing_qty_value)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """,
                    (
                        ingredient_id,
                        global_nutrient_id,
                        ntr_mass_unit_id,
                        ntr_mass_value,
                        ing_qty_unit_id,
                        ing_qty_value,
                    ),
                )

    def update_recipe_name(self, recipe_id: int, name: str) -> None:
        """Updates the name of the recipe associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE recipes
                SET recipe_name = ?
                WHERE id = ?;
            """,
                (name, recipe_id),
            )

    def update_recipe_description(
        self, recipe_id: int, description: str | None
    ) -> None:
        """Updates the description of the recipe associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE recipes
                SET recipe_description = ?
                WHERE id = ?;
            """,
                (description, recipe_id),
            )

    def update_recipe_instructions(
        self, recipe_id: int, instructions: str | None
    ) -> None:
        """Updates the instructions of the recipe associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE recipes
                SET recipe_instructions = ?
                WHERE id = ?;
            """,
                (instructions, recipe_id),
            )

    def upsert_recipe_ingredient(
        self,
        recipe_id: int,
        ingredient_id: int,
        qty_unit_id: int|None,
        qty_value: float|None,
        qty_utol: float|None,
        qty_ltol: float|None

    ) -> None:
        """Updates the ingredients of the recipe associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT OR REPLACE INTO recipe_ingredients
                (recipe_id, ingredient_id, qty_unit_id, qty_value, qty_utol, qty_ltol)
                VALUES (?, ?, ?, ?, ?, ?);
            """,
                (recipe_id, ingredient_id, qty_unit_id, qty_value, qty_utol, qty_ltol),
            )

    def update_recipe_serve_time_window(self, serve_time_id:int, serve_time_window:str) -> None:
        """Updates the serve times of the recipe associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE recipe_serve_time_windows
                SET serve_time_window = ?
                WHERE id = ?;
            """,
                (serve_time_window, serve_time_id),
            )

    def update_recipe_tags(self, recipe_id: int, recipe_tag_ids: list[int]) -> None:
        """Updates the recipe tags of the recipe associated with the given ID."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM recipe_tags
                WHERE recipe_id = ?;
            """,
                (recipe_id,),
            )
            for tag_id in recipe_tag_ids:
                cursor.execute(
                    """
                    INSERT INTO recipe_tags (recipe_id, recipe_tag_id) VALUES (?, ?);
                """,
                    (recipe_id, tag_id),
                )

    def fetch_all_global_units(self) -> dict[int, dict]:
        """Returns a dictionary of all global units in the database.
        Data structure returned is a dictionary:
        {
            unit_id: {
                'unit_name': str,
                'plural_name': str,
                'unit_type': str,
                'aliases': dict[int, str],
                'conversions': dict[int, float]
            }
        }
        """
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
    
    def fetch_global_unit_aliases(self, unit_id: int) -> dict[int, str]:
        """Returns a list of aliases for the given global unit ID.
        Data structure returned is a dictionary:
        {
            alias_id: alias_name
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, alias FROM global_unit_aliases WHERE primary_unit_id = ?;
            """,
                (unit_id,),
            ).fetchall()
        return {row[0]: row[1] for row in rows}
    
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

    def fetch_all_global_unit_names(self) -> dict[int, str]:
        """Returns a list of all global units in the database.
        Data structure returned is a dictionary:
        {
            unit_id: unit_name
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, unit_name FROM global_units;
            """
            ).fetchall()
        return {row[0]: row[1] for row in rows}

    def fetch_all_global_flags(self) -> dict[int, str]:
        """Returns a list of all global flags in the database.
        Data structure returned is a dictionary:
        {
            flag_id: flag_name
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, flag_name FROM global_flags;
            """
            ).fetchall()
        return {row[0]: row[1] for row in rows}

    def fetch_all_global_nutrients(self) -> dict[int, dict]:
        """
        Retrieve all group nutrient names from the database.
    
        This method returns a dictionary with the following structure:
        {
            nutrient_id: {
                'nutrient_name': str,
                'aliases': list[str],
                'parent_id': int
            }
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

    def fetch_all_global_recipe_tags(self) -> dict[int, str]:
        """Returns a list of all global recipe tags in the database.
        Data structure returned is a dictionary:
        {
            recipe_tag_id: recipe_tag_name
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, recipe_tag_name FROM global_recipe_tags;
            """
            ).fetchall()
        return {row[0]: row[1] for row in rows}

    def fetch_all_ingredient_names(self) -> dict[int, str]:
        """Returns a list of all the ingredient names in the database.
        Data structure returned is a dictionary:
        {
            ingredient_id: ingredient_name
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, ingredient_name FROM ingredients;
            """
            ).fetchall()
        return {row[0]: row[1] for row in rows}

    def fetch_ingredient_description(self, ingredient_id: int) -> str | None:
        """Returns the description of the ingredient associated with the given ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT ingredient_description FROM ingredients WHERE id = ?;
            """,
                (ingredient_id,),
            ).fetchall()
        return rows[0][0] if rows else None

    def fetch_ingredient_cost(self, ingredient_id: int) -> dict:
        """
        Return the cost data of the ingredient associated with the given ID.

        The data structure returned is a dictionary:
        {
            'cost_value': float | None,
            'cost_qty_unit_id': int | None,
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
                SELECT cost_value, cost_qty_unit_id, cost_qty_value
                FROM ingredients
                WHERE id = ?;
            """,
                (ingredient_id,),
            ).fetchall()
        return {
            "cost_value": rows[0][0],
            "cost_qty_unit_id": rows[0][1],
            "cost_qty_value": rows[0][2],
        }

    def fetch_ingredient_units(self, ingredient_id: int) -> dict[int, dict]:
        """Returns a list of custom measurements for the given ingredient ID.
        Data structure returned is a dictionary:
        {
            ingredient_unit_id: {
                'target_unit_global_id': int,
                'ref_unit_global_id': int,
                'target_unit_qty': float,
                'ref_unit_qty': float
            }
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT custom_unit_id, target_unit_global_id, ref_unit_global_id, target_unit_qty, ref_unit_qty
                FROM ingredient_custom_units
                WHERE ingredient_id = ?;
            """,
                (ingredient_id,),
            ).fetchall()
        return {
            row[0]: {
                "target_unit_global_id": row[1],
                "ref_unit_global_id": row[2],
                "target_unit_qty": row[3],
                "ref_unit_qty": row[4],
            }
            for row in rows
        }

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

    def fetch_ingredient_gi(self, ingredient_id: int) -> float | None:
        """Returns the GI of the ingredient associated with the given ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT ingredient_gi FROM ingredients WHERE id = ?;
            """,
                (ingredient_id,),
            ).fetchall()
        return rows[0][0] if rows else None

    def fetch_ingredient_nutrient_quantities(
        self, ingredient_id: int
    ) -> dict[int, dict]:
        """Returns a dict of nutrients for the given ingredient ID.
        
        The data structure returned is a dictionary:
        {
            nutrient_id: {
                'ntr_mass_unit_id': int|None,
                'ntr_mass_value': float|None,
                'ing_qty_unit_id': int|None,
                'ing_qty_value': float|None
            }
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT nutrient_id, ntr_mass_unit_id, ntr_mass_value, ing_qty_unit_id, ing_qty_value
                FROM ingredient_nutrients
                WHERE ingredient_id = ?;
            """,
                (ingredient_id,),
            ).fetchall()
        return {
            row[0]: {
                "ntr_mass_unit_id": row[1],
                "ntr_mass_value": row[2],
                "ing_qty_unit_id": row[3],
                "ing_qty_value": row[4],
            }
            for row in rows
        }

    def fetch_all_recipe_names(self) -> dict[int, str]:
        """Returns a list of all the recipe names in the database.
        Data structure returned is a dictionary:
        {
            recipe_id: recipe_name
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, recipe_name FROM recipes;
            """
            ).fetchall()
        return {row[0]: row[1] for row in rows}

    def fetch_recipe_description(self, recipe_id: int) -> str | None:
        """Returns the description of the recipe associated with the given ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT recipe_description FROM recipes WHERE id = ?;
            """,
                (recipe_id,),
            ).fetchall()
        return rows[0][0] if rows else None

    def fetch_recipe_instructions(self, recipe_id: int) -> str | None:
        """Returns the instructions of the recipe associated with the given ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT recipe_instructions FROM recipes WHERE id = ?;
            """,
                (recipe_id,),
            ).fetchall()
        return rows[0][0] if rows else None

    def fetch_recipe_ingredients(self, recipe_id: int) -> dict[int, dict]:
        """
        Returns the ingredients of the recipe associated with the given ID.
        Data structure returned is a dictionary:
        {
            ingredient_id: {
                'qty_value': float|None,
                'qty_unit_id': int|None,
                'qty_utol': float|None,
                'qty_ltol': float|None
            }
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT ingredient_id, qty_value, qty_unit_id, qty_utol, qty_ltol
                FROM recipe_ingredients
                WHERE recipe_id = ?;
            """,
                (recipe_id,),
            ).fetchall()
        return {
            row[0]: {
                "qty_value": row[1],
                "qty_unit_id": row[2],
                "qty_utol": row[3],
                "qty_ltol": row[4],
            }
            for row in rows
        }

    def fetch_recipe_serve_time_windows(self, recipe_id: int) -> dict[int, str]:
        """Returns the serve times of the recipe associated with the given ID.
        Data structure returned is a dictionary:
        {
            serve_time_id: serve_time_window
        }
        """
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, serve_time_window
                FROM recipe_serve_time_windows
                WHERE recipe_id = ?;
            """,
                (recipe_id,),
            ).fetchall()
        return {row[0]: row[1] for row in rows}

    def fetch_recipe_tags(self, recipe_id: int) -> list[int]:
        """Returns a list of all recipe tags for the given recipe ID."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT recipe_tag_id FROM recipe_tags WHERE recipe_id = ?;
            """,
                (recipe_id,),
            ).fetchall()
        return [row[0] for row in rows]

    def delete_ingredient(self, ingredient_id: int) -> None:
        """Deletes the given ingredient from the database."""
        # Remove all entries against the ID from all ingredient tables.
        queries = [
            """
            DELETE FROM ingredients
            WHERE id = ?;
            """,
            """
            DELETE FROM ingredient_flags
            WHERE ingredient_id = ?;
            """,
            """
            DELETE FROM ingredient_nutrients
            WHERE ingredient_id = ?;
            """,
            """
            DELETE FROM ingredient_units
            WHERE ingredient_id = ?;
            """,
        ]
        with self.get_cursor() as cursor:
            for query in queries:
                cursor.execute(query, (ingredient_id,))

    def delete_recipe(self, recipe_id: int) -> None:
        """Deletes the given recipe from the database."""
        # Remove all entries against the ID from all recipe tables.
        queries = [
            """
            DELETE FROM recipes
            WHERE id = ?;
            """,
            """
            DELETE FROM recipe_ingredients
            WHERE recipe_id = ?;
            """,
            """
            DELETE FROM recipe_tags
            WHERE recipe_id = ?;
            """,
            """
            DELETE FROM recipe_serve_time_windows
            WHERE recipe_id = ?;
            """,
        ]
        with self.get_cursor() as cursor:
            for query in queries:
                cursor.execute(query, (recipe_id,))
