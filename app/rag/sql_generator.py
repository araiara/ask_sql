from langchain_aws import ChatBedrock
from langchain_core.prompts import PromptTemplate
from app.config import get_bedrock_client


def generate_sql(question: str, retrieved_docs: str) -> str:
    llm = ChatBedrock(
        client=get_bedrock_client(), model_id="amazon.nova-pro-v1:0", temperature=0
    )

    prompt_template: str = """
You are an expert SQL engineer.

Rules:
1. Always use explicit JOINs
2. Use foreign key relationships provided
3. Revenue = SUM(order_items.quantity * order_items.unit_price)
4. Only include completed orders
5. If information is missing, ask for clarification

Database schema:
{schema_docs}

User question:
{question}

Write a correct Postgres SQL query. Only return SQL, no explanations.
Make sure the generated query is syntactically correct.

SQL Query:
"""
    prompt = PromptTemplate(
        input_variables=["schema_docs", "question"], template=prompt_template
    )
    chain = prompt | llm
    response = chain.invoke({"schema_docs": retrieved_docs, "question": question})
    sql_query: str = response.content.strip()

    # Remove markdown code fences if present
    if sql_query.startswith("```"):
        sql_query = sql_query.split("\n", 1)[1]  # Remove first line with ```sql
        sql_query = sql_query.rsplit("```", 1)[0]  # Remove closing ```
        sql_query = sql_query.strip()

    return sql_query
