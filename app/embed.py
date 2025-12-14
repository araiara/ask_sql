from app.config import get_postgres_connection
from app.embedding.schema_extractor import extract_schema
from app.embedding.doc_generator import generate_semantic_docs
from app.embedding.embed import embed_documents_to_chroma


def run_embedding_pipeline() -> None:
    conn = get_postgres_connection()
    schema_dict = extract_schema(conn)
    conn.close()
    semantic_docs = generate_semantic_docs(schema_dict)

    embed_documents_to_chroma(semantic_docs)
    print("Embedding pipeline completed successfully.")


if __name__ == "__main__":
    run_embedding_pipeline()
