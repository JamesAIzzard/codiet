import sqlite3

from typing import List, Tuple

import model

# Initialise the connecton
conn = sqlite3.connect("data/codiet.db")
cursor = conn.cursor()


def get_adopted_nutrients() -> List[Tuple[str, str]]:
    """Returns a list of the adopted nutrients."""
    qry = """SELECT
        nutrient_name, nutrient_string
    FROM
        nutrients
    """
    cursor.execute(qry)
    data = cursor.fetchall()
    return data


def get_flag_strings() -> List[str]:
    """Returns a list of all flag strings."""
    qry = """SELECT
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


def get_mass_units() -> List[str]:
    """Returns a list of all mass units."""
    qry = """SELECT
        unit_name
    FROM
        mass_units
    """
    cursor.execute(qry)
    data = cursor.fetchall()
    units = []
    for row in data:
        units.append(row[0])
    return units


def get_vol_units() -> List[str]:
    """Returns a list of all volume units."""
    qry = """SELECT
        unit_name
    FROM
        vol_units
    """
    cursor.execute(qry)
    data = cursor.fetchall()
    units = []
    for row in data:
        units.append(row[0])
    return units


def save_ingredient(ingredient: model.ingredients.Ingredient):
    """Saves the ingredient."""
    qry = f"""INSERT INTO ingredients
        (name, )
        VALUES
        ('{ingredient.name}');
    """
    cursor.execute(qry)
    conn.commit()
