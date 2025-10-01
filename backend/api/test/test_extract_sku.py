import sys
import os

# Ajouter le dossier 'app' au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from services.llm_service import conversation
from services.extractor_sku import extract_sku_with_llm

questions = [
    "Prédiction pour SKU 45678",
]

sku = extract_sku_with_llm(questions)
print("le sku - test_extract_sku.py:15", sku)
