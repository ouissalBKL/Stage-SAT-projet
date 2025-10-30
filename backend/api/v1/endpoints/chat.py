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
from fastapi import Depends
from database import get_db
from services.response_service import clean_response    

router = APIRouter()





@router.post("/ask")
async def ask_api(request: Request, db=Depends(get_db)):
    try:
        data = await request.json()
        question = data.get("question", "").strip()
        email = data.get("email")

        # 1 Détection de l’intention
        intent = detect_intent_with_llm(question)

        # 2 Extraction et normalisation du SKU si besoin
        sku_number = extract_sku_with_llm(question) if intent == "prediction" else None

        # 3 Récupération du contexte RAG
        contexte = search_similarity(question)
    
        # 4 Détection du style selon le type d'utilisateur
        user_is_specialist = get_specialist(email, db) if email else None
        # Définition du style selon l’utilisateur
        if user_is_specialist is True:
            prompt_style_text = (
            "Vous êtes un assistant expert en gestion d'approvisionnement. "
             "Répondez de manière technique, précise et concise, adaptée à un spécialiste du domaine."
    )
        elif user_is_specialist is False:
            prompt_style_text = (
            "Vous êtes un assistant en gestion d'approvisionnement. "
            "Répondez de manière claire, détaillée et pédagogique, adaptée à un non-spécialiste."
    )
        else:
            prompt_style_text = (
            "Vous êtes un assistant en gestion d'approvisionnement. "
            " Répondez simplement et de façon courte, accessible à tout utilisateur."
    )

# Prompt final pour le LLM
        prompt = (
        f"{prompt_style_text}\n\n"
        f"Instructions importantes :\n"
        f"- Ne répondez qu'aux questions liées à la gestion d'approvisionnement.\n"
        f"- Si la question est une salutation (ex. 'bonjour', 'salut', 'hello'), répondez poliment.\n"
        f"- Sinon, utilisez le contexte fourni ci-dessous pour formuler une réponse pertinente.\n\n"
        f"Contexte : {contexte}\n\n"
        f"Question : {question}\n\n"
        f"Répondez en respectant strictement le style indiqué au début."
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
