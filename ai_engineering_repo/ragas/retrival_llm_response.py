from langchain_community.vectorstores import Qdrant
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 1. Initialize your actual production RAG pipeline components
vector_db = Qdrant.from_existing_collection(
    collection_name="earnings_transcripts",
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
)
app_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Input queries
questions = [
    "What was NVIDIA's Data Center revenue in Q4 and what drove the growth?",
    "What is the company's outlook for Q1 gross margin?",
]

retrieved_contexts_list = []
responses_list = []

# 3. Execute RAG loop to collect live runtime telemetry
for query in questions:
    # A. FETCH CHUNKS FROM VECTOR DB
    docs = vector_db.similarity_search(query, k=2)
    raw_chunks = [doc.page_content for doc in docs]
    retrieved_contexts_list.append(raw_chunks)

    # B. GENERATE RESPONSE WITH APP LLM
    context_str = "\n".join(raw_chunks)
    prompt = f"Context:\n{context_str}\n\nQuestion: {query}\nAnswer:"
    answer = app_llm.invoke(prompt).content
    responses_list.append(answer)