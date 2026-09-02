from enum import Enum

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field


# Load variables from .env
load_dotenv()


# Possible sentiment values
class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


# Structure we want Gemini to return
class SentimentResult(BaseModel):
    sentiment: Sentiment
    confidence: float = Field(ge=0, le=1)
    explanation: str


# Create Gemini client
# It automatically picks up GOOGLE_API_KEY
client = genai.Client()


# Example news article
article = """
Apple reported record quarterly revenue driven by strong iPhone sales
and growing demand for its services business. The company's profits
also exceeded Wall Street expectations.
"""


# Ask Gemini to analyze the article
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=f"""
Determine the sentiment of this news article.

Classify it as positive, negative, or neutral.

Article:
{article}
""",
    config={
        "response_mime_type": "application/json",
        "response_schema": SentimentResult,
    },
)


# Convert Gemini's JSON response into our Pydantic model
result = SentimentResult.model_validate_json(response.text)


# Use the result
print("Sentiment:", result.sentiment.value)
print("Confidence:", result.confidence)
print("Explanation:", result.explanation)