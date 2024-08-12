import os
import sqlite3

class Database:
    def __init__(self, db_path:str):
        self._db_path = db_path
        self._connection = None

    @property
    def connection(self) -> sqlite3.Connection:
        """Return a connection to the database."""
        if self._connection is None:
            self._connection = self._connection = sqlite3.connect(self._db_path)
        return self._connection
    
    def close_connection(self) -> None:
        """Close the connection to the database."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def create_database_file(self) -> None:
        """Create the database file."""
        connection = self.connection
        cursor = connection.cursor()

        # Create the tables
        # Global tables
        self.create_unit_base_table(cursor)
        self.create_global_unit_conversion_table(cursor)
        self.create_unit_alias_table(cursor)
        self.create_global_flags_table(cursor)
        self.create_global_nutrients_table(cursor)
        self.create_nutrient_alias_table(cursor)
        self.create_global_recipe_tags_table(cursor)

        # Ingredients tables   
        self.create_ingredient_base_table(cursor)
        self.create_ingredient_unit_conversions_table(cursor)
        self.create_ingredient_flags_table(cursor)
        self.create_ingredient_nutrient_quantities_table(cursor)

        # Recipes tables
        self.create_recipe_base_table(cursor)
        self.create_recipe_ingredients_table(cursor)
        self.create_recipe_serve_time_windows_table(cursor)
        self.create_recipe_tags_table(cursor)
        
        # Commit the changes
        connection.commit()

    def delete_database_file(self) -> None:
        """Delete the database file."""
        self.close_connection()
        os.remove(self._db_path)

    def create_unit_base_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the global unit table in the database."""
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS unit_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unit_name TEXT NOT NULL UNIQUE,
                single_display_name TEXT NOT NULL,
                plural_display_name TEXT NOT NULL,
                unit_type TEXT NOT NULL
            )
        """)

    def create_global_unit_conversion_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the global unit conversion table in the database."""
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS global_unit_conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_unit_id INTEGER NOT NULL,
                to_unit_id INTEGER NOT NULL,
                from_unit_qty REAL,
                to_unit_qty REAL,
                FOREIGN KEY (from_unit_id) REFERENCES global_units(id),
                FOREIGN KEY (to_unit_id) REFERENCES global_units(id)
            )
        """)

    def create_unit_alias_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the global unit alias table in the database."""
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS unit_aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias TEXT NOT NULL UNIQUE,
                primary_unit_id INTEGER NOT NULL,
                FOREIGN KEY (primary_unit_id) REFERENCES global_units(id)
            )
        """)

    def create_global_flags_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the global flag table in the database."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS global_flags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flag_name TEXT NOT NULL UNIQUE
            )
        """)

    def create_global_nutrients_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the leaf nutrient table in the database."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS global_nutrients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nutrient_name TEXT NOT NULL UNIQUE,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES global_nutrients(id)
            )
        """)

    def create_nutrient_alias_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the nutrient alias table in the database."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nutrient_aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nutrient_alias TEXT NOT NULL UNIQUE,
                primary_nutrient_id INTEGER NOT NULL,
                FOREIGN KEY (primary_nutrient_id) REFERENCES global_nutrients(id)
            )
        """)

    def create_global_recipe_tags_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the table for all global recipe tags."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS global_recipe_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                parent_tag_id INTEGER,
                recipe_tag_name TEXT UNIQUE
            )
        """)

    def create_ingredient_base_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the ingredient base table in the database."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredient_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                gi REAL,
                cost_unit_id INTEGER,
                cost_value REAL,
                cost_qty_unit_id INTEGER,
                cost_qty_value REAL,
                standard_unit_id INTEGER,
                FOREIGN KEY (cost_qty_unit_id) REFERENCES global_units(id),
                FOREIGN KEY (standard_unit_id) REFERENCES global_units(id)
            )
        """)

    def create_ingredient_unit_conversions_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the table for ingredient conversions specific to ingredients."""
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS ingredient_unit_conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_id INTEGER NOT NULL,
                from_unit_id INTEGER NOT NULL,
                to_unit_id INTEGER NOT NULL,
                from_unit_qty REAL,
                to_unit_qty REAL,
                FOREIGN KEY (ingredient_id) REFERENCES ingredient_base(id)
                FOREIGN KEY (from_unit_id) REFERENCES global_units(id)
                FOREIGN KEY (to_unit_id) REFERENCES global_units(id)
            )
        """)

    def create_ingredient_flags_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the table to associate flags with ingredients."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredient_flags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_id INTEGER,
                flag_id INTEGER,
                flag_value BOOLEAN NOT NULL,
                FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
                FOREIGN KEY (flag_id) REFERENCES global_flags(id)
            )
        """)

    def create_ingredient_nutrient_quantities_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the table to associate nutrient quantities with recipes."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredient_nutrient_quantities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_id INTEGER NOT NULL,
                nutrient_id INTEGER NOT NULL,
                ntr_mass_unit_id INTEGER NOT NULL,
                ntr_mass_value REAL,
                ing_grams_qty REAL,
                FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
                FOREIGN KEY (nutrient_id) REFERENCES nutrient_list(id),
                FOREIGN KEY (ntr_mass_unit_id) REFERENCES global_units(id)
            )
        """)

    def create_recipe_base_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the recipe base table in the database."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipe_base (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_name TEXT UNIQUE NOT NULL,
                use_as_ingredient BOOLEAN NOT NULL,
                recipe_description TEXT,
                recipe_instructions TEXT
            )
        """)

    def create_recipe_ingredients_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the table to associate ingredient quantities with recipes."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipe_ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                ingredient_id INTEGER,
                qty_unit_id INTEGER,
                qty_value REAL,
                qty_utol REAL,
                qty_ltol REAL,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
            )
        """)

    def create_recipe_serve_time_windows_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the table to associate serve times with recipes."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipe_serve_time_windows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                serve_time_window TEXT,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id)
            )
        """)

    def create_recipe_tags_table(self, cursor:sqlite3.Cursor) -> None:
        """Create the table to associate recipe tags to recipes."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipe_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER,
                recipe_tag_id INTEGER,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                FOREIGN KEY (recipe_tag_id) REFERENCES global_recipe_tags(id)
            )
        """)        