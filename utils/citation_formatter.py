# utils/citation_formatter.py — Formatage des sources recuperees
from typing import List, Dict


def format_context(docs: List[Dict]) -> str:
    """Construit le bloc de contexte injecte dans le prompt."""
    if not docs:
        return "Aucune source disponible."
    parts = []
    for i, doc in enumerate(docs, 1):
        source  = doc.get("source", "Source inconnue")
        content = doc.get("content", "").strip()
        score   = doc.get("score", 0.0)
        parts.append(
            f"[Source {i}] {source} (score: {score:.2f})\n{content}"
        )
    return "\n\n---\n\n".join(parts)


def format_sources(docs: List[Dict], max_display: int = 5) -> str:
    """Genere la liste lisible des sources pour l'affichage final."""
    if not docs:
        return "Aucune source."
    lines = []
    for i, doc in enumerate(docs[:max_display], 1):
        source   = doc.get("source", "Source inconnue")
        metadata = doc.get("metadata", {})
        date     = metadata.get("date", "")
        ref      = metadata.get("reference", "")
        label = f"{i}. {source}"
        if ref:
            label += f" - {ref}"
        if date:
            label += f" ({date})"
        lines.append(label)
    return "\n".join(lines)
