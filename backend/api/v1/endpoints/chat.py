# app/api/v1/endpoints/chat.py
from fastapi import APIRouter, Request
from services.llm_service import conversation
from services.vector_service import search_similarity
from services.specialist_service import get_specialist
from services.intent_service import detect_intent_with_llm
from services.extractor_sku import extract_sku_with_llm
from services.db_acess import get_product_features
from services.prediction_service import predict_from_features
import re

router = APIRouter()


def clean_response(text: str) -> str:
    """Nettoie la réponse des balises markdown indésirables"""
    if not text:
        return text
    
    # Supprimer les balises de header markdown
    text = re.sub(r'<\|header_start\|>', '', text)
    text = re.sub(r'<\|header_end\|>', '', text)
    text = re.sub(r'<\|.*?\|>', '', text)  # Supprimer toutes les balises <|...|>
    
    # Supprimer les balises HTML indésirables
    text = re.sub(r'<[^>]+>', '', text)
    
    # Nettoyer les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


@router.post("/ask")
async def ask_api(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "").strip()

        # 1 Détection de l’intention
        intent = detect_intent_with_llm(question)

        # 2 Extraction et normalisation du SKU si besoin
        sku_number = extract_sku_with_llm(question) if intent == "prediction" else None

        # 3 Récupération du contexte RAG
        contexte = search_similarity(question, k=2)

        # 4 Détection du style selon le type d'utilisateur
        user_is_specialist = get_specialist()
        if user_is_specialist is True:
            prompt_style = "Utilise un langage technique et concis."
        elif user_is_specialist is False:
            prompt_style = "Explique de façon claire et bien détaillée, accessible à un non-spécialiste."
        else:
            prompt_style = "Explique la réponse de manière simple et courte."

        # 5 Construction du prompt pour RAG
        prompt = (
            f"Vous êtes un assistant en gestion d'approvisionnement. "
            f"Si la question est une salutation (par ex. 'bonjour', 'salut', 'hello'), "
            f"répondez par une salutation polie et adaptée. "
            f"Répondez uniquement aux questions pertinentes à ce domaine . "
            f"Sinon, dites : "
            f"'Je suis ici pour vous offrir des réponses concernant l’approvisionnement. "
            f"Merci de poser une question en lien avec ce domaine.'\n"
            f"{prompt_style}\n"
            f"Contexte :\n{contexte}\n"
            f"Question : {question}\n"
        )

        # 6 Logique principale selon l’intention
        if intent == "prediction":
            if sku_number:
                features = get_product_features(sku_number)
                if features:
                    prediction_result = predict_from_features(features)
                    response_text = (
                        f"Pour le SKU {sku_number}, la prédiction est : "
                        f"{prediction_result['prediction']} avec une probabilité de {prediction_result['probability']:.2f}"
                    )
                else:
                    response_text = (
                        f"Je n'ai pas trouvé de données pour le SKU {sku_number}."
                    )
            else:
                response_text = "Je n'ai pas pu identifier de SKU dans votre question."
        else:
            # Question générale → LLM RAG
            response_text = conversation.invoke({"input": prompt})["response"]

        # Nettoyer la réponse des balises markdown indésirables
        response_text = clean_response(response_text)

        return {"response": response_text}

    except Exception as e:
        return {"error": str(e)}
