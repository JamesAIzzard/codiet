"""Consctruction script to create the database schema."""

import sqlite3
from codiet.db import DB_PATH

def create_schema() -> None:
    """
    This module contains a script for creating the database schema.

    Note:
        This code is not included in the repository or database service, 
        hence it has been moved to a separate script.
    """
    # Connect to the database
    connection = sqlite3.connect(DB_PATH)
    # Grab the cursor
    cursor = connection.cursor()
    # Create the tables
    create_global_flag_table(cursor)
    create_global_leaf_nutrient_table(cursor)
    create_global_group_nutrient_table(cursor)
    create_nutrient_alias_table(cursor)
    create_ingredient_base_table(cursor)
    create_ingredient_custom_units_table(cursor)
    create_ingredient_flag_table(cursor)
    create_ingredient_nutrient_table(cursor)
    create_recipe_base_table(cursor)
    create_recipe_ingredient_table(cursor)
    create_recipe_serve_times_table(cursor)
    create_global_recipe_tags_table(cursor)
    create_recipe_tags_table(cursor)
    # Commit the changes
    connection.commit()
    # Close the connection
    connection.close()

def create_global_flag_table(cursor:sqlite3.Cursor) -> None:
    """Create the global flag table in the database."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_flag_list (
            flag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag_name TEXT NOT NULL UNIQUE
        )
    """)

def create_global_leaf_nutrient_table(cursor:sqlite3.Cursor) -> None:
    """Create the leaf nutrient table in the database."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_leaf_nutrients (
            nutrient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutrient_name TEXT NOT NULL UNIQUE,
            parent_id INTEGER,
            FOREIGN KEY (parent_id) REFERENCES global_group_nutrients(nutrient_id)
        )
    """)

def create_global_group_nutrient_table(cursor:sqlite3.Cursor) -> None:
    """Create the group nutrient table in the database."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_group_nutrients (
            nutrient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutrient_name TEXT NOT NULL UNIQUE,
            parent_id INTEGER
        )
    """)

def create_nutrient_alias_table(cursor:sqlite3.Cursor) -> None:
    """Create the nutrient alias table in the database."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrient_aliases (
            nutrient_alias TEXT NOT NULL UNIQUE,
            primary_nutrient_id INTEGER NOT NULL,
            FOREIGN KEY (primary_nutrient_id) REFERENCES nutrient_list(nutrient_id)
        )
    """)

def create_ingredient_base_table(cursor:sqlite3.Cursor) -> None:
    """Create the ingredient base table in the database."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_base (
            ingredient_id INTEGER PRIMARY KEY,
            ingredient_name TEXT NOT NULL UNIQUE,
            ingredient_description TEXT,
            ingredient_gi REAL,
            cost_unit TEXT NOT NULL,
            cost_value REAL,
            cost_qty_unit TEXT,
            cost_qty_value REAL
        )
    """)

def create_ingredient_custom_units_table(cursor:sqlite3.Cursor) -> None:
    """Create the table to associate custom measurements with ingredients."""
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS ingredient_custom_units (
            unit_id INTEGER PRIMARY KEY,
            ingredient_id INTEGER,
            unit_name TEXT,
            custom_unit_qty REAL,
            std_unit_qty REAL,
            std_unit_name TEXT,
            FOREIGN KEY (ingredient_id) REFERENCES ingredient_base(ingredient_id)
        )
    """)

def create_ingredient_flag_table(cursor:sqlite3.Cursor) -> None:
    """Create the table to associate flags with ingredients."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_flags (
            ingredient_id INTEGER,
            flag_id INTEGER,
            flag_value BOOLEAN,
            FOREIGN KEY (ingredient_id) REFERENCES ingredient_base(ingredient_id),
            FOREIGN KEY (flag_id) REFERENCES flag_list(flag_id)
        )
    """)

def create_ingredient_nutrient_table(cursor:sqlite3.Cursor) -> None:
    """Create the table to associate nutrient quantities with recipes."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_nutrients (
            ingredient_id INTEGER NOT NULL,
            nutrient_id INTEGER NOT NULL,
            ntr_mass_unit TEXT,
            ntr_mass_value REAL,
            ing_qty_unit TEXT,
            ing_qty_value REAL,
            FOREIGN KEY (ingredient_id) REFERENCES ingredient_base(ingredient_id),
            FOREIGN KEY (nutrient_id) REFERENCES nutrient_list(nutrient_id)
        )
    """)

def create_recipe_base_table(cursor:sqlite3.Cursor) -> None:
    """Create the recipe base table in the database."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_base (
            recipe_id INTEGER PRIMARY KEY,
            recipe_name TEXT UNIQUE NOT NULL,
            recipe_description TEXT,
            recipe_instructions TEXT
        )
    """)

def create_recipe_ingredient_table(cursor:sqlite3.Cursor) -> None:
    """Create the table to associate ingredient quantities with recipes."""
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

def create_recipe_serve_times_table(cursor:sqlite3.Cursor) -> None:
    """Create the table to associate serve times with recipes."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_serve_times (
            recipe_id INTEGER,
            serve_time_window TEXT,
            FOREIGN KEY (recipe_id) REFERENCES recipe_base(id)
        )
    """)

def create_global_recipe_tags_table(cursor:sqlite3.Cursor) -> None:
    """Create the table for all global recipe tags."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS global_recipe_tags (
            recipe_tag_id INTEGER PRIMARY KEY,
            recipe_tag_name TEXT UNIQUE
        )
    """)

def create_recipe_tags_table(cursor:sqlite3.Cursor) -> None:
    """Create the table to associate recipe tags to recipes."""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_tags (
            recipe_id INTEGER,
            recipe_tag_id INTEGER,
            FOREIGN KEY (recipe_id) REFERENCES recipe_base(id),
            FOREIGN KEY (recipe_tag_id) REFERENCES global_recipe_tags(recipe_tag_id)
        )
    """)