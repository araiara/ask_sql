from app.rag.retriever import retrieve_schema_docs
from app.rag.sql_generator import generate_sql
from app.rag.executor import execute_sql


def run_rag_pipeline() -> None:
    question: str = input("Enter your question: ")
    docs: str = retrieve_schema_docs(question)

    sql_query: str = generate_sql(question, docs)
    print("\n✅ Generated SQL Query:\n")
    print(sql_query)

    user_confirmation = input("\nDo you want to execute this SQL query? (y/n): ")
    if user_confirmation.lower() == "y":
        result = execute_sql(sql_query)
        print("\n✅ SQL Execution Result:\n")
        print(result)
    else:
        print("SQL execution aborted by the user.")
        return


if __name__ == "__main__":
    run_rag_pipeline()
