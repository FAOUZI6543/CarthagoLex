def build_llm():
    def fake_llm(prompt: str) -> str:
        return (
            "1. Question traitée\n"
            "Analyse préparatoire générée en mode démonstration.\n\n"
            "2. Fondements juridiques applicables\n"
            "À compléter à partir des sources récupérées.\n\n"
            "3. Jurisprudence favorable\n"
            "À compléter.\n\n"
            "4. Jurisprudence défavorable ou limites\n"
            "À compléter.\n\n"
            "5. Analyse de risque\n"
            "Conclusion prudente, sous réserve de vérification manuelle.\n\n"
            "6. Points à vérifier\n"
            "- Vérifier les références exactes\n"
            "- Vérifier l'actualité des textes et décisions\n\n"
            "7. Sources\n"
            "Voir la liste des sources récupérées."
        )

    return fake_llm
