import typing

from codiet import data

def get_adopted_nutrients() -> typing.List[typing.Tuple[str, str]]:
    """Returns a list of the adopted nutrients."""
    qry = """SELECT
        nutrient_name, nutrient_string
    FROM
        nutrients
    """
    conn, cursor = data.connect()
    cursor.execute(qry)
    res = cursor.fetchall()
    return res