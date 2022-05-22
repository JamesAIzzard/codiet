import typing

from codiet import data

def get_flag_names_and_strings() -> typing.Dict[str, str]:
    """Returns a Dict. The keys are the flag_names, the values
    are the flag_strings.
    """
    _, cursor = data.connect()
    cursor.execute("""
    SELECT
        flag_name, flag_string
    FROM
        flags;
    """)
    res = cursor.fetchall()
    results = {}
    for row in res:
        results[row[0]] = row[1]
    return results    