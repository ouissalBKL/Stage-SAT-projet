from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import os
import pickle

print("🔹 Début du script - load_toPostgre.py:8")

# --- 1. Chargement du CSV ---
csv_path = os.path.join("Datasets", "Training_BOP.csv")
print(f"Chargement du CSV depuis : {csv_path} - load_toPostgre.py:12")
data = pd.read_csv(csv_path, encoding="latin1", low_memory=False)
print(
    f"CSV chargé avec {data.shape[0]} lignes et {data.shape[1]} colonnes"
)

# --- 2. Remplacer -99 par NaN ---
data = data.replace(-99, np.nan)
print("Valeurs 99 remplacées par NaN - load_toPostgre.py:20")

# --- 3. Remplir les valeurs manquantes ---
for col in data.columns:
    if data[col].dtype == "object":
        data[col] = data[col].fillna(data[col].mode()[0])
    else:
        data[col] = data[col].fillna(data[col].median())
print("valeurs manquantes remplies - load_toPostgre.py:28")

# --- 4. Encodage des variables catégorielles avec les encoders sauvegardés ---
cat_cols = [
    "potential_issue",
    "deck_risk",
    "oe_constraint",
    "ppap_risk",
    "stop_auto_buy",
    "rev_stop",
]

# Charger les encoders depuis le fichier
with open("encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

# Appliquer les encoders existants
for col in cat_cols:
    if col in encoders:
        le = encoders[col]
        data[col] = le.transform(data[col])
print("Colonnes catégorielles encodées avec encoders.pkl - load_toPostgre.py:49")

# --- 5. Supprimer la colonne cible si présente ---
data_to_db = data.drop(columns=["went_on_backorder"], errors="ignore")
print("Colonne cible supprimée (si présente) - load_toPostgre.py:53")

# --- 6. Créer l'engine SQLAlchemy ---
conn_string = "postgresql+psycopg2://postgres:post1234@localhost:5432/stockout_db"
engine = create_engine(conn_string, future=True)
print("Engine SQLAlchemy créé - load_toPostgre.py:58")

# --- 7. Charger le DataFrame dans PostgreSQL ---
try:
    print("🔹 Début de l'insertion dans PostgreSQL - load_toPostgre.py:62")
    data_to_db.to_sql(
        "products_features",
        con=engine,
        if_exists="replace",
        index=False,
        method="multi",
    )
    print("DataFrame chargé dans PostgreSQL - load_toPostgre.py:70")

    # --- 8. Vérification ---
    data_check = pd.read_sql("SELECT * FROM products_features LIMIT 5;", engine)
    print("Vérification réussie : premières lignes récupérées - load_toPostgre.py:74")
    print(data_check)

except Exception as e:
    print("Une erreur est survenue : - load_toPostgre.py:78", e)

print("🔹Fin du script - load_toPostgre.py:80")
