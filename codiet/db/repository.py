from typing import Optional
import sqlite3

from codiet.models.ingredient import Ingredient
from codiet.exceptions import ingredient_exceptions as ingredient_exceptions


class Repository:
    def __init__(self, db):
        self.db = db

    def fetch_flag_id(self, name: str) -> int:
        return self.db.execute(
            """
            SELECT flag_id FROM flag_list WHERE flag_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def insert_flag_into_database(self, name: str) -> int:
        cursor = self.db.execute(
            """
            INSERT INTO flag_list (flag_name) VALUES (?);
        """,
            (name,),
        )
        return cursor.lastrowid

    def fetch_all_flags(self) -> list[str]:
        """Returns a list of all the flags in the database."""
        rows = self.db.execute(
            """
            SELECT flag_name FROM flag_list;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def fetch_ingredient_id(self, name: str) -> int:
        return self.db.execute(
            """
            SELECT ingredient_id FROM ingredient_base WHERE ingredient_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def fetch_all_ingredient_names(self) -> list[str]:
        """Returns a list of all the ingredient names in the database."""
        rows = self.db.execute(
            """
            SELECT ingredient_name FROM ingredient_base;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def insert_ingredient_entry(self, name: str):
        """Adds an ingredient name to the database."""
        try:
            self.db.execute(
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
        """Updates the name of the given ingredient."""
        self.db.execute(
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
        """Sets the description for the given ingredient."""
        self.db.execute(
            """
            UPDATE ingredient_base
            SET description = ?
            WHERE ingredient_id = ?;
            """,
            (description, ingredient_id),
        )

    def insert_ingredient_cost(
        self,
        ingredient_id: int,
        cost_value: Optional[float],
        qty_unit: Optional[str],
        qty_value: Optional[float],
    ) -> None:
        """Sets the cost data for the given ingredient."""
        self.db.execute(
            """
            INSERT INTO ingredient_cost (ingredient_id, cost_unit, cost_value, qty_unit, qty_value)
            VALUES (?, 'GBP', ?, ?, ?);
        """,
            (ingredient_id, cost_value, qty_unit, qty_value),
        )

    def update_ingredient_cost(
        self,
        ingredient_id: int,
        cost_value: float | None,
        qty_unit: str | None,
        qty_value: float | None,
    ) -> None:
        """Updates the cost data for the given ingredient."""
        self.db.execute(
            """
            UPDATE ingredient_cost
            SET cost_value = ?, qty_unit = ?, qty_value = ?
            WHERE ingredient_id = ?;
        """,
            (cost_value, qty_unit, qty_value, ingredient_id),
        )

    def insert_ingredient_density(
        self,
        ingredient_id: int,
        dens_mass_unit: str | None,
        dens_mass_value: float | None,
        dens_vol_unit: str | None,
        dens_vol_value: float | None,
    ):
        self.db.execute(
            """
            INSERT INTO ingredient_bulk (ingredient_id, density_mass_unit, density_mass_value, density_vol_unit, density_vol_value)
            VALUES (?, ?, ?, ?, ?);
        """,
            (
                ingredient_id,
                dens_mass_unit,
                dens_mass_value,
                dens_vol_unit,
                dens_vol_value,
            ),
        )

    def update_ingredient_density(
        self,
        ingredient_id: int,
        dens_mass_unit: str | None,
        dens_mass_value: float | None,
        dens_vol_unit: str | None,
        dens_vol_value: float | None,
    ) -> None:
        """Updates the density data for the given ingredient."""
        self.db.execute(
            """
            UPDATE ingredient_bulk
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

    def fetch_ingredient(self, name: str) -> Ingredient:
        """Retrieves all the data for the named ingredient and
        returns a populated ingredient object."""
        # Grab the ID of the ingredient
        ingredient_id = self.fetch_ingredient_id(name)

        # Instantiate the ingredient
        ingredient = Ingredient(name=name)

        # Populate the ingredient ID
        ingredient.id = ingredient_id

        # Fetch data from the base table
        base_data = self.db.execute(
            """
            SELECT gi FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchone()
        # Populate GI field on ingredient
        ingredient.gi = base_data[0]

        # Get the cost details
        cost_data = self.db.execute(
            """
            SELECT cost_value, qty_unit, qty_value
            FROM ingredient_cost
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchone()
        # Populate cost fields on ingredient
        ingredient.cost_value = cost_data[0]
        ingredient.cost_qty_unit = cost_data[1]
        ingredient.cost_qty_value = cost_data[2]

        # Get the bulk details
        bulk_data = self.db.execute(
            """
            SELECT density_mass_unit, density_mass_value, density_vol_unit, density_vol_value
            FROM ingredient_bulk
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchone()
        # Populate bulk fields on ingredient
        ingredient.density_mass_unit = bulk_data[0]
        ingredient.density_mass_value = bulk_data[1]
        ingredient.density_vol_unit = bulk_data[2]
        ingredient.density_vol_value = bulk_data[3]

        # Get the flags
        flag_data = self.db.execute(
            """
            SELECT flag_name
            FROM flag_list
            JOIN ingredient_flags ON flag_list.flag_id = ingredient_flags.flag_id
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchall()
        # Populate flags on ingredient
        ingredient.flags = [row[0] for row in flag_data]

        # Get the nutrient data
        nutrient_data = self.db.execute(
            """
            SELECT nutrient_name, quantity_unit, quantity_value, serving_size_unit, serving_size_value
            FROM nutrient_list
            JOIN ingredient_nutrient ON nutrient_list.nutrient_id = ingredient_nutrient.nutrient_id
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchall()
        # Populate nutrients on ingredient
        for row in nutrient_data:
            ingredient.nutrients[row[0]] = {
                "ntr_qty": row[2],
                "ntr_qty_unit": row[1],
                "ing_qty": row[4],
                "ing_qty_unit": row[3],
            }

        return ingredient

    def delete_ingredient(self, ingredient_name: str) -> None:
        """Deletes the given ingredient from the database."""
        # Grab the ID of the ingredient
        ingredient_id = self.fetch_ingredient_id(ingredient_name)

        # Remove all entries against the ID from all ingredient tables
        # which include ingredient_base, ingredient_bulk, ingredient_cost,
        # ingredient_nutrient, and ingredient_flag.
        queries = [
            """
            DELETE FROM ingredient_base
            WHERE ingredient_id = ?;
            """,
            """
            DELETE FROM ingredient_bulk
            WHERE ingredient_id = ?;
            """,
            """
            DELETE FROM ingredient_cost
            WHERE ingredient_id = ?;
            """,
            """
            DELETE FROM ingredient_nutrient
            WHERE ingredient_id = ?;
            """,
            """
            DELETE FROM ingredient_flags
            WHERE ingredient_id = ?;
            """,
        ]
        try:
            for query in queries:
                self.db.execute(query, (ingredient_id,))
                self.db.commit()
        except Exception as e:
            self.db.connection.rollback()
            raise e

    def fetch_all_nutrient_names(self) -> list[str]:
        """Returns a list of all the nutrient names in the database."""
        rows = self.db.execute(
            """
            SELECT nutrient_name FROM nutrient_list;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def insert_nutrient(self, name: str, parent_id: Optional[int]) -> int:
        """Adds a nutrient to the database and returns the ID."""
        cursor = self.db.execute(
            """
            INSERT INTO nutrient_list (nutrient_name, parent_id) VALUES (?, ?);
            """,
            (name, parent_id),
        )
        return cursor.lastrowid

    def insert_nutrient_alias(self, alias: str, primary_nutrient_id: int) -> None:
        """Adds a nutrient alias to the database."""
        self.db.execute(
            """
            INSERT INTO nutrient_alias (nutrient_alias, primary_nutrient_id) VALUES (?, ?);
        """,
            (alias, primary_nutrient_id),
        )
