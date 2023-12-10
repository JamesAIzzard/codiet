from typing import Optional


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

    def add_ingredient_name(self, name: str):
        self.db.execute(
            """
            INSERT INTO ingredient_base (ingredient_name) VALUES (?);
        """,
            (name,),
        )

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

    def add_nutrient(self, name: str, mandatory: bool, parent_id: Optional[int]) -> int:
        """Adds a nutrient to the database and returns the ID."""
        cursor = self.db.execute(
            """
            INSERT INTO nutrient_list (nutrient_name, mandatory, parent_id) VALUES (?, ?, ?);
            """,
            (name, mandatory, parent_id),
        )
        return cursor.lastrowid

    def get_mandatory_nutrient_names(self) -> list[str]:
        """Returns a list of all the mandatory nutrient names in the database."""
        rows = self.db.execute(
            """
            SELECT nutrient_name FROM nutrient_list WHERE mandatory = TRUE;
        """
        ).fetchall()
        return [row[0] for row in rows]
