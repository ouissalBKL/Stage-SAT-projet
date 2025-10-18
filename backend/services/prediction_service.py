import pickle
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
#from tensorflow.keras.models import load_model
import tensorflow as tf
from pgmpy.inference import VariableElimination

# =========================
# 1️⃣ Charger les modèles et objets sérialisés
# =========================

cnn_model = tf.keras.models.load_model("ML_Models/cnn_model.h5")  # ton CNN
model_bn = joblib.load("ML_Models/bayesian_model.pkl")  # BN
discretization_edges = joblib.load(
    "ML_Models/discretization_edges.pkl"
)  # edges de discrétisation
scaler = joblib.load("ML_Models/scaler1.pkl")  # scaler utilisé pendant training

# Créer l’inférence pour le BN
infer_bn = VariableElimination(model_bn)

# Liste des colonnes/features utilisées
feature_columns = [
    "national_inv",
    "lead_time",
    "in_transit_qty",
    "forecast_3_month",
    "forecast_6_month",
    "forecast_9_month",
    "sales_1_month",
    "sales_3_month",
    "sales_6_month",
    "sales_9_month",
    "min_bank",
    "potential_issue",
    "pieces_past_due",
    "perf_6_month_avg",
    "perf_12_month_avg",
    "local_bo_qty",
    "deck_risk",
    "oe_constraint",
    "ppap_risk",
    "stop_auto_buy",
    "rev_stop",
]


# =========================
# 2️⃣ Fonction de prédiction hybride
# =========================
def predict_from_features(features: dict):
    X = pd.DataFrame([features], columns=feature_columns)
    X_scaled = scaler.transform(X)
    X_cnn = X_scaled.reshape(X_scaled.shape[0], X_scaled.shape[1], 1)

    # CNN : prédiction
    cnn_pred_prob = cnn_model.predict(X_cnn).flatten()[0]
    cnn_pred_bin = int(cnn_pred_prob > 0.5)

    # Discrétisation pour le BN
    X_disc = pd.DataFrame()
    for col in feature_columns:
        edges = discretization_edges[col]
        X_disc[col + "_bin"] = pd.cut(
        [features[col]], bins=edges, labels=False, include_lowest=True)
        X_disc[col + "_bin"] = X_disc[col + "_bin"].fillna(0).astype(int)

    # Ajouter la prédiction CNN
    X_disc["cnn_pred"] = cnn_pred_bin

    # Evidence pour l’inférence BN
    evidence = {col: int(X_disc.iloc[0][col]) for col in X_disc.columns}

    # Inférence Bayésienne
    q = infer_bn.query(["went_on_backorder"], evidence=evidence, show_progress=False)
    pred_bin = int(np.argmax(q.values))
    probability = float(np.max(q.values))

    prediction = "rupture de stock" if pred_bin == 1 else "pas de rupture de stock"
    return {"prediction": prediction, "probability": probability}
