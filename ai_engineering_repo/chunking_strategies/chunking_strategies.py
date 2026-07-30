#7. Semantic Chunking (LlamaIndex)

"""
Semantic chunking groups text based on meaning instead of
fixed sizes.

Instead of splitting every N characters, embeddings are
generated for sentences or paragraphs. Similar neighboring
sentences are merged into the same chunk, while topic changes
start a new chunk.

Pros:
    - Best retrieval quality
    - Preserves semantic context
    - Excellent for enterprise RAG

Cons:
    - Slower than rule-based chunking
    - Requires embedding generation during indexing
"""

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding(
    model="text-embedding-3-small"
)

splitter = SemanticSplitterNodeParser(
    embed_model=embed_model
)

nodes = splitter.get_nodes_from_documents(documents)



#6. LangChain Recursive Chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter

"""
Recursive chunking attempts to preserve larger document
structures before falling back to smaller ones.

Split priority:

    Paragraph
        ↓
    Line
        ↓
    Sentence
        ↓
    Word
        ↓
    Character

This is a good general-purpose chunker but does not understand
document semantics or topic boundaries.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=100,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

chunks = splitter.split_text(text)



#5. Markdown / Heading Chunking
import re

def markdown_heading_chunker(text):
    """
    Split a document based on Markdown headings.

    This works well for documentation, SEC filings,
    technical reports, and any structured document.

    Each heading becomes the start of a new chunk,
    preserving the document hierarchy.

    Example:

        # Manufacturing
        ...

        # Clinical Trials
        ...

        # Pipeline
        ...

    Returns:
        List of section-based chunks.
    """

    pattern = r"(?=^#{1,6}\s)"

    chunks = re.split(
        pattern,
        text,
        flags=re.MULTILINE
    )

    return [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]


#Token chunking
import tiktoken

def token_chunker(
    text: str,
    model: str = "text-embedding-3-small",
    max_tokens: int = 400
):
    """
    Split text using tokenizer tokens instead of characters.

    Embedding models operate on tokens rather than characters,
    making this approach more accurate than character-based
    chunking.

    Pros:
        - Consistent chunk sizes
        - Matches embedding model limits
        - Common production approach

    Cons:
        - Can still split sentences
        - Requires tokenizer dependency
    """

    encoding = tiktoken.encoding_for_model(model)

    tokens = encoding.encode(text)

    chunks = []

    for i in range(0, len(tokens), max_tokens):

        chunk_tokens = tokens[i:i + max_tokens]

        chunks.append(
            encoding.decode(chunk_tokens)
        )

    return chunks


#Sentence window

from nltk.tokenize import sent_tokenize

def sentence_window_chunker(
    text: str,
    max_chars: int = 600
):
    """
    Build chunks by combining consecutive sentences until a
    maximum chunk size is reached.

    Unlike character chunking, this approach preserves complete
    sentences, resulting in more coherent chunks and better
    embedding quality.

    This is a common production strategy for news articles,
    scientific literature, and general RAG systems.

    Args:
        text: Input document.
        max_chars: Approximate maximum characters per chunk.

    Returns:
        List of sentence-based chunks.
    """

    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        # Add sentence if the chunk is still within the size limit
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += " " + sentence

        else:
            # Save completed chunk
            chunks.append(current_chunk.strip())

            # Start a new chunk
            current_chunk = sentence

    # Add the final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# Paragraph chunking

def paragraph_chunker(text: str):
    """
    Split a document using paragraph boundaries.

    Paragraphs usually represent a single topic or idea, making this
    approach significantly better than fixed character chunking for
    news articles, blogs, documentation, and reports.

    Assumes paragraphs are separated by blank lines.

    Pros:
        - Preserves logical structure
        - Better semantic coherence
        - Very simple implementation

    Cons:
        - Paragraphs can be extremely long
        - Paragraph lengths are inconsistent
    """

    paragraphs = text.split("\n\n")

    # Remove empty paragraphs
    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]

#1. Fixed Character Chunking

from typing import List

def fixed_character_chunker(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> List[str]:
    """
    Split a document into fixed-size character chunks.

    This is the simplest chunking strategy and is useful for quick
    proof-of-concepts. Chunks are created purely based on character
    count and do not consider sentence or paragraph boundaries.

    Pros:
        - Very fast
        - No external dependencies
        - Easy to implement

    Cons:
        - Can split sentences or words in half
        - May reduce embedding quality and retrieval accuracy

    Args:
        text: Input document.
        chunk_size: Maximum number of characters per chunk.
        overlap: Number of overlapping characters between chunks.

    Returns:
        List of text chunks.
    """

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Store the current chunk
        chunks.append(text[start:end])

        # Move the window forward while preserving overlap
        start += chunk_size - overlap

    return chunks