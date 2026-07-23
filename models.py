"""Configuración de modelos de lenguaje y embeddings."""

from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq

from keys import COHERE_API_KEY, GROQ_API_KEY

GEMINI_FLASH = "gemini-1.5-flash"
OPENAI = "openai/gpt-oss-120b"
GROQ = "llama-3.3-70b-versatile"
COHERE_EMBEDDING_MODEL = "embed-v4.0"


def create_embeddings() -> CohereEmbeddings:
    """Crea el modelo de embeddings de Cohere."""
    if not COHERE_API_KEY:
        raise ValueError("Falta la variable de entorno COHERE_API_KEY.")

    return CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model=COHERE_EMBEDDING_MODEL,
        embedding_types=["float"],
    )

def create_llm(model_name: str = GROQ) -> ChatGroq:
    """Crea el modelo de lenguaje (LLM) utilizando Groq."""
    if not GROQ_API_KEY:
        raise ValueError("Falta la variable de entorno GROQ_API_KEY.")

    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=model_name,
        temperature=0.2,
    )