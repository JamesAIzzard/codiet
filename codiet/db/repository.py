class Repository:
    def __init__(self, db):
        self.db = db

    def get_ingredient_id(self, name: str) -> int:
        """Gets the primary key of an ingredient from the database.

        Args:
            name (str): The name of the ingredient to get the ID of.

        Returns:
            int: The primary key of the ingredient.
        """
        return self.db.execute("""
            SELECT ingredient_id FROM ingredient_base WHERE ingredient_name = ?;
        """, (name,)).fetchone()[0]

    def add_ingredient_name(self, name: str) -> int:
        """Adds a new ingredient name to the database.

        Args:
            name (str): The name of the ingredient to add.
        """
        return self.db.execute("""
            INSERT INTO ingredient_base (ingredient_name) VALUES (?);
        """, (name,))

    def add_ingredient_cost(self, ingredient_id:int, cost_unit:str, cost_value:float, mass_unit:str, mass_value:float) -> None:
        """Adds the cost data of an ingredient to the database.

        Args:
            ingredient_id (int): The primary key of the ingredient.
            cost_unit (str): The unit of the cost.
            cost_value (float): The value of the cost.
            mass_unit (str): The unit of the mass.
            mass_value (float): The value of the mass.
        """
        self.db.execute("""
            INSERT INTO ingredient_cost (ingredient_id, cost_unit, cost_value, mass_unit, mass_value)
            VALUES (?, ?, ?, ?, ?);
        """, (ingredient_id, cost_unit, cost_value, mass_unit, mass_value))