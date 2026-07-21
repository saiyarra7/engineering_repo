import os
import litellm
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

# model="gemini/gemini-3.1-flash-lite"
# model="gemini/gemini-3.5-flash"
response = completion(
    model="gemini/gemini-3.1-flash-lite",
    messages=[
        {
            "role": "user",
            "content": "test"
        }
    ]
)

print(response.choices[0].message.content)


