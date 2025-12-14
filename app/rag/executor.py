from typing import Any
from app.config import get_postgres_connection


def execute_sql(sql_query: str) -> list[tuple[Any, ...]] | str:
    conn = get_postgres_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        if sql_query.strip().lower().startswith("select"):
            rows: list[tuple[Any, ...]] = cursor.fetchall()
            return rows
        else:
            conn.commit()
            return f"Query executed successfully: {cursor.rowcount} rows affected."
    except Exception as e:
        return f"SQL execution error: {e}"
    finally:
        cursor.close()
        conn.close()
