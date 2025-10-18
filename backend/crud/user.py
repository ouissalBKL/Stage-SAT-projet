from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.hash import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password),
        specialist=user.specialist,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
