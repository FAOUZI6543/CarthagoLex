from typing import List
from models.retriever import RetrievedDoc


def has_sufficient_sources(docs: List[RetrievedDoc], min_docs: int) -> bool:
    return len(docs) >= min_docs


def has_reliable_scores(docs: List[RetrievedDoc], min_score: float = 0.55) -> bool:
    if not docs:
        return False
    return any(doc.score >= min_score for doc in docs)
