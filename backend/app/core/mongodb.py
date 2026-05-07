import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "gitlab_chatbot")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "handbook_chunks")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is missing. Please add it to backend/.env")

client = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=30000,
)

db = client[DATABASE_NAME]

handbook_collection = db[COLLECTION_NAME]
users_collection = db["users"]
chats_collection = db["chats"]


def get_collection():
    return handbook_collection


def get_users_collection():
    return users_collection


def get_chats_collection():
    return chats_collection