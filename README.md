# SQL RAG System

A Retrieval-Augmented Generation (RAG) system that converts natural language questions into SQL queries using AWS Bedrock and ChromaDB.

## Overview

This system extracts database schema metadata, embeds it into a vector database, and uses semantic search with LLMs to generate accurate SQL queries from natural language questions.

## Architecture

```
┌─────────────────┐
│  PostgreSQL DB  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ Schema Extract  │────▶│  ChromaDB    │
└─────────────────┘      └──────┬───────┘
                                │
                                │ Semantic Search
                                ▼
                         ┌──────────────┐
                         │  AWS Bedrock │
                         │  (Nova Lite) │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │  SQL Query   │
                         └──────────────┘
```

## Prerequisites

- Docker and Docker Compose
- AWS credentials with Bedrock access
- Make (optional, for simplified commands)

## Setup

### Create environment file

Create a `.env` file in the project root:

```env
cp .env.example .env
```

### Start PostgreSQL

```bash
docker-compose up -d
```

### Build Docker image

```bash
make build
```

## Usage

### Seed the Database

Populate the database with sample data:

```bash
make seed
```

This creates tables: `categories`, `products`, `customers`, `orders`, and `order_items`.

### Run Schema Embedding

Extract database schema and embed it into ChromaDB:

```bash
make embed
```

This process:
1. Connects to PostgreSQL
2. Extracts table schemas (columns, types, primary keys, foreign keys)
3. Generates semantic documentation
4. Embeds documents into ChromaDB using AWS Bedrock Titan embeddings

### Run RAG Query System

Ask natural language questions about your database:

```bash
make rag
```

Examples:
- "Show me the top 5 most expensive products"
- "What is the total revenue from completed orders?"
- "List all customers who made purchases in December"

### Run Complete Pipeline

Execute both embedding and RAG in sequence:

```bash
make all
```

### Clean Up

Remove Docker image:

```bash
make clean
```

## Workflow

### 1. **Database Seeding** (`app/seed_db.py`)
- Creates sample e-commerce database schema
- Inserts test data for products, customers, orders

### 2. **Schema Extraction** (`app/embedding/schema_extractor.py`)
- Queries PostgreSQL `information_schema`
- Extracts tables, columns, data types, constraints
- Identifies primary keys and foreign key relationships

### 3. **Document Generation** (`app/embedding/doc_generator.py`)
- Converts schema metadata into semantic text documents
- Formats information for embedding

### 4. **Embedding** (`app/embedding/embed.py`)
- Uses AWS Bedrock Titan embeddings (1024 dimensions)
- Stores vectors in ChromaDB for semantic retrieval
- Creates persistent collection: `schema_metadata`

### 5. **RAG Pipeline** (`app/run.py`)

   **a. Retrieval** (`app/rag/retriever.py`)
   - Takes user's natural language question
   - Performs semantic similarity search in ChromaDB
   - Retrieves top-k relevant schema documents

   **b. SQL Generation** (`app/rag/sql_generator.py`)
   - Sends question + retrieved schema to AWS Bedrock Nova Lite
   - LLM generates PostgreSQL query
   - Cleans markdown formatting from response

   **c. Execution** (`app/rag/executor.py`)
   - Executes generated SQL against PostgreSQL
   - Returns query results or error messages

## Project Structure

```
sql-genai/
├── app/
│   ├── config.py              # Configuration and connections
│   ├── embed.py               # Embedding pipeline entry point
│   ├── run.py                 # RAG pipeline entry point
│   ├── seed_db.py             # Database seeding script
│   ├── embedding/
│   │   ├── schema_extractor.py   # Extract DB schema
│   │   ├── doc_generator.py      # Generate semantic docs
│   │   └── embed.py               # Embed to ChromaDB
│   └── rag/
│       ├── retriever.py           # Semantic search
│       ├── sql_generator.py       # LLM SQL generation
│       └── executor.py            # SQL execution
├── chroma_db/                 # Vector database storage
├── docker-compose.yml         # PostgreSQL service
├── Dockerfile                 # Application container
├── Makefile                   # Build and run commands
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables
```

## Technologies

- **LangChain**: RAG framework and LLM orchestration
- **AWS Bedrock**: Titan embeddings + Nova Lite LLM
- **ChromaDB**: Vector database for semantic search
- **PostgreSQL**: Source database
- **psycopg2**: PostgreSQL adapter
- **Docker**: Containerization
