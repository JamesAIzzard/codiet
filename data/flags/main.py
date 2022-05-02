import typing

import data

def get_flag_strings() -> typing.List[str]:
    """Returns a list of all flag strings."""
    qry = """SELECT
        flag_string
    FROM
        flags;
    """
    conn, cursor = data.connect()
    cursor.execute(qry)
    res = cursor.fetchall()
    flags = []
    for row in res:
        flags.append(row[0])
    return flags