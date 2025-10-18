from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.specialist_service import get_specialist

router = APIRouter()


@router.get("/status")
def specialist_status(
    email: str = Query(..., description="Email de l'utilisateur"),
    db: Session = Depends(get_db),
):
    """Retourne le statut specialist (true/false) pour l'email fourni."""
    specialist = get_specialist(email, db)
    if specialist is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"email": email, "specialist": specialist}
