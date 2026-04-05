# models/embedder.py — Embeddings via OpenAI pour CarthagoLex
from typing import List
import config


def embed_text(text: str) -> List[float]:
    """Genere un embedding OpenAI pour un texte donne."""
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def embed_documents(texts: List[str]) -> List[List[float]]:
    """Batch embedding pour indexation de documents."""
    return [embed_text(t) for t in texts]
