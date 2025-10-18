from pydantic import BaseModel, EmailStr


# Schéma pour l'inscription
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    specialist: bool = False


# Schéma pour la réponse (sans le mot de passe)
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    specialist: bool

    class Config:
        orm_mode = True


# Schéma pour le login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
