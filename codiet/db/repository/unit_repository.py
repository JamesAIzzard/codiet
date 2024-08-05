from codiet.db.database import Database
from codiet.db.repository.repository_base import RepositoryBase

class UnitRepository(RepositoryBase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def create_unit_base(
        self,
        unit_name: str,
        single_display_name: str,
        plural_display_name: str,
        unit_type: str,
    ) -> int:
        """Adds a unit to the unit base table and returns the ID."""
        # Add the global unit to the base table
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO unit_base (unit_name, single_display_name, plural_display_name, unit_type) VALUES (?, ?, ?, ?);
            """,
                (unit_name, single_display_name, plural_display_name, unit_type),
            )

            # Get the ID of the unit
            id = cursor.lastrowid

        assert id is not None

        return id 
    
    def create_unit_alias(self, alias: str, primary_unit_id:int) -> int:
        """Adds an alias to the unit alias table."""
        with self.get_cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO unit_aliases (alias, primary_unit_id) VALUES (?, ?);
            """,
                (alias, primary_unit_id),
            )

            # Get the ID of the unit
            id = cursor.lastrowid

        assert id is not None

        return id

    def read_unit_base(self, unit_id: int) -> dict:
        """Returns the unit base with the given ID."""
        with self.get_cursor() as cursor:
            row = cursor.execute(
                """
                SELECT unit_name, single_display_name, plural_display_name, unit_type FROM unit_base WHERE id = ?;
            """,
                (unit_id,),
            ).fetchone()
        return {
            "unit_name": row[0],
            "single_display_name": row[1],
            "plural_display_name": row[2],
            "unit_type": row[3],
        }

    def read_all_unit_bases(self) -> list[dict]:
        """Return all unit bases."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, unit_name, single_display_name, plural_display_name, unit_type FROM unit_base;
            """
            ).fetchall()
        return [
            {
                "id": row[0],
                "unit_name": row[1],
                "single_display_name": row[2],
                "plural_display_name": row[3],
                "unit_type": row[4],
            }
            for row in rows
        ]
    
    def read_unit_aliases(self, unit_id: int) -> dict[int, str]:
        """Return all aliases for a unit."""
        with self.get_cursor() as cursor:
            rows = cursor.execute(
                """
                SELECT id, alias FROM unit_aliases WHERE primary_unit_id = ?;
            """,
                (unit_id,),
            ).fetchall()
        return {row[0]: row[1] for row in rows}
    
    def update_unit_base(
        self,
        unit_id: int,
        unit_name: str,
        single_display_name: str,
        plural_display_name: str,
        unit_type: str,
    ) -> None:
        """Update a unit base."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE unit_base SET unit_name = ?, single_display_name = ?, plural_display_name = ?, unit_type = ? WHERE id = ?;
            """,
                (unit_name, single_display_name, plural_display_name, unit_type, unit_id),
            )

    def update_unit_alias(self, alias_id: int, alias: str) -> None:
        """Update a unit alias."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE unit_aliases SET alias = ? WHERE id = ?;
            """,
                (alias, alias_id),
            )

    def delete_unit_base(self, unit_id: int) -> None:
        """Delete a unit base."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM unit_base WHERE id = ?;
            """,
                (unit_id,),
            )

    def delete_unit_alias(self, alias_id: int) -> None:
        """Delete a unit alias."""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM unit_aliases WHERE id = ?;
            """,
                (alias_id,),
            )