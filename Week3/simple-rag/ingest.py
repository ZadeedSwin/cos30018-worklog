"""Part 1 - Ingestion: file -> chunk -> embed -> Pinecone.

Usage:
  python ingest.py                          # lab default: 200/20, namespace week3-code-lab
  python ingest.py --chunk-size 100 --namespace week3-code-100   # Experiment B
"""
import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pinecone import Pinecone

load_dotenv(override=True)  # .env wins over old terminal variables

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX")

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSION = 1024

parser = argparse.ArgumentParser()
parser.add_argument("--chunk-size", type=int, default=200)
parser.add_argument("--overlap", type=int, default=20)
parser.add_argument("--namespace", default="week3-code-lab")
args = parser.parse_args()
NAMESPACE = args.namespace

if not all([GEMINI_API_KEY, PINECONE_API_KEY, INDEX_NAME]):
    raise ValueError("Missing GEMINI_API_KEY, PINECONE_API_KEY, or PINECONE_INDEX in .env")

gemini = genai.Client(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)


def chunk_text(text: str, chunk_size: int = 200, overlap: int = 20) -> list[str]:
    """Split text into overlapping word-based chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(words), step):
        end = start + chunk_size
        chunk_words = words[start:end]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if end >= len(words):
            break
    return chunks


def embed_text(text: str) -> list[float]:
    result = gemini.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIMENSION),
    )
    return result.embeddings[0].values


# Make: Google Drive -> Download a File
file_path = Path("data/intelligent_agents_overview.txt")
if not file_path.exists():
    raise FileNotFoundError(f"Cannot find {file_path}. Put the lab text file inside the data folder.")
text = file_path.read_text(encoding="utf-8")
print(f"Loaded: {file_path.name}")
print(f"Characters: {len(text)}")

# Make: AI Toolkit -> Chunk text
chunks = chunk_text(text, chunk_size=args.chunk_size, overlap=args.overlap)
print(f"Chunk size {args.chunk_size}, overlap {args.overlap} -> created {len(chunks)} chunks")
print(f"Namespace: {NAMESPACE}")

# Make: Iterator -> Gemini embeddings -> Pinecone upsert
for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i + 1}/{len(chunks)}")
    vector = embed_text(chunk)
    index.upsert(
        namespace=NAMESPACE,
        vectors=[
            {
                "id": f"{file_path.name}-chunk-{i}",
                "values": vector,
                "metadata": {
                    "text": chunk,
                    "source": file_path.name,
                    "chunk_number": i,
                },
            }
        ],
    )

print("Ingestion complete.")
