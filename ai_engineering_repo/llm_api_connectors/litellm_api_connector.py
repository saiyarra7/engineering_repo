import os
import litellm
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

# model="gemini/gemini-3.1-flash-lite"
# model="gemini/gemini-3.5-flash"
# model="groq/llama-3.1-8b-instant"
response = completion(
    model="gemini/gemini-3.1-flash-lite",
    messages=[
        {
            "role": "user",
            "content": "return the exact model name that is being used and the infra provider being used. Are you running on groq or other inference provider?"
        }
    ]
)

print(response.choices[0].message.content)


