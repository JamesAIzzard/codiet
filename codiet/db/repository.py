from typing import Optional
import sqlite3

from codiet.exceptions import ingredient_exceptions as ingredient_exceptions

class Repository:
    def __init__(self, db):
        self.db = db

    def get_flag_id(self, name: str) -> int:
        return self.db.execute(
            """
            SELECT flag_id FROM flag_list WHERE flag_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def add_flag(self, name: str) -> int:
        cursor = self.db.execute(
            """
            INSERT INTO flag_list (flag_name) VALUES (?);
        """,
            (name,),
        )
        return cursor.lastrowid

    def get_all_flags(self) -> list[str]:
        """Returns a list of all the flags in the database."""
        rows = self.db.execute(
            """
            SELECT flag_name FROM flag_list;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def get_ingredient_id(self, name: str) -> int:
        return self.db.execute(
            """
            SELECT ingredient_id FROM ingredient_base WHERE ingredient_name = ?;
        """,
            (name,),
        ).fetchone()[0]

    def get_ingredient_names(self) -> list[str]:
        """Returns a list of all the ingredient names in the database."""
        rows = self.db.execute(
            """
            SELECT ingredient_name FROM ingredient_base;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def add_ingredient_name(self, name: str):
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

    def set_ingredient_cost(
        self,
        ingredient_id: int,
        cost_unit: Optional[str],
        cost_value: Optional[float],
        qty_unit: Optional[str],
        qty_value: Optional[float],
    ) -> None:
        self.db.execute(
            """
            INSERT INTO ingredient_cost (ingredient_id, cost_unit, cost_value, qty_unit, qty_value)
            VALUES (?, ?, ?, ?, ?);
        """,
            (ingredient_id, cost_unit, cost_value, qty_unit, qty_value),
        )

    def set_ingredient_density(
        self,
        ingredient_id: int,
        dens_mass_unit: Optional[str],
        dens_mass_value: Optional[float],
        dens_vol_unit: Optional[str],
        dens_vol_value: Optional[float],
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

    def get_all_nutrient_names(self) -> list[str]:
        """Returns a list of all the nutrient names in the database."""
        rows = self.db.execute(
            """
            SELECT nutrient_name FROM nutrient_list;
        """
        ).fetchall()
        return [row[0] for row in rows]

    def add_nutrient(self, name: str, parent_id: Optional[int]) -> int:
        """Adds a nutrient to the database and returns the ID."""
        cursor = self.db.execute(
            """
            INSERT INTO nutrient_list (nutrient_name, parent_id) VALUES (?, ?);
            """,
            (name, parent_id),
        )
        return cursor.lastrowid
    
    def add_nutrient_alias(self, alias: str, primary_nutrient_id: int) -> None:
        """Adds a nutrient alias to the database."""
        self.db.execute(
            """
            INSERT INTO nutrient_alias (nutrient_alias, primary_nutrient_id) VALUES (?, ?);
        """,
            (alias, primary_nutrient_id),
        )
