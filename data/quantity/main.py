import typing

import data


def get_mass_units() -> typing.Dict[str, float]:
    """Returns a list of all mass units."""
    qry = """SELECT
        unit_name, grams_in_unit
    FROM
        mass_units
    """
    _, cursor = data.connect()
    cursor.execute(qry)
    res = cursor.fetchall()
    units = {}
    for r in res:
        units[r[0]] = r[1]
    return units


def get_vol_units() -> typing.Dict[str, float]:
    """Returns a list of all volume units."""
    qry = """SELECT
        unit_name, mls_in_unit
    FROM
        vol_units
    """
    _, cursor = data.connect()
    cursor.execute(qry)
    res = cursor.fetchall()
    units = {}
    for r in res:
        units[r[0]] = r[1]
    return units