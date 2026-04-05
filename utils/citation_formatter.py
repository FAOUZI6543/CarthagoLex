from typing import List
from models.retriever import RetrievedDoc


def format_sources(docs: List[RetrievedDoc], max_items: int = 8) -> str:
    lines = []
    for i, doc in enumerate(docs[:max_items], start=1):
        lines.append(f"{i}. {doc.source} | {doc.reference} | {doc.date}")
    return "\n".join(lines) if lines else "Aucune source exploitable."


def format_context(docs: List[RetrievedDoc]) -> str:
    blocks = []
    for i, doc in enumerate(docs, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[SOURCE {i}]",
                    f"Origine: {doc.source}",
                    f"Référence: {doc.reference}",
                    f"Date: {doc.date}",
                    f"Type: {doc.doc_type}",
                    f"Score: {doc.score}",
                    "Contenu:",
                    doc.content,
                ]
            )
        )
    return "\n\n".join(blocks)
