from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import chat, specialist, predict, user
from database import Base, engine
import models.user  



Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(chat.router, prefix="/api/v1/endpoints", tags=["chat"])
#je pense que ca sert a rien 
app.include_router(specialist.router, prefix="/api/v1/endpoints", tags=["specialist"])
app.include_router(predict.router, prefix="/api/v1/endpoints", tags=["predict"])
app.include_router(user.router, prefix="/api/v1/endpoints", tags=["user"])
