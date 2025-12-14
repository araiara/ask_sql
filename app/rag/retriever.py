from langchain_chroma import Chroma
from app.config import CHROMA_DIR, get_embedding_function


def retrieve_schema_docs(question: str, top_k: int = 3) -> str:
    collection = Chroma(
        persist_directory=CHROMA_DIR,
        collection_name="schema_metadata",
        embedding_function=get_embedding_function(),
    )
    results = collection.similarity_search(query=question, k=top_k)
    docs_text: str = "\n".join([doc.page_content for doc in results])
    return docs_text
