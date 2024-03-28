from typing import Union
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

    def fetch_all_flag_names(self) -> list[str]:
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
            UPDATE ingredient_base
            SET cost_value = ?, qty_unit = ?, qty_value = ?
            WHERE ingredient_id = ?;
        """,
            (cost_value, qty_unit, qty_value, ingredient_id),
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

    def update_ingredient_pc_mass(
        self,
        ingredient_id: int,
        pc_qty: float | None,
        pc_mass_unit: str | None,
        pc_mass_value: float | None,
    ) -> None:
        """Updates the piece mass data for the given ingredient."""
        self.db.execute(
            """
            UPDATE ingredient_base
            SET pc_qty = ?, pc_mass_unit = ?, pc_mass_value = ?
            WHERE ingredient_id = ?;
        """,
            (pc_qty, pc_mass_unit, pc_mass_value, ingredient_id),
        )

    def update_ingredient_flags(
        self, ingredient_id: int, flags: dict[str, bool]
    ) -> None:
        """Updates the flags for the given ingredient."""
        # Clear the existing flags
        self.db.execute(
            """
            DELETE FROM ingredient_flags WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        )
        # Add the new flags
        for flag, value in flags.items():
            flag_id = self.fetch_flag_id(flag)
            if value:
                self.db.execute(
                    """
                    INSERT INTO ingredient_flags (ingredient_id, flag_id) VALUES (?, ?);
                """,
                    (ingredient_id, flag_id),
                )

    def update_ingredient_gi(self, ingredient_id: int, gi: float | None) -> None:
        """Updates the GI for the given ingredient."""
        self.db.execute(
            """
            UPDATE ingredient_base
            SET gi = ?
            WHERE ingredient_id = ?;
        """,
            (gi, ingredient_id),
        )

    def update_ingredient_nutrients(
        self,
        ingredient_id: int,
        nutrients: dict[str, dict[str, Union[None, float, str]]],
    ) -> None:
        """Updates the nutrients for the given ingredient."""
        # Clear the existing nutrients
        self.db.execute(
            """
            DELETE FROM ingredient_nutrient WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        )
        # Add the new nutrients
        for nutrient, data in nutrients.items():
            # Skip if nutrient is not populated
            if not nutrient_is_populated(data):
                continue
            # Get the nutrient ID
            nutrient_id = self.db.execute(
                """
                SELECT nutrient_id FROM nutrient_list WHERE nutrient_name = ?;
            """,
                (nutrient,),
            ).fetchone()[0]
            # Add the nutrient
            self.db.execute(
                """
                INSERT INTO ingredient_nutrient (ingredient_id, nutrient_id, ntr_qty_unit, ntr_qty_value, ing_qty_unit, ing_qty_value)
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

    def fetch_ingredient(self, name: str) -> Ingredient:
        """Retrieves all the data for the named ingredient and
        returns a populated ingredient object."""
        # Grab the ID of the ingredient
        ingredient_id = self.fetch_ingredient_id(name)

        # Instantiate an ingredient instance
        ingredient = Ingredient()

        # Populate the ingredient name
        ingredient.name = name

        # Populate the ingredient ID
        ingredient.id = ingredient_id

        # Fetch data from the base table
        base_data = self.db.execute(
            """
            SELECT description, gi FROM ingredient_base WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchone()
        # Populate GI field on ingredient
        ingredient.description = base_data[0]
        ingredient.gi = base_data[1]

        # Get the cost details
        cost_data = self.db.execute(
            """
            SELECT cost_value, qty_unit, qty_value
            FROM ingredient_base
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
            FROM ingredient_base
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchone()
        # Populate bulk fields on ingredient
        ingredient.density_mass_unit = bulk_data[0]
        ingredient.density_mass_value = bulk_data[1]
        ingredient.density_vol_unit = bulk_data[2]
        ingredient.density_vol_value = bulk_data[3]

        # Get the piece mass details
        pc_mass_data = self.db.execute(
            """
            SELECT pc_qty, pc_mass_unit, pc_mass_value
            FROM ingredient_base
            WHERE ingredient_id = ?;
        """,
            (ingredient_id,),
        ).fetchone()
        # Populate piece mass fields on ingredient
        ingredient.pc_qty = pc_mass_data[0]
        ingredient.pc_mass_unit = pc_mass_data[1]
        ingredient.pc_mass_value = pc_mass_data[2]

        # Get a list of all the flags, init each as false
        ingredient.set_flags({flag: False for flag in self.fetch_all_flag_names()})
        # Get the flag data
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
        ingredient.set_flags({row[0]: True for row in flag_data})

        # Initialise nutrients with empty data
        nutrient_names = self.fetch_all_nutrient_names()
        ingredient.nutrients = {ntr: create_nutrient_dict() for ntr in nutrient_names}

        # Fill in the data which has been populated
        nutrient_data = self.fetch_ingredient_nutrients(ingredient_id)
        for nutrient, data in nutrient_data.items():
            ingredient.nutrients[nutrient] = create_nutrient_dict(
                ntr_qty_value=data["ntr_qty_value"],
                ntr_qty_unit=str(data["ntr_qty_unit"]),
                ing_qty_value=data["ing_qty_value"],
                ing_qty_unit=str(data["ing_qty_unit"]),
            )

        return ingredient

    def fetch_ingredient_nutrients(
        self, ingredient_id: int
    ) -> dict[str, dict[str, float | str]]:
        """Returns a dict of nutrients for the given ingredient ID."""
        rows = self.db.execute(
            """
            SELECT nutrient_name, ntr_qty_unit, ntr_qty_value, ing_qty_unit, ing_qty_value
            FROM nutrient_list
            JOIN ingredient_nutrient ON nutrient_list.nutrient_id = ingredient_nutrient.nutrient_id
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

    def insert_nutrient(self, name: str, parent_id: int | None) -> int:
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


def create_nutrient_dict(
    ntr_qty_value=None, ntr_qty_unit="g", ing_qty_value=None, ing_qty_unit="g"
):
    """
    Create a nutrient dictionary with default or provided values.
    """
    return {
        "ntr_qty_value": ntr_qty_value,
        "ntr_qty_unit": ntr_qty_unit,
        "ing_qty_value": ing_qty_value,
        "ing_qty_unit": ing_qty_unit,
    }


def nutrient_is_populated(nutrient: dict[str, Union[None, float, str]]) -> bool:
    """Returns True if the nutrient has been populated.
    returns false if any of the value fields are None."""
    return all(value is not None for value in nutrient.values())
