from typing import Any
from psycopg2.extensions import connection


def extract_schema(conn: connection) -> dict[str, Any]:
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """
    )
    tables = [row[0] for row in cursor.fetchall()]

    schema = {}

    for table in tables:
        # Columns
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s;
        """,
            (table,),
        )
        columns = [r[0] for r in cursor.fetchall()]

        # Primary keys
        cursor.execute(
            """
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            WHERE tc.table_name = %s
              AND tc.constraint_type = 'PRIMARY KEY';
        """,
            (table,),
        )
        pks = [r[0] for r in cursor.fetchall()]

        # Foreign keys
        cursor.execute(
            """
            SELECT
                kcu.column_name,
                ccu.table_name AS foreign_table,
                ccu.column_name AS foreign_column
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tc.constraint_name
            WHERE tc.table_name = %s
              AND tc.constraint_type = 'FOREIGN KEY';
        """,
            (table,),
        )

        fks = [
            {"column": r[0], "references": f"{r[1]}.{r[2]}"} for r in cursor.fetchall()
        ]

        schema[table] = {"columns": columns, "primary_keys": pks, "foreign_keys": fks}

    cursor.close()
    return schema
