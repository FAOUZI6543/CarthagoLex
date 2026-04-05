# chains/rag_chain.py — Point d'entree utilise par app.py
from typing import List, Dict
import config
from chains.rag_pipeline import CarthagoLexPipeline


def _build_llm_callable():
    """Construit la fonction LLM OpenAI injectable dans le pipeline."""
    from openai import OpenAI
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    def call_llm(prompt: str) -> str:
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    return call_llm


# Instance singleton du pipeline
_pipeline = None


def get_pipeline() -> CarthagoLexPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = CarthagoLexPipeline(llm_callable=_build_llm_callable())
    return _pipeline


def run_chain(user_query: str, history: List[Dict] = None, mode: str = None) -> str:
    """Fonction principale appelee par app.py."""
    mode = mode or config.DEFAULT_MODE
    pipeline = get_pipeline()
    result = pipeline.run(user_query=user_query, mode=mode)
    return result.get("answer", config.LOW_CONFIDENCE_MESSAGE)
