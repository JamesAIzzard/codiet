from codiet.db.repository.repository_base import RepositoryBase

class FlagRepository(RepositoryBase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def create_flag(self, flag_name: str) -> int:
        """Adds a flag to the flag table and returns the ID."""
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO global_flags (flag_name) VALUES (?);
            """,
                (flag_name,),
            )

            # Get the ID of the flag
            id = cursor.lastrowid

        assert id is not None

        return id
    
    def create_ingredient_flag(self, ingredient_id:int, flag_id:int, flag_value:bool) -> int:
        """Adds a flag to an ingredient."""
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO ingredient_flags (ingredient_id, flag_id, flag_value) VALUES (?, ?, ?);
            """,
                (ingredient_id, flag_id, flag_value),
            )

            # Get the ID of the flag
            id = cursor.lastrowid

        assert id is not None

        return id

    def read_all_global_flag_names(self) -> dict[int, str]:
        """Read all flag names from the flag table.
        Returns:
            flag_id[int]: flag_name[str]
        """
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                SELECT id, flag_name FROM global_flags;
            """
            )

            flags = {}

            for row in cursor.fetchall():
                flags[row[0]] = row[1]

            return flags
        
    def read_ingredient_flags(self, ingredient_id:int) -> dict[int, dict]:
        """Read all flags for an ingredient.
        Returns:
            ingredient_flag_id[int]: {
                "global_flag_id": flag_id[int],
                "flag_value": flag_value[bool] 
            }
        """
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                SELECT flag_id, flag_value FROM ingredient_flags WHERE ingredient_id=?;
            """,
                (ingredient_id,),
            )

            flags = {}

            for row in cursor.fetchall():
                flags[row[0]] = {
                    "flag_id": row[0],
                    "flag_value": row[1],
                }

            return flags

    def update_ingredient_flag(self, ingredient_id: int, flag_id: int, flag_value: bool) -> None:
        """Updates a flag for an ingredient."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE ingredient_flags SET flag_value=? WHERE ingredient_id=? AND flag_id=?;
                """,
                (flag_value, ingredient_id, flag_id),
            )
            # Raise an exception if no flag was found to update
            if cursor.rowcount == 0:
                raise ValueError(f"No ingredient flag found for ingredient_id={ingredient_id} and flag_id={flag_id}")

    def delete_ingredient_flag(self, ingredient_id:int, flag_id:int) -> None:
        """Deletes a flag for an ingredient."""
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM ingredient_flags WHERE ingredient_id=? AND flag_id=?;
            """,
                (ingredient_id, flag_id),
            )