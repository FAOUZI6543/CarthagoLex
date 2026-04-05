from dataclasses import dataclass
from typing import List


@dataclass
class RetrievedDoc:
    content: str
    source: str
    reference: str = ""
    date: str = ""
    score: float = 0.0
    doc_type: str = ""


class LegalRetriever:
    def __init__(self, index_path: str, top_k: int = 6):
        self.index_path = index_path
        self.top_k = top_k

    def retrieve(self, query: str) -> List[RetrievedDoc]:
        if not query or not query.strip():
            return []

        return [
            RetrievedDoc(
                content=(
                    "Extrait simulé : article CESEDA ou jurisprudence potentiellement pertinente "
                    "pour la question posée."
                ),
                source="Base juridique interne",
                reference="CESEDA / décision à confirmer",
                date="À vérifier",
                score=0.82,
                doc_type="texte",
            ),
            RetrievedDoc(
                content=(
                    "Extrait simulé : décision défavorable ou limitative à intégrer dans "
                    "l'analyse contradictoire."
                ),
                source="Base jurisprudentielle",
                reference="CAA / TA / CE à confirmer",
                date="À vérifier",
                score=0.75,
                doc_type="jurisprudence",
            ),
            RetrievedDoc(
                content=(
                    "Extrait simulé : commentaire doctrinal ou circulaire récente utile "
                    "à la vérification."
                ),
                source="Doctrine / circulaire",
                reference="Source à confirmer",
                date="À vérifier",
                score=0.70,
                doc_type="doctrine",
            ),
        ]
