# utils/validators.py — Validation de la qualite des sources
from typing import List, Dict

SCORE_THRESHOLD = 0.45  # Seuil minimum de pertinence FAISS


def has_sufficient_sources(docs: List[Dict], min_docs: int) -> bool:
    """Verifie qu'assez de documents ont ete recuperes."""
    valid = [d for d in docs if d.get("content", "").strip()]
    return len(valid) >= min_docs


def has_reliable_scores(docs: List[Dict]) -> bool:
    """Verifie qu'au moins un doc depasse le seuil de score."""
    if not docs:
        return False
    return any(d.get("score", 0.0) >= SCORE_THRESHOLD for d in docs)
