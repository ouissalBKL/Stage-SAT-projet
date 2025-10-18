from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse, UserLogin
from database import get_db
from crud import user as crud_user
from utils.hash import verify_password

router = APIRouter(prefix="/users", tags=["Users"])


# ---------------------
# Route d'inscription
# ---------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    new_user = crud_user.create_user(db, user)
    return new_user


# ---------------------
# Route de connexion
# ---------------------
@router.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials"
        )
    return db_user
