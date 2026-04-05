# models/retriever.py — Retriever FAISS pour CarthagoLex
from typing import List, Dict
from pathlib import Path


class LegalRetriever:
    def __init__(self, index_path: str, top_k: int = 5):
        self.index_path = index_path
        self.top_k = top_k
        self.index = None
        self.documents = []
        self._load_index()

    def _load_index(self):
        """Charge l'index FAISS s'il existe, sinon passe en mode degrade."""
        try:
            import faiss
            import pickle
            idx_file  = Path(self.index_path) / "index.faiss"
            docs_file = Path(self.index_path) / "documents.pkl"
            if idx_file.exists() and docs_file.exists():
                self.index = faiss.read_index(str(idx_file))
                with open(docs_file, "rb") as f:
                    self.documents = pickle.load(f)
                print(f"Index FAISS charge : {len(self.documents)} documents")
            else:
                print("Index FAISS introuvable - mode sans base documentaire active.")
        except ImportError:
            print("faiss-cpu non installe - pip install faiss-cpu")

    def retrieve(self, query: str) -> List[Dict]:
        """Retourne les documents les plus pertinents pour la requete."""
        if self.index is None or not self.documents:
            return self._fallback_docs(query)
        try:
            import numpy as np
            from models.embedder import embed_text
            query_vec = embed_text(query)
            query_vec = np.array([query_vec], dtype="float32")
            scores, indices = self.index.search(query_vec, self.top_k)
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents):
                    doc = self.documents[idx].copy()
                    doc["score"] = float(score)
                    results.append(doc)
            return results
        except Exception as e:
            print(f"Erreur retriever : {e}")
            return self._fallback_docs(query)

    def _fallback_docs(self, query: str) -> List[Dict]:
        """Retourne des docs generiques si l'index est absent."""
        return [
            {
                "content": f"Aucune source trouvee pour : '{query}'.",
                "source": "Base documentaire vide",
                "score": 0.0,
                "metadata": {}
            }
        ]
