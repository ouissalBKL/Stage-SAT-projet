from services.llm_service import conversation
import re


def extract_sku_with_llm(question: str) -> str | None:
    """
    Utilise le LLM pour détecter s'il y a un SKU dans la question,
    puis renvoie uniquement le numéro du SKU (sans 'SKU').
    """
    prompt = f"""
    Analyse la question suivante et indique s'il y a un SKU (identifiant produit alphanumérique ou numérique).
    Répond librement, le SKU peut apparaître dans une phrase.

    Question : {question}
    """
    response = conversation.invoke({"input": prompt})["response"].strip()

    # Regex pour extraire le numéro après 'SKU'
    match = re.search(r"\b([0-9]+)\b", response, re.IGNORECASE)
    if match:
        return match.group(1)  # retourne uniquement le numéro
    return None
