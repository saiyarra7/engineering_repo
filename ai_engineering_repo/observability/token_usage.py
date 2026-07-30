#1. Extract Directly from API Responses
import openai

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain vector indexing."}],
)

# Extract token counts
prompt_tokens = response.usage.prompt_tokens
completion_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens

print(f"Input: {prompt_tokens} | Output: {completion_tokens} | Total: {total_tokens}")


#2. Auto-Tracing via MLOps Frameworks

import mlflow

# Enable automatic tracing for your provider/framework (OpenAI, LangChain, LlamaIndex, etc.)
mlflow.openai.autolog()  # or mlflow.langchain.autolog()

# Execution automatically logs token usage & calculated USD cost to the MLflow server
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Query execution plan optimization"}],
)

#Using LangChain Callback Handlers
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

with get_openai_callback() as cb:
    response = llm.invoke("What is a bloom filter?")
    print(f"Tokens: {cb.total_tokens} (Prompt: {cb.prompt_tokens}, Completion: {cb.completion_tokens})")
    print(f"Cost USD: ${cb.total_cost:.6f}")


# 3. Pre-Inference Estimation (Client-Side)

import tiktoken

# Load the encoding matching the target model
encoding = tiktoken.encoding_for_model("gpt-4o")

prompt = "SELECT * FROM large_table WHERE status = 'active'"
token_count = len(encoding.encode(prompt))

print(f"Estimated Input Tokens: {token_count}")