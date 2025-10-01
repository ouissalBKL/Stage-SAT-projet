from services.llm_service import conversation


def detect_intent_with_llm(question: str) -> str:
    """utilise le LLM pour classifier l'intention
    retourne prediction ou rag
    """

    prompt = f"""
    Analyse la question suivante et réponds uniquement par :
    - 'prediction' si l'utilisateur demande une probabilité de rupture, un risque de stockout ou une prédiction basée sur un SKU.
    - 'rag' sinon (question générale d'explication ou conseil).

    Question : {question}
    """

    response = conversation.invoke({"input": prompt})["response"].strip().lower()
    if "prediction" in response:
        return "prediction"
    else:
        return "rag"
