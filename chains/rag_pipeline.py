from pathlib import Path
from typing import Dict

import config
from models.retriever import LegalRetriever
from utils.citation_formatter import format_context, format_sources
from utils.validators import has_sufficient_sources, has_reliable_scores


class CarthagoLexPipeline:
    def __init__(self, llm_callable):
        self.llm_callable = llm_callable
        self.retriever = LegalRetriever(
            index_path=config.FAISS_INDEX_PATH,
            top_k=config.TOP_K_RETRIEVAL,
        )
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        path = Path(config.SYSTEM_PROMPT_PATH)
        if not path.exists():
            return "Tu es CarthagoLex, assistant juridique spécialisé."
        return path.read_text(encoding="utf-8")

    def _mode_instruction(self, mode: str) -> str:
        mapping = {
            "analyse_risque": (
                "Produis une analyse de risque structurée : "
                "Question traitée, Fondements juridiques applicables, "
                "Jurisprudence favorable, Jurisprudence défavorable ou limites, "
                "Analyse de risque, Points à vérifier, Sources."
            ),
            "controle_qualite": (
                "Produis un rapport de contrôle qualité : "
                "Résumé du contrôle, Points VALIDÉS, Points À VÉRIFIER, "
                "ERREURS ou incohérences, Recommandations de correction, Sources."
            ),
            "interpretation_texte": (
                "Produis une note d'interprétation : "
                "Nature et portée du texte, Version et vigueur, "
                "Conditions d'application, Exceptions et limites, "
                "Effets pratiques pour le dossier, Points ambigus ou à vérifier, Sources."
            ),
            "redaction_recours": (
                "Produis un brouillon de recours : "
                "Objet du recours, Rappel synthétique des faits, Décision contestée, "
                "Recevabilité et délai, Moyens de légalité externe, "
                "Moyens de légalité interne, Éléments de preuve utiles, "
                "Points faibles / risques, Sources."
            ),
        }
        return mapping.get(mode, mapping[config.DEFAULT_MODE])

    def run(self, user_query: str, mode: str) -> Dict:
        retrieved_docs = self.retriever.retrieve(user_query)

        if config.REQUIRE_SOURCES:
            if not has_sufficient_sources(retrieved_docs, config.MIN_RETRIEVED_DOCS):
                return {
                    "answer": config.LOW_CONFIDENCE_MESSAGE,
                    "sources": [],
                    "status": "A_VERIFIER",
                }

            if not has_reliable_scores(retrieved_docs):
                return {
                    "answer": config.LOW_CONFIDENCE_MESSAGE,
                    "sources": [],
                    "status": "A_VERIFIER",
                }

        context = format_context(retrieved_docs)
        sources_text = format_sources(retrieved_docs, config.MAX_SOURCES_DISPLAY)

        prompt = f"""
{self.system_prompt}

### Mode demandé
{mode}

### Instruction métier
{self._mode_instruction(mode)}

### Question du juriste
{user_query}

### Sources récupérées
{context}

### Contraintes impératives
- Ne jamais inventer de source.
- N'affirmer que ce qui est soutenu par les sources fournies.
- Si un point n'est pas confirmé, l'indiquer comme \"à vérifier\".
- Toujours terminer par une section Sources.
"""

        answer = self.llm_callable(prompt)

        return {
            "answer": answer,
            "sources": sources_text.split("\n"),
            "status": "OK",
        }
