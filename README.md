# 🤖 Assistant Approvisionnement - Chatbot avec RAG

Ce projet est un **chatbot intelligent spécialisé dans l’approvisionnement** qui utilise la technologie **RAG (Retrieval-Augmented Generation)** pour fournir des réponses **précises, rapides et contextuelles**.

---

## 🏗️ Architecture

<p align="center">
  <img src="c25bf11d-0595-4728-b29f-236feafc1e5a.png" alt="Architecture du chatbot RAG" width="850">
</p>

---

## 🔍 Explication de l’Architecture

L’architecture repose sur une **intégration fluide entre FastAPI, Angular et les modèles d’intelligence artificielle**.

### 🧑‍💻 Utilisateur (Frontend Angular)
- L’utilisateur interagit via une interface moderne construite avec **Angular**.
- Ses requêtes (questions ou prédictions) sont envoyées à l’**API FastAPI**.

### ⚙️ FastAPI (Backend)
C’est le **cœur du système** : il reçoit les requêtes, orchestre les modèles IA, et renvoie les réponses.

### 🧩 Détection d’intention
Un **modèle de langage (LLM)** identifie le type de demande :
- **Question** → envoyée vers le **module RAG**
- **Prédiction de rupture de stock** → envoyée vers le **modèle CNN + Random Boosting**

### 📈 Prédiction Stockout (CNN + RB)
Le modèle **CNN+RB** prédit les risques de rupture de stock à partir des données contenues dans **PostgreSQL**.

### 🧠 Module RAG (Retrieval-Augmented Generation)
Si la requête est une question, le **pipeline RAG** est déclenché :
1. **Nomic Embed-Text** transforme la question en vecteurs.
2. Une **recherche sémantique** est effectuée dans **ChromaDB**.
3. Le **modèle ChatGroq (LLM)** combine les résultats et génère une **réponse contextuelle**.

### 💾 Base de données
- **ChromaDB** : stocke les embeddings pour la recherche vectorielle.
- **PostgreSQL** : conserve les données métiers et historiques.

### 🔁 Réponse
La **réponse finale** est renvoyée à l’utilisateur via l’interface Angular.

---

## ⚙️ Composants

| Composant | Description |
|------------|-------------|
| 🧩 **Backend** | FastAPI (Python) – API REST du chatbot |
| 💻 **Frontend** | Angular – Interface utilisateur moderne |
| 🧠 **IA & RAG** | LLM, ChatGroq, Nomic Embed-Text, ChromaDB |
| 🗄️ **Base de données** | PostgreSQL pour les données métiers |

---

## 🚀 Installation et Démarrage

### 🔧 Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python main.py
