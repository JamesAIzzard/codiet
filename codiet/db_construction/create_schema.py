import sqlite3
from codiet.db import DB_PATH

def create_schema():
    """Create the database schema."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create the global flag table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_flag_list (
            flag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag_name TEXT NOT NULL UNIQUE
        )
    """)

    # Create the nutrient tables
    # Build the global table of leaf nutrients
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_leaf_nutrients (
            nutrient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutrient_name TEXT NOT NULL UNIQUE,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES global_group_nutrients(nutrient_id)
        )
    """)
    # Build the global table of group nutrients
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_group_nutrients (
            nutrient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutrient_name TEXT NOT NULL UNIQUE,
            parent_id INTEGER
        )
    """)
    # Build the list of nutrient aliases
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrient_aliases (
            nutrient_alias TEXT NOT NULL UNIQUE,
            primary_nutrient_id INTEGER NOT NULL,
            FOREIGN KEY (primary_nutrient_id) REFERENCES nutrient_list(nutrient_id)
        )
    """)

    # Create the ingredient tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_base (
            ingredient_id INTEGER PRIMARY KEY,
            ingredient_name TEXT NOT NULL UNIQUE,
            description TEXT,
            gi REAL,
            cost_unit TEXT,
            cost_value REAL,
            cost_qty_unit TEXT,
            cost_qty_value REAL,
            density_mass_unit TEXT,
            density_mass_value REAL,
            density_vol_unit TEXT,
            density_vol_value REAL,
            pc_qty REAL,
            pc_mass_unit TEXT,
            pc_mass_value REAL
        )
    """)

    # Create the ingredient flag tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_flags (
            ingredient_id INTEGER,
            flag_id INTEGER,
            flag_value BOOLEAN,
            FOREIGN KEY (ingredient_id) REFERENCES ingredient_base(ingredient_id),
            FOREIGN KEY (flag_id) REFERENCES flag_list(flag_id)
        )
    """)

    # Create the ingredient nutrient table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_nutrients (
            ingredient_id INTEGER,
            nutrient_id INTEGER,
            ntr_qty_unit TEXT,
            ntr_qty_value REAL,
            ing_qty_unit TEXT,
            ing_qty_value REAL,
            FOREIGN KEY (ingredient_id) REFERENCES ingredient_base(ingredient_id),
            FOREIGN KEY (nutrient_id) REFERENCES nutrient_list(nutrient_id)
        )
    """)

    # Create the recipe table.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_base (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    """)

    # Create the recipe ingredient table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            recipe_id INTEGER,
            ingredient_id INTEGER,
            qty_unit TEXT,
            qty_value REAL,
            qty_tol_upper REAL,
            qty_tol_lower REAL,
            FOREIGN KEY (recipe_id) REFERENCES recipe_base(id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredient_base(ingredient_id)
        )
    """)

    connection.commit()
    connection.close()