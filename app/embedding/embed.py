from langchain_chroma import Chroma

from app.config import CHROMA_DIR, get_embedding_function


def embed_documents_to_chroma(semantic_docs: dict[str, str]) -> Chroma:
    embeddings = get_embedding_function()

    collection = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name="schema_metadata",
        embedding_function=embeddings,
    )

    texts: list[str] = list(semantic_docs.values())
    metadatas: list[dict[str, str]] = [{"table_name": t} for t in semantic_docs.keys()]
    collection.add_texts(texts=texts, metadatas=metadatas)
    return collection
