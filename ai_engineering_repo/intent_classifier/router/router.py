"""
Central routing logic.

Given a user question:

1. Determine intent.
2. Route to the appropriate backend.
"""

from router.classifier import classify_intent
from router.models import DataSource


def route_query(query: str):

    intent = classify_intent(query)

    print("=" * 50)
    print("Intent Classification")
    print("=" * 50)

    print(f"Datasource : {intent.datasource}")
    print(f"Confidence : {intent.confidence:.2f}")
    print(f"Reasoning  : {intent.reasoning}")

    print()

    match intent.datasource:

        case DataSource.DUCKDB:
            return execute_duckdb(query)

        case DataSource.QDRANT:
            return execute_qdrant(query)

        case DataSource.GRAPH:
            return execute_graph(query)

        case DataSource.HYBRID:
            return execute_hybrid(query)

        case _:
            raise ValueError("Unknown datasource")


def execute_duckdb(query):
    print("Executing DuckDB")
    return "duckdb"


def execute_qdrant(query):
    print("Executing Qdrant")
    return "qdrant"


def execute_graph(query):
    print("Executing Graph")
    return "graph"


def execute_hybrid(query):
    print("Executing Hybrid Pipeline")
    return "hybrid"