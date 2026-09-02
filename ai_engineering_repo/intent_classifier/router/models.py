"""
Pydantic models used by the intent router.

The LLM is constrained to generate one of these values.
No manual JSON parsing is required.
"""

from enum import Enum

from pydantic import BaseModel, Field


class DataSource(str, Enum):
    DUCKDB = "duckdb"
    QDRANT = "qdrant"
    GRAPH = "graph"
    HYBRID = "hybrid"


class IntentResponse(BaseModel):
    """
    Output returned by the LLM.

    datasource:
        Backend responsible for answering the query.

    confidence:
        Confidence score between 0 and 1.

    reasoning:
        Short explanation for debugging/logging.
    """

    datasource: DataSource

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score."
    )

    reasoning: str