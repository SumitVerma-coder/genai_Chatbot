from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.chat import router as chat_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router

app = FastAPI(title="GitLab Handbook Chatbot API")

origins = [
    "http://localhost:5173",
    "https://genai-chatbot-adkk.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(users_router, prefix="/api/users")


@app.get("/")
def root():
    return {"message": "GitLab Handbook Chatbot API is running"}