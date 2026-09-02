"""
Intent classifier using OpenAI Structured Outputs.

The OpenAI SDK automatically:

1. Converts the Pydantic model into JSON Schema.
2. Sends it to the model.
3. Validates the response.
4. Returns a populated Pydantic object.

No json.loads() required.
"""

from openai import OpenAI

from router.models import IntentResponse
from router.prompts import SYSTEM_PROMPT

client = OpenAI()


def classify_intent(query: str) -> IntentResponse:
    """
    Classify which backend should answer
    the user's question.
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-5-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        response_format=IntentResponse,
    )

    message = completion.choices[0].message

    if message.refusal:
        raise RuntimeError(message.refusal)

    return message.parsed