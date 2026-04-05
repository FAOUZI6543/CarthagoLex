# config.py — Configuration centrale CarthagoLex
import os
from dotenv import load_dotenv

load_dotenv()

# LLM
OPENAI_API_KEY        = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL             = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_TEMPERATURE       = float(os.getenv("LLM_TEMPERATURE", "0.2"))

# FAISS / Retriever
FAISS_INDEX_PATH      = os.getenv("FAISS_INDEX_PATH", "data/faiss_index")
TOP_K_RETRIEVAL       = int(os.getenv("TOP_K_RETRIEVAL", "5"))

# Prompts
SYSTEM_PROMPT_PATH    = os.getenv("SYSTEM_PROMPT_PATH", "prompts/system_prompt.txt")

# Controle qualite
REQUIRE_SOURCES       = os.getenv("REQUIRE_SOURCES", "true").lower() == "true"
MIN_RETRIEVED_DOCS    = int(os.getenv("MIN_RETRIEVED_DOCS", "2"))
MAX_SOURCES_DISPLAY   = int(os.getenv("MAX_SOURCES_DISPLAY", "5"))
DEFAULT_MODE          = os.getenv("DEFAULT_MODE", "analyse_risque")

# Message confiance insuffisante
LOW_CONFIDENCE_MESSAGE = (
    "Sources insuffisantes ou peu fiables pour repondre avec certitude. "
    "Veuillez reformuler votre question ou enrichir la base documentaire."
)
