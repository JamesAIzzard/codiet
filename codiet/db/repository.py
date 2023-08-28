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

    def add_flag(self, name: str) -> None:
        self.db.execute(
            """
            INSERT INTO flag_list (flag_name) VALUES (?);
        """,
            (name,),
        )

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
        cost_unit: str,
        cost_value: float,
        mass_unit: str,
        mass_value: float,
    ) -> None:
        self.db.execute(
            """
            INSERT INTO ingredient_cost (ingredient_id, cost_unit, cost_value, qty_unit, qty_value)
            VALUES (?, ?, ?, ?, ?);
        """,
            (ingredient_id, cost_unit, cost_value, mass_unit, mass_value),
        )

    def set_ingredient_density(
        self,
        ingredient_id: int,
        dens_mass_unit: str,
        dens_mass_value: float,
        dens_vol_unit: str,
        dens_vol_value: float,
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
