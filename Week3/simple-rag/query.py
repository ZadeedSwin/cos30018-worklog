"""Part 2 - Query: question -> embed -> Pinecone search -> context -> Gemini -> answer.

Usage:
  python query.py                       # lab default: top-k 3, namespace week3-code-lab
  python query.py --top-k 1             # Experiment A (also try 5)
  python query.py --namespace week3-code-100   # Experiment B
"""
import argparse
import os

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
GENERATION_MODEL = "gemini-3.6-flash"

parser = argparse.ArgumentParser()
parser.add_argument("--top-k", type=int, default=3)
parser.add_argument("--namespace", default="week3-code-lab")
parser.add_argument("--model", default="gemini-3.6-flash")  # switch if a model is busy (503)
args = parser.parse_args()
NAMESPACE = args.namespace
TOP_K = args.top_k
GENERATION_MODEL = args.model

if not all([GEMINI_API_KEY, PINECONE_API_KEY, INDEX_NAME]):
    raise ValueError("Missing GEMINI_API_KEY, PINECONE_API_KEY, or PINECONE_INDEX in .env")

gemini = genai.Client(api_key=GEMINI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)


def embed_text(text: str) -> list[float]:
    result = gemini.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=EMBEDDING_DIMENSION),
    )
    return result.embeddings[0].values


# Make: Tools -> Set variable
question = input("Ask a question: ").strip()
if not question:
    raise ValueError("Question cannot be empty")
print(f"Namespace: {NAMESPACE} | TOP_K: {TOP_K} | Model: {GENERATION_MODEL}")

# Make: Gemini -> Generate embeddings
query_vector = embed_text(question)
print(f"Query embedding dimensions: {len(query_vector)}")

# Make: Pinecone -> Search with a query
results = index.query(
    namespace=NAMESPACE,
    vector=query_vector,
    top_k=TOP_K,
    include_metadata=True,
    include_values=False,
)

print("\nRetrieved chunks:")
context_parts = []
for rank, match in enumerate(results.matches, start=1):
    text = match.metadata.get("text", "")
    source = match.metadata.get("source", "unknown")
    print("\n--------------------")
    print(f"Rank: {rank}")
    print(f"ID: {match.id}")
    print(f"Score: {match.score:.4f}")
    print(f"Source: {source}")
    print(f"Text: {text[:300]}")
    if text:
        context_parts.append(text)

if not context_parts:
    print("\nNo context was retrieved from Pinecone.")
    raise SystemExit(1)

# Make: Tools -> Text aggregator
context = "\n\n---\n\n".join(context_parts)

# Make: Gemini -> Generate a response
# Lab uses gemini.interactions.create(); google-genai on Python 3.9 doesn't have it,
# so we use the equivalent generate_content() call. Same prompt, same grounding rule.
response = gemini.models.generate_content(
    model=GENERATION_MODEL,
    contents=f"CONTEXT:\n{context}\n\nQUESTION:\n{question}",
    config=types.GenerateContentConfig(
        system_instruction=(
            "Answer the user's question using only the supplied context. "
            "If the context does not contain enough information, say: "
            "'I don't have enough information in the provided documents.'"
        ),
    ),
)
answer = response.text

# Make: Tools -> Get variable
print("\n====================")
print("FINAL ANSWER")
print("====================")
print(answer)
