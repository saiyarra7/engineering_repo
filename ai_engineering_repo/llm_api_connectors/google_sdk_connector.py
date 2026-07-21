import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
Client automatically reads os.environ.get("GEMINI_API_KEY")
client = genai.Client()

for model in client.models.list():
    if "gemini" in model.name:
        print(model.name)