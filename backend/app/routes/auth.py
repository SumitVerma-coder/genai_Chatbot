from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from uuid import uuid4

from app.models.schemas import SignupRequest, LoginRequest, AuthResponse
from app.core.mongodb import get_users_collection
from app.core.auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/signup", response_model=AuthResponse)
def signup(request: SignupRequest):
    users_collection = get_users_collection()

    existing_user = users_collection.find_one({"email": request.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid4())

    user = {
        "_id": user_id,
        "name": request.name,
        "email": request.email,
        "password_hash": hash_password(request.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    users_collection.insert_one(user)

    token = create_access_token({"sub": user_id})

    return {
        "token": token,
        "user": {
            "id": user_id,
            "name": user["name"],
            "email": user["email"],
        },
    }


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest):
    users_collection = get_users_collection()

    user = users_collection.find_one({"email": request.email})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user["_id"]})

    return {
        "token": token,
        "user": {
            "id": user["_id"],
            "name": user["name"],
            "email": user["email"],
        },
    }