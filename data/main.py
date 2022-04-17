import sqlite3
from typing import List

import model

# Initialise the connecton
conn = sqlite3.connect('data/codiet.db')
cursor = conn.cursor()

def get_flag_strings() -> List[str]:
    """Returns a list of all flag strings."""
    qry = f"""SELECT
        flag_string
    FROM
        flags;
    """
    cursor.execute(qry)
    data = cursor.fetchall()
    flags = []
    for row in data:
        flags.append(row[0])
    return flags

def save_ingredient(ingredient: model.ingredients.Ingredient):
    """Saves the ingredient."""
    qry = f"""INSERT INTO ingredients
        (ingredient_name)
        VALUES
        ('{ingredient.name}');
    """
    cursor.execute(qry)
    conn.commit()