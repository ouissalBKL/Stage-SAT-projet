from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import chat, specialist, predict

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
app.include_router(specialist.router, prefix="/api/v1/endpoints", tags=["specialist"])
app.include_router(predict.router, prefix="/api/v1/endpoints", tags=["predict"])
