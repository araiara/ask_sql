from typing import Any


def generate_semantic_docs(schema_dict: dict[str, dict[str, Any]]) -> dict[str, str]:
    semantic_docs: dict[str, str] = {}
    for table, meta in schema_dict.items():
        doc_text: str = (
            f"Table: {table}\nColumns: {meta['columns']}\nPrimary Keys: {meta['primary_keys']}\nForeign Keys: {meta['foreign_keys']}"
        )
        semantic_docs[table] = doc_text
    return semantic_docs
