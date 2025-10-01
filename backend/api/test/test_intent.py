import sys
import os

# Ajouter le dossier racine 'app' au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from services.llm_service import conversation
from services.intent_service import detect_intent_with_llm

questions = [
    "Peux-tu me donner la probabilité de rupture pour le SKU12345 ?",
    "Explique-moi ce qu’est un stockout",
    "Prédiction pour SKU45678",
    "Quels sont les facteurs qui causent un stockout ?",
]

for q in questions:
    intent = detect_intent_with_llm(q)
    print(f"Question: {q} - test_intent.py:19")
    print(f"Intention détectée: {intent} - test_intent.py:20")
    print("" * 50)
