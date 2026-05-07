from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from uuid import uuid4

from app.models.schemas import ChatRequest, ChatResponse
from app.core.guardrails import is_gitlab_related,is_possible_followup
from app.core.rag_pipeline import generate_answer
from app.core.auth import get_current_user
from app.core.mongodb import get_chats_collection

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    chats_collection = get_chats_collection()

    user_message = {
        "role": "user",
        "content": request.question,
        "sources": [],
    }
    
    is_related = is_gitlab_related(request.question)
    is_followup = request.chat_id and is_possible_followup(request.question)

    if not is_related and not is_followup:
        assistant_message = {
            "role": "assistant",
            "content": "I'm only able to answer questions about GitLab's Handbook and Direction pages.",
            "sources": [],
        }

    else:
        try:
            chat_history = []

            if request.chat_id:
                existing_chat = chats_collection.find_one(
                    {
                        "_id": request.chat_id,
                        "user_id": current_user["_id"],
                    },
                    {
                        "messages": 1,
                        "_id": 0,
                    }
                )

                if existing_chat:
                    chat_history = existing_chat.get("messages", [])
                    
            result = generate_answer(request.question,chat_history)

            answer = result["answer"]
            sources = result["sources"]

            assistant_message = {
                "role": "assistant",
                "content": answer,
                "sources": sources,
            }
        except Exception as e:
            error_message = str(e)
            print("Backend error while generating answer:", error_message)

            if "429" in error_message or "quota" in error_message.lower():
                answer = (
                    "The chatbot is temporarily unavailable because the daily AI usage "
                    "limit has been reached. Please try again later."
                )

            elif "timeout" in error_message.lower():
                answer = "The request took too long. Please try again."

            else:
                answer = "Something went wrong while generating the answer. Please try again."

            sources = []

            assistant_message = {
                "role": "assistant",
                "content": answer,
                "sources": sources,
            }

    now = datetime.now(timezone.utc).isoformat()

    if request.chat_id:
        chat_id = request.chat_id

        chats_collection.update_one(
            {
                "_id": chat_id,
                "user_id": current_user["_id"],
            },
            {
                "$push": {
                    "messages": {
                        "$each": [user_message, assistant_message]
                    }
                },
                "$set": {
                    "updated_at": now
                },
            },
        )

    else:
        chat_id = str(uuid4())
        title = request.question[:60]

        chats_collection.insert_one({
            "_id": chat_id,
            "user_id": current_user["_id"],
            "title": title,
            "messages": [user_message, assistant_message],
            "created_at": now,
            "updated_at": now,
        })

    return {
        "answer": answer,
        "sources": sources,
        "chat_id": chat_id,
    }

@router.get("/chats")
def get_chats(current_user: dict = Depends(get_current_user)):
    chats_collection = get_chats_collection()

    chats = list(
        chats_collection.find(
            {"user_id": current_user["_id"]},
            {"messages": 0}
        ).sort("updated_at", -1)
    )

    return [
        {
            "id": chat["_id"],
            "title": chat["title"],
            "created_at": chat["created_at"],
            "updated_at": chat["updated_at"],
        }
        for chat in chats
    ]


@router.get("/chats/{chat_id}")
def get_chat(chat_id: str, current_user: dict = Depends(get_current_user)):
    chats_collection = get_chats_collection()

    chat = chats_collection.find_one({
        "_id": chat_id,
        "user_id": current_user["_id"],
    })

    if not chat:
        return {"error": "Chat not found"}

    return {
        "id": chat["_id"],
        "title": chat["title"],
        "messages": chat["messages"],
        "created_at": chat["created_at"],
        "updated_at": chat["updated_at"],
    }


@router.delete("/chats/{chat_id}")
def delete_chat(chat_id: str, current_user: dict = Depends(get_current_user)):
    chats_collection = get_chats_collection()

    chats_collection.delete_one({
        "_id": chat_id,
        "user_id": current_user["_id"],
    })

    return {"message": "Chat deleted"}