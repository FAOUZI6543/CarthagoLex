# chains/doc_chain.py — Génération de documents juridiques pour CarthagoLex
import os
from typing import Dict


DOC_TEMPLATES = {
    "contrat": """
Vous êtes CarthagoLex, expert en rédaction de contrats juridiques.
Générez un contrat complet et structuré basé sur les paramètres suivants :
{params}

Le contrat doit inclure :
1. Identification des parties
2. Objet du contrat
3. Durée et conditions
4. Obligations réciproques
5. Conditions de résiliation
6. Clauses spéciales
7. Signatures

Rédigez en français juridique formel.
""",
    "recours": """
Vous êtes CarthagoLex, spécialiste en droit administratif français.
Rédigez un recours administratif complet basé sur :
{params}

Structure requise :
1. En-tête (autorité saisie, identité du requérant)
2. Objet du recours
3. Rappel des faits
4. Décision contestée
5. Moyens de droit (légalité externe et interne)
6. Conclusions
7. Pièces jointes

Format : recours gracieux ou hiérarchique selon le contexte.
""",
    "courrier": """
Vous êtes CarthagoLex, assistant juridique spécialisé.
Rédigez un courrier officiel basé sur :
{params}

Structure :
1. En-tête (expéditeur, destinataire, date, objet)
2. Corps du courrier (clair, précis, professionnel)
3. Formule de politesse
4. Signature
""",
    "conclusion": """
Vous êtes CarthagoLex, juriste spécialiste.
Rédigez une note de synthèse juridique basée sur :
{params}

Structure :
1. Faits pertinents
2. Problématique juridique
3. Analyse et argumentation
4. Conclusion et recommandations
""",
}


def generate_doc(doc_type: str, params: Dict) -> str:
    """Génère un document juridique via LLM."""
    template = DOC_TEMPLATES.get(doc_type, DOC_TEMPLATES["courrier"])
    params_str = "\n".join([f"- {k}: {v}" for k, v in params.items()]) if params else "Aucun paramètre fourni."
    prompt = template.format(params=params_str)

    try:
        from openai import OpenAI
        import config
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            temperature=0.3,
            messages=[
                {"role": "system", "content": "Tu es CarthagoLex, assistant juridique expert en droit français et droit des étrangers."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except ImportError:
        return _fallback_doc(doc_type, params)
    except Exception as e:
        return f"Erreur lors de la génération du document : {str(e)}"


def _fallback_doc(doc_type: str, params: Dict) -> str:
    """Génère un document modèle sans LLM."""
    params_str = "\n".join([f"  - {k}: {v}" for k, v in params.items()]) if params else "  Aucun paramètre fourni."
    return f"""[CarthagoLex — Modèle {doc_type.upper()}]

Ce document est généré en mode de secours (LLM non connecté).

Paramètres reçus :
{params_str}

Pour obtenir un document complet et personnalisé, veuillez :
1. Configurer votre clé API OpenAI dans le fichier .env
2. Redémarrer le serveur CarthagoLex
3. Relancer la génération

— CarthagoLex v2.0.0
"""
