from app.rag.retriever import retrieve_schema_docs
from app.rag.sql_generator import generate_sql
from app.rag.executor import execute_sql


def run_rag_pipeline() -> None:
    while True:
        question: str = input("Enter your question: ")
        docs: str = retrieve_schema_docs(question)

        sql_query: str = generate_sql(question, docs)
        print("\nGenerated SQL Query:\n")
        print(sql_query)

        user_confirmation = input("\nDo you want to execute this SQL query? (y/n): ")
        if user_confirmation.lower() == "y":
            try:
                result = execute_sql(sql_query)
                print("\nSQL Execution Result:\n")
                print(result)
            except Exception as e:
                print(f"\nSQL query execution failed: {str(e)}")
        else:
            print("SQL execution aborted by the user.")

        continue_prompt = input("\nDo you want to ask another question? (y/n): ")
        if continue_prompt.lower() != "y":
            print("Thank you for using the SQL Assistant. Goodbye!")
            break


if __name__ == "__main__":
    run_rag_pipeline()
