from app.embedding.semantic_docs import get_semantic_docs
from app.embedding.embed import embed_documents_to_chroma


def run_embedding_pipeline() -> None:
    semantic_docs = get_semantic_docs()
    embed_documents_to_chroma(semantic_docs)
    print("Embedding pipeline completed successfully.")


if __name__ == "__main__":
    run_embedding_pipeline()
