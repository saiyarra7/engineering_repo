import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatLiteLLM

load_dotenv()

# Pass model routing string directly
llm = ChatLiteLLM(model="gemini/gemini-2.5-flash")
# llm = ChatLiteLLM(model="groq/llama-3.1-8b-instant")

prompt = "return the exact model name that is being used and the infra provider being used. Are you running on groq or other inference provider?"

response = llm.invoke(prompt)

print(response.content)