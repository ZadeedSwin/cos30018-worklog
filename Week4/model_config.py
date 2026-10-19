"""
COS30018 Week 4 - one place to configure the language model.
Every script in this lab imports get_model() from here, so you can swap the
backend for the whole system by changing one environment variable.
"""
import os
from dotenv import load_dotenv
from smolagents import InferenceClientModel, OpenAIModel

load_dotenv()

# Gemini exposes an OpenAI-compatible endpoint, so smolagents' OpenAIModel can
# talk to it directly. No extra SDK is needed.
GEMINI_OPENAI_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"

# A stronger model for the agent that plans, a cheaper one for the agents that
# just fetch and compute. Check the current ids at
# https://ai.google.dev/gemini-api/docs/models before each semester.
MANAGER_MODEL_ID = "gemini-3.7-flash"
WORKER_MODEL_ID = "gemini-3.5-flash-lite"


def get_model(role: str = "worker", backend: str | None = None):
    """Return a smolagents model.

    Args:
        role: 'manager' for the planning agent, 'worker' for sub-agents.
        backend: 'gemini' (default) or 'hf' to fall back to the Week 2 setup.
    """
    backend = (backend or os.getenv("MODEL_BACKEND", "gemini")).lower()
    if backend == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")
        return OpenAIModel(
            model_id=MANAGER_MODEL_ID if role == "manager" else WORKER_MODEL_ID,
            api_base=GEMINI_OPENAI_BASE,
            api_key=api_key,
            temperature=0.2,
            requests_per_minute=10,  # stay inside the free-tier limit
        )
    if backend == "hf":
        # Exactly the model class you used in Week 2.
        return InferenceClientModel()
    raise ValueError(f"Unknown MODEL_BACKEND '{backend}'. Use 'gemini' or 'hf'.")
