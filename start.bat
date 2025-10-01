@echo off
echo Démarrage de l'Assistant Approvisionnement...
echo.

echo Démarrage du backend (FastAPI)...
start cmd /k "cd backend && uvicorn main:app --reload"

echo Attente de 3 secondes...
timeout /t 3 /nobreak > nul

echo Démarrage du frontend (Angular)...
start cmd /k "cd frontend && ng serve"

echo.
echo Les deux serveurs sont en cours de démarrage...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:4200
echo.
pause

