# 👩‍⚖️ CarthagoLex

**Assistant juridique IA spécialisé en droit des étrangers, droit administratif et droit de la sécurité sociale en France.**

CarthagoLex est une plateforme d'assistance juridique intelligente basée sur un pipeline RAG (Retrieval-Augmented Generation) avec FAISS et OpenAI, conçue pour aider les juristes dans l'analyse de dossiers complexes.

---

## 🎯 Fonctionnalités

### 📋 Modes d'analyse disponibles
- **Analyse de risque** : Évaluation structurée des risques juridiques
- **Contrôle qualité** : Vérification de la cohérence et validité des documents
- **Interprétation de texte** : Analyse approfondie de textes juridiques
- **Rédaction de recours** : Génération de brouillons de recours administratifs

### 🛠️ Capacités
- ✅ Interface de chat moderne et responsive
- ✅ Recherche sémantique dans une base documentaire juridique (FAISS)
- ✅ Génération de documents (contrats, recours, courriers)
- ✅ Historique de conversation
- ✅ Citations des sources juridiques
- ✅ Modes fallback si LLM non connecté

---

## 📂 Architecture

```
CarthagoLex/
├── app.py                  # Backend Flask principal
├── config.py               # Configuration centralisée
├── index.html              # Interface utilisateur (chat UI)
├── chains/
│   ├── __init__.py
│   ├── rag_chain.py        # Pipeline RAG principal
│   ├── rag_pipeline.py     # Classe CarthagoLexPipeline
│   └── doc_chain.py        # Génération de documents
├── models/
│   ├── __init__.py
│   ├── retriever.py        # LegalRetriever FAISS
│   ├── embedder.py         # Gestion des embeddings
│   └── generator.py        # Génération LLM
├── utils/
│   ├── __init__.py
│   ├── citation_formatter.py
│   └── validators.py
├── prompts/
│   ├── system_prompt.txt
│   └── system_prompt_carthagolex.md
├── scripts/
│   └── index_documents.py  # Construction de l'index FAISS
├── .env.example            # Template de configuration
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Prérequis
- Python 3.9+
- pip
- (Optionnel) virtualenv

### 1. Cloner le dépôt
```bash
git clone https://github.com/FAOUZI6543/CarthagoLex.git
cd CarthagoLex
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
```

Éditez le fichier `.env` avec vos clés :
```env
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.2
EMBEDDING_MODEL=text-embedding-3-small

FAISS_INDEX_PATH=data/faiss_index
SYSTEM_PROMPT_PATH=prompts/system_prompt.txt

DEFAULT_MODE=analyse_risque
REQUIRE_SOURCES=true
MIN_RETRIEVED_DOCS=2
TOP_K_RETRIEVAL=5
MAX_SOURCES_DISPLAY=5

PORT=5000
FLASK_DEBUG=true
```

### 5. (Optionnel) Construire l'index FAISS
Si vous avez des documents juridiques à indexer :
```bash
python scripts/index_documents.py --input data/documents --output data/faiss_index
```

### 6. Lancer le serveur
```bash
python app.py
```

🌐 Accédez à l'application : **http://localhost:5000**

---

## 📖 Utilisation

### Interface Web
1. Ouvrez http://localhost:5000 dans votre navigateur
2. Sélectionnez un mode d'analyse (Analyse de Risque, Contrôle Qualité, etc.)
3. Posez votre question juridique dans le chat
4. CarthagoLex recherche dans sa base documentaire et génère une réponse structurée avec sources

### API REST

#### Consultation juridique
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Puis-je contester un refus de titre de séjour?",
    "historique": [],
    "mode": "analyse_risque"
  }'
```

#### Génération de documents
```bash
curl -X POST http://localhost:5000/api/generate-document \
  -H "Content-Type: application/json" \
  -d '{
    "type": "recours",
    "params": {
      "decision": "Refus de titre de séjour",
      "autorite": "Préfecture de Paris",
      "date_decision": "15/01/2025"
    }
  }'
```

#### Health Check
```bash
curl http://localhost:5000/api/health
```

---

## 🧪 Tests

```bash
python -m pytest tests/
```

---

## 📝 Structure des données FAISS

L'index FAISS stocke :
- **index.faiss** : Index vectoriel des embeddings
- **documents.pkl** : Métadonnées des documents (source, article, contenu)

Format des documents :
```python
{
    "content": "Texte du document juridique...",
    "source": "CESEDA L311-1",
    "article": "Article L311-1",
    "score": 0.92  # Ajouté lors de la recherche
}
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT.

---

## 👤 Auteur

**FAOUZI6543**  
Spécialiste en droit des étrangers et assistance juridique

---

## 🆘 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation dans `/docs`

---

**© 2025 CarthagoLex - Votre assistant juridique de confiance** 👩‍⚖️
