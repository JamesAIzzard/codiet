import sqlite3

import model

def _connect() -> sqlite3.Connection:
    return sqlite3.connect('data/codiet.db')

def save_ingredient(ingredient: model.ingredients.Ingredient):
    """Saves the ingredient."""
    conn = _connect()
    cursor = conn.cursor()
    qry = f"""INSERT INTO ingredients
        (ingredient_name)
        VALUES
        ('{ingredient.name}')
    """
    cursor.execute(qry)
    conn.commit()
    cursor.close()
    conn.close()