import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# OpenRouter automatically failovers down this list if the first model returns a 429
response = client.chat.completions.create(
    model="openrouter/free",  # Default auto-router entrypoint
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "Hello! Explain what an API is in one short sentence."},
    ],
    extra_body={
        "models": [
            "openai/gpt-oss-20b:free",
            "meta-llama/llama-3.3-70b-instruct:free",
            "google/gemma-4-31b-it:free",
        ]
    },
)

print(f"Model used: {response.model}")
print(f"Response: {response.choices[0].message.content}")