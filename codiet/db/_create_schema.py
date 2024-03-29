def _create_schema(cursor):
    # Create the nutrient tables
    # Build the primary list of nutrients
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrient_list (
            nutrient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nutrient_name TEXT NOT NULL UNIQUE,
            parent_id INTEGER
        )
    """)
    # Build the list of nutrient aliases
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrient_alias (
            nutrient_alias TEXT NOT NULL UNIQUE,
            primary_nutrient_id INTEGER NOT NULL,
            FOREIGN KEY (primary_nutrient_id) REFERENCES nutrient_list(nutrient_id)
        )
    """)

    # Create the ingredient tables.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_base (
            ingredient_id INTEGER PRIMARY KEY,
            ingredient_name TEXT NOT NULL UNIQUE,
            description TEXT,
            gi REAL,
            cost_unit TEXT,
            cost_value REAL,
            qty_unit TEXT,
            qty_value REAL,
            density_mass_unit TEXT,
            density_mass_value REAL,
            density_vol_unit TEXT,
            density_vol_value REAL,
            pc_qty REAL,
            pc_mass_unit TEXT,
            pc_mass_value REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flag_list (
            flag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag_name TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_flags (
            ingredient_id INTEGER,
            flag_id INTEGER,
            FOREIGN KEY (ingredient_id) REFERENCES ingredient_base(ingredient_id),
            FOREIGN KEY (flag_id) REFERENCES flag_list(flag_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient_nutrient (
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

    # Create the recipe tables.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_base (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL UNIQUE
        )
    """)