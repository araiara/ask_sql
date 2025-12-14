import os
import boto3
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection
from langchain_aws import BedrockEmbeddings

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


def get_bedrock_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )


def get_embedding_function():
    return BedrockEmbeddings(
        client=get_bedrock_client(),
        model_id="amazon.titan-embed-text-v2:0",
    )
