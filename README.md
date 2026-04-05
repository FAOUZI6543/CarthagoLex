# CarthagoLex

Assistant juridique IA specialise en **droit des etrangers**, **droit administratif** et **droit de la securite sociale** en France.

Backend Python/Flask avec pipeline RAG (Retrieval-Augmented Generation) base sur FAISS et OpenAI.

---

## Architecture

```
CarthagoLex/
|-- app.py                    # Serveur Flask (point d'entree)
|-- config.py                 # Configuration centrale
|-- requirements.txt          # Dependances Python
|-- .env.example              # Variables d'environnement (modele)
|
|-- chains/
|   |-- rag_pipeline.py       # Pipeline RAG principal
|   `-- rag_chain.py          # Interface appelable depuis app.py
|
|-- models/
|   |-- retriever.py          # LegalRetriever (FAISS)
|   `-- embedder.py           # Embeddings OpenAI
|
|-- utils/
|   |-- citation_formatter.py # Formatage des sources
|   `-- validators.py         # Validation qualite des sources
|
|-- prompts/
|   `-- system_prompt.txt     # Prompt systeme CarthagoLex
|
|-- scripts/
|   `-- index_documents.py    # Script d'indexation FAISS
|
|-- data/
|   |-- docs/                 # Vos documents juridiques (.txt, .pdf, .md)
|   `-- faiss_index/          # Index FAISS genere (cree automatiquement)
|
`-- index.html                # Interface web
```

---

## Installation rapide

### 1. Cloner et configurer

```powershell
git clone https://github.com/FAOUZI6543/CarthagoLex
cd CarthagoLex

# Copier et remplir le fichier .env
copy .env.example .env
# Editer .env et renseigner : OPENAI_API_KEY, LLM_MODEL, etc.
```

### 2. Environnement Python

```powershell
# Autoriser PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Creer et activer le virtualenv
python -m venv .venv
.venv\Scripts\Activate.ps1

# Installer les dependances
pip install -r requirements.txt
```

### 3. Indexer vos documents (premiere fois)

```bash
# Placer vos documents PDF/TXT/MD dans data/docs/
mkdir -p data/docs
# ... copier vos fichiers ...

# Indexer
python scripts/index_documents.py --docs_dir data/docs --index_dir data/faiss_index
```

### 4. Lancer le serveur

```bash
python app.py
# Ouvrir : http://localhost:5000
```

---

## API REST

| Methode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/chat` | Consultation juridique (RAG) |
| POST | `/api/analyze` | Analyse de dossier |
| POST | `/api/generate-document` | Generation de document |
| GET | `/api/modes` | Liste des modes disponibles |
| GET | `/api/health` | Etat du serveur |

### Exemple de requete

```json
POST /api/chat
{
  "message": "Quelles sont les conditions pour une AES a titre exceptionnel ?",
  "mode": "analyse_risque"
}
```

### Modes disponibles

| Mode | Description |
|------|-------------|
| `analyse_risque` | Analyse juridique structuree avec evaluation des risques |
| `controle_qualite` | Verification et correction d'un dossier |
| `interpretation_texte` | Interpretation d'un texte juridique |
| `redaction_recours` | Aide a la redaction d'un recours |

---

## Domaines de competence

- **CESEDA** : Code de l'entree et du sejour des etrangers
- **Droit au sejour** : Titres de sejour, renouvellement, AES
- **Contentieux administratif** : Recours gracieux, hierarchiques, TA
- **Securite sociale** : Droits sociaux des etrangers
- **Conventions bilaterales** : France-Tunisie
- **Droit du travail** : Autorisation de travail, changement de statut
- **Protection internationale** : Asile, protection subsidiaire

---

## Variables d'environnement (.env)

```env
OPENAI_API_KEY=sk-...         # Cle API OpenAI (obligatoire)
LLM_MODEL=gpt-4o-mini         # Modele LLM
LLM_TEMPERATURE=0.2           # Temperature
FAISS_INDEX_PATH=data/faiss_index
TOP_K_RETRIEVAL=5             # Nombre de sources recuperees
SYSTEM_PROMPT_PATH=prompts/system_prompt.txt
REQUIRE_SOURCES=true          # Refuser si sources insuffisantes
MIN_RETRIEVED_DOCS=2
MAX_SOURCES_DISPLAY=5
DEFAULT_MODE=analyse_risque
PORT=5000
FLASK_DEBUG=true
```

---

## Licence

MIT - Voir [LICENSE](LICENSE)

## Contact

Pour toute question : [support@carthagolex.com](mailto:support@carthagolex.com)

*Derniere mise a jour : Avril 2026*
