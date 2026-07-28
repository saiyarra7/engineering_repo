#https://console.groq.com/docs/models
import requests
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()
completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
      {
        "role": "user",
        "content": "return the exact model name that is being used and the infra provider being used. Are you running on groq or other inference provider?\n"
      }
    ],
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
