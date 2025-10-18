from crud.user import get_user_by_email
from sqlalchemy.orm import Session


# services/specialist_service.py
user_is_specialist = None


def set_specialist(value: bool):
    global user_is_specialist
    user_is_specialist = value


def get_specialist(email: str, db: Session):
    user = get_user_by_email(db, email)
    return user.specialist if user else None
