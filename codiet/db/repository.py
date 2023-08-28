class Repository:
    def __init__(self, db):
        self.db = db

    def add_ingredient_name(self, name: str):
        """Adds a new ingredient name to the database.

        Args:
            name (str): The name of the ingredient to add.
        """
        self.db.execute(f"""
            INSERT INTO ingredient_base (name) VALUES ({name});
        """)