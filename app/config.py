import os
import boto3
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection
from langchain_aws import BedrockEmbeddings

from app.rag.schema_extractor import extract_schema

load_dotenv()

CHROMA_DIR: str = os.path.join(os.path.dirname(__file__), "../chroma_db")


def get_postgres_connection() -> connection:
    return psycopg2.connect(
        host=os.getenv("SOURCE_DB_HOST"),
        database=os.getenv("SOURCE_DB_NAME"),
        user=os.getenv("SOURCE_DB_USER"),
        password=os.getenv("SOURCE_DB_PASSWORD"),
        port=os.getenv("SOURCE_DB_PORT"),
    )


def get_bedrock_client() -> boto3.client:
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )


def get_embedding_function() -> BedrockEmbeddings:
    return BedrockEmbeddings(
        client=get_bedrock_client(),
        model_id="amazon.titan-embed-text-v2:0",
    )


def generate_authoritative_schema() -> str:
    with get_postgres_connection() as conn:
        schema_dict = extract_schema(conn)

    lines = ["AUTHORITATIVE DATABASE SCHEMA (DO NOT INVENT):\n"]

    for table, meta in schema_dict.items():
        lines.append(f"{table}(")
        for col in meta["columns"]:
            suffix = ""
            if col in meta["primary_keys"]:
                suffix = " PK"
            for fk in meta["foreign_keys"]:
                if fk["column"] == col:
                    suffix = f" FK → {fk['references']}"
            lines.append(f"  {col}{suffix},")
        lines.append(")\n")

    lines.append(
        "Revenue definition:\n"
        "SUM(order_items.quantity * order_items.unit_price)\n"
        "Only include orders.status = 'completed'\n"
    )

    return "\n".join(lines)
