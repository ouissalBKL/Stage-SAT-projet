
from fastapi import APIRouter, Request
from services.specialist_service import set_specialist

router = APIRouter()


@router.post("/set_specialist")
async def set_specialist_route(request: Request):
    data = await request.json()
    answer = data.get("answer")
    if answer == "oui":
        set_specialist(True)
        message = "Parfait ! Je vais adapter mes réponses à votre niveau d'expertise."
    elif answer == "non":
        set_specialist(False)
        message = "Parfait ! Je vais vous expliquer les concepts de manière claire et accessible."
    else:
        message = "Réponse non reconnue."
    return {"message": message}
