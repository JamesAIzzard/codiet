import typing

import data


def get_mass_units() -> typing.List[str]:
    """Returns a list of all mass units."""
    qry = """SELECT
        unit_name
    FROM
        mass_units
    """
    conn, cursor = data.connect()
    cursor.execute(qry)
    res = cursor.fetchall()
    units = []
    for row in res:
        units.append(row[0])
    return units


def get_vol_units() -> typing.List[str]:
    """Returns a list of all volume units."""
    qry = """SELECT
        unit_name
    FROM
        vol_units
    """
    conn, cursor = data.connect()
    cursor.execute(qry)
    res = cursor.fetchall()
    units = []
    for row in res:
        units.append(row[0])
    return units