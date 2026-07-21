from qdrant_client import QdrantClient, models

# 1. CONNECT to Qdrant running in Docker
client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "tech_knowledge_base"
MODEL_NAME = "BAAI/bge-small-en-v1.5"  # Fast, accurate 384-dim CPU embedding model

# 2. CREATE COLLECTION
if client.collection_exists(COLLECTION_NAME):
    client.delete_collection(COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=client.get_embedding_size(MODEL_NAME),
        distance=models.Distance.COSINE,
    ),
)
print(f"Collection '{COLLECTION_NAME}' created.")

# 3. PREPARE DOCUMENTS
documents = [
    "Polars is a high-performance, fast DataFrame library written in Rust.",
    "DuckDB is an in-process SQL OLAP database management system for analytics.",
    "Qdrant is a vector database built in Rust for neural network semantic search.",
    "PySpark provides Python API bindings for Apache Spark distributed computing.",
    "The golden retriever is a popular dog breed known for its friendly nature.",
]

# Wrap text into Qdrant Document objects for automatic embedding generation
docs_to_upload = [
    models.Document(text=doc, model=MODEL_NAME) for doc in documents
]

payloads = [
    {"text_content": doc, "category": "tech" if i < 4 else "animals"}
    for i, doc in enumerate(documents)
]

# 4. UPSERT INTO QDRANT
client.upload_collection(
    collection_name=COLLECTION_NAME,
    vectors=docs_to_upload,
    payload=payloads,
    ids=list(range(1, len(documents) + 1)),
)
print(f"Successfully embedded and stored {len(documents)} documents.")

# 5. RUN A SEMANTIC SEARCH QUERY
user_query = "What tools can I use for fast data processing and dataframes?"

print(f"\nSearching for: '{user_query}'")

search_results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=models.Document(text=user_query, model=MODEL_NAME),
    limit=2,  # Return Top 2 nearest vector matches
).points

print("\n=== TOP RESULTS ===")
for hit in search_results:
    print(f"Score: {hit.score:.4f} | Text: {hit.payload['text_content']}")