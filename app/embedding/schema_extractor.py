from typing import Any
from psycopg2.extensions import connection


def extract_schema(conn: connection) -> dict[str, dict[str, Any]]:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public';
        """
        )
        tables = [row[0] for row in cursor.fetchall()]

        schema_dict = {}
        for table in tables:
            cursor.execute(
                f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name='{table}';
            """
            )
            columns = [
                {"name": r[0], "type": r[1], "nullable": r[2]}
                for r in cursor.fetchall()
            ]

            # Primary keys
            cursor.execute(
                f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_name='{table}' AND tc.constraint_type='PRIMARY KEY';
            """
            )
            pks = [r[0] for r in cursor.fetchall()]

            # Foreign keys
            cursor.execute(
                f"""
                SELECT kcu.column_name, ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                WHERE tc.table_name='{table}' AND tc.constraint_type='FOREIGN KEY';
            """
            )
            fks = [
                {"column": r[0], "references": f"{r[1]}.{r[2]}"}
                for r in cursor.fetchall()
            ]

            schema_dict[table] = {
                "columns": columns,
                "primary_keys": pks,
                "foreign_keys": fks,
            }

    return schema_dict
