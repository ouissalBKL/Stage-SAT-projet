# Assistant Approvisionnement - Chatbot avec RAG

Ce projet est un chatbot intelligent spécialisé dans l'approvisionnement qui utilise la technologie RAG (Retrieval-Augmented Generation) pour fournir des réponses précises et contextuelles.

## Architecture

- **Backend**: FastAPI (Python) - API REST pour le chatbot
- **Frontend**: Angular - Interface utilisateur moderne
- **Fonctionnalités**: RAG, prédictions  de la rupture de stock, détection de spécialité

## Installation et Démarrage

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Le backend sera accessible sur `http://localhost:8000`

### Frontend (Angular)

```bash
cd frontend
npm install
ng serve
```

Le frontend sera accessible sur `http://localhost:4200`

## Fonctionnalités

### Chatbot Intelligent
- Interface de chat moderne avec Angular
- Détection automatique du niveau d'expertise utilisateur
- Réponses adaptées selon le profil (spécialiste/non-spécialiste)

### RAG (Retrieval-Augmented Generation)
- Recherche sémantique dans la base de connaissances
- Génération de réponses contextuelles
- Support multilingue

### Prédictions
- Prédiction de demandes pour les SKUs
- Analyse de probabilités
- Support des prédictions en lot

### API Endpoints

- `POST /api/v1/endpoints/ask` - Poser une question au chatbot
- `POST /api/v1/endpoints/set_specialist` - Définir le niveau d'expertise
- `GET /api/v1/endpoints/predict/{sku}` - Prédiction pour un SKU spécifique
- `GET /api/v1/endpoints/predict/all` - Prédictions pour tous les produits

## Structure du Projet

```
├── backend/                 # API FastAPI
│   ├── api/v1/endpoints/   # Endpoints API
│   ├── services/           # Services métier
│   ├── Models/            # Modèles ML
│   └── main.py            # Point d'entrée
├── frontend/              # Application Angular
│   ├── src/app/          # Composants Angular
│   └── package.json      # Dépendances
└── README.md             # Documentation
```

## Technologies Utilisées

- **Backend**: FastAPI, Python, ML Models
- **Frontend**: Angular 20, TypeScript, CSS3
- **IA**: RAG, LLM, Vector Search
- **Base de données**: Vector Database (Chroma)

## Développement

Pour le développement, vous pouvez utiliser les commandes suivantes :

```bash
# Backend en mode développement
cd backend
uvicorn main:app --reload

# Frontend en mode développement
cd frontend
ng serve --open
```

## Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

