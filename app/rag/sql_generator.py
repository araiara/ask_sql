from langchain_aws import ChatBedrock
from langchain_core.prompts import PromptTemplate

from app.config import LLM_MODEL_ID, get_bedrock_client


PROMPT_TEMPLATE = """
You are an expert SQL engineer.

RULES (MANDATORY):
- Use ONLY tables and columns listed in the schema.
- Do NOT invent columns or tables.
- Use explicit JOINs via foreign keys.
- Revenue = SUM(order_items.quantity * order_items.unit_price)
- If information is missing, say “schema does not support this query.”
- Validate join paths using foreign keys.
- For queries unrelated to ecommerce sql generator, give a generic answer without taking any provided schema context.

AUTHORITATIVE SCHEMA:
{schema}

SEMANTIC CONTEXT (for reasoning only):
{context}

USER QUESTION:
{question}

Return ONLY valid PostgreSQL SQL, no explanations.
"""


def generate_sql(question: str, retrieved_docs: str, authoritative_schema: str) -> str:
    llm = ChatBedrock(client=get_bedrock_client(), model_id=LLM_MODEL_ID, temperature=0)

    prompt = PromptTemplate(
        input_variables=["schema", "context", "question"], template=PROMPT_TEMPLATE
    )
    chain = prompt | llm
    response = chain.invoke(
        {
            "schema": authoritative_schema,
            "context": retrieved_docs,
            "question": question,
        }
    )
    sql_query: str = response.content.strip()

    # Remove markdown code fences if present
    if sql_query.startswith("```"):
        sql_query = sql_query.split("\n", 1)[1]  # Remove first line with ```sql
        sql_query = sql_query.rsplit("```", 1)[0]  # Remove closing ```
        sql_query = sql_query.strip()

    return sql_query
