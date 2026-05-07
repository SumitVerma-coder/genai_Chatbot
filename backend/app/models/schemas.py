from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Source(BaseModel):
    title: str
    url: Optional[str] = None
    snippet: Optional[str] = None


class ChatRequest(BaseModel):
    question: str
    chat_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source] = []
    chat_id: Optional[str] = None
    
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    token: str
    user: dict


class ChatMessage(BaseModel):
    role: str
    content: str
    sources: Optional[List[Source]] = []


class ChatSession(BaseModel):
    id: str
    title: str
    messages: List[ChatMessage] = []