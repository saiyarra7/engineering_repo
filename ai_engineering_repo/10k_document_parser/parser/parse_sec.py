from __future__ import annotations

from pathlib import Path
from typing import Any
import warnings

from bs4 import MarkupResemblesLocatorWarning

try:
    from sec_parser import Edgar10QParser
except ImportError as exc:  # pragma: no cover - runtime import guard
    raise ImportError("sec-parser is required. Install it with pip install -r requirements.txt") from exc


def parse_html(file_path: Path) -> list[dict[str, Any]]:
    """Parse an SEC HTML filing and return a list of structured elements."""
    if not file_path.exists():
        raise FileNotFoundError(f"HTML file not found: {file_path}")

    try:
        warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
        parser = Edgar10QParser()
        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
            parsed_tree = parser.parse(handle)
    except Exception as exc:  # pragma: no cover - runtime guard
        raise RuntimeError(f"Failed to parse filing: {exc}") from exc

    elements: list[dict[str, Any]] = []
    node_list: list[Any] = []

    if hasattr(parsed_tree, "iter_nodes"):
        node_list = list(parsed_tree.iter_nodes())
    elif hasattr(parsed_tree, "children"):
        node_list = list(parsed_tree.children)
    elif isinstance(parsed_tree, (list, tuple)):
        node_list = list(parsed_tree)

    for index, element in enumerate(node_list):
        element_type = getattr(element, "tag", None) or getattr(element, "type", None) or getattr(element, "__class__", None)
        text = getattr(element, "text", None)
        if text is None:
            text = getattr(element, "content", None)
        if text is None and hasattr(element, "to_text"):
            text = element.to_text()

        if text is None:
            continue

        cleaned_text = str(text).strip()
        if not cleaned_text:
            continue

        elements.append(
            {
                "element_index": index,
                "element_type": str(element_type),
                "text": cleaned_text,
            }
        )

    return elements
