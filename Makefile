.PHONY: build seed embed rag all clean

build:
	@echo "🔨 Building Docker image..."
	docker build -t sql-genai-app .

seed: build
	@echo "🌱 Seeding database..."
	docker run --rm -it \
		--env-file .env \
		--network host \
		-v $$(pwd)/app:/app/app \
		sql-genai-app \
		python -m app.seed_db

embed: build
	@echo "Running Schema Embedding..."
	docker run --rm -it \
		--env-file .env \
		--network host \
		-v $$(pwd)/app:/app/app \
		-v $$(pwd)/chroma_db:/app/chroma_db \
		sql-genai-app \
		python -m app.embed

run: build
	@echo "Running RAG + SQL Executor..."
	docker run --rm -it \
		--env-file .env \
		--network host \
		-v $$(pwd)/app:/app/app \
		-v $$(pwd)/chroma_db:/app/chroma_db \
		sql-genai-app \
		python -m app.run

all: embed rag

clean:
	@echo "Removing Docker image..."
	docker rmi sql-genai-app || true
