#!/bin/bash

echo "Démarrage de l'Assistant Approvisionnement..."
echo

echo "Démarrage du backend (FastAPI)..."
cd backend
python main.py &
BACKEND_PID=$!

echo "Attente de 3 secondes..."
sleep 3

echo "Démarrage du frontend (Angular)..."
cd ../frontend
ng serve &
FRONTEND_PID=$!

echo
echo "Les deux serveurs sont en cours de démarrage..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:4200"
echo
echo "Appuyez sur Ctrl+C pour arrêter les serveurs"

# Fonction pour arrêter les processus
cleanup() {
    echo "Arrêt des serveurs..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

# Capturer Ctrl+C
trap cleanup SIGINT

# Attendre que les processus se terminent
wait

