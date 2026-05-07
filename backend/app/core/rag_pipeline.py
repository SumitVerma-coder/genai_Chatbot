import os
import google.generativeai as genai
from dotenv import load_dotenv

from app.core.mongodb import get_collection
from app.utils.helpers import (
    extract_keywords,
    build_context,
    format_sources,
    is_direction_question,
    is_handbook_question,
)

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Please add it to backend/.env")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def retrieve_relevant_chunks(question: str, limit: int = 6):
    collection = get_collection()

    keywords = extract_keywords(question)

    if not keywords:
        return []

    direction_question = is_direction_question(question)
    handbook_question = is_handbook_question(question)

    keyword_conditions = []

    for keyword in keywords:
        keyword_conditions.extend([
            {"text": {"$regex": keyword, "$options": "i"}},
            {"title": {"$regex": keyword, "$options": "i"}},
            {"url": {"$regex": keyword, "$options": "i"}},
        ])

    query = {
        "$or": keyword_conditions
    }

    chunks = list(
        collection.find(query, {"_id": 0})
        .limit(150)
    )

    scored_chunks = []

    for chunk in chunks:
        title = chunk.get("title", "").lower()
        url = chunk.get("url", "").lower()
        text = chunk.get("text", "").lower()

        score = 0

        for keyword in keywords:
            if keyword in title:
                score += 5
            if keyword in url:
                score += 4
            if keyword in text:
                score += 1

        if direction_question and "/direction/" in url:
            score += 10

        if handbook_question and "/handbook/" in url:
            score += 10

        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda item: item[0])

    return [chunk for score, chunk in scored_chunks[:limit]]

def build_history_context(chat_history, max_messages: int = 6):
    if not chat_history:
        return ""

    recent_messages = chat_history[-max_messages:]

    history_parts = []

    for message in recent_messages:
        role = message.get("role", "")
        content = message.get("content", "")

        if content:
            history_parts.append(f"{role}: {content}")

    return "\n".join(history_parts)

def rewrite_followup_question(question: str, chat_history=None):
    history_context = build_history_context(chat_history)

    if not history_context:
        return question

    prompt = f"""
You are rewriting a user's follow-up question into a standalone search query.

Rules:
1. Use the chat history only to resolve references like it, this, that, they, those, above, same, previous.
2. Do not answer the question.
3. Do not add new facts.
4. Keep it short and clear.
5. Return only the rewritten question.

Chat history:
{history_context}

User question:
{question}

Standalone question:
"""

    response = model.generate_content(prompt)

    rewritten_question = getattr(response, "text", None)

    if not rewritten_question:
        return question

    return rewritten_question.strip()


def generate_answer(question: str, chat_history=None):
    try:
        standalone_question = rewrite_followup_question(question, chat_history)

        chunks = retrieve_relevant_chunks(standalone_question)

        if not chunks:
            return {
                "answer": "I could not find enough information in GitLab's Handbook or Direction pages to answer that.",
                "sources": []
            }

        context = build_context(chunks)
        history_context = build_history_context(chat_history)

        prompt = f"""
You are a helpful chatbot that answers questions only using the provided GitLab Handbook and Direction pages context.

Rules:
1. Answer only from the provided context.
2. Use the chat history only to understand the user's follow-up question.
3. Do not use outside knowledge.
4. If the question is not related to GitLab, say exactly:
   "I'm only able to answer questions about GitLab's Handbook and Direction pages."
5. If the context does not contain enough relevant information, say exactly:
   "I could not find enough information in GitLab's Handbook or Direction pages to answer that."
6. Use the most relevant context. If the user asks about Direction, prefer Direction page context. If the user asks about Handbook topics, prefer Handbook page context.
7. Keep the answer clear and concise.
8. Do not invent facts.

Chat history:
{history_context}

Retrieved context:
{context}

Original user question:
{question}

Standalone rewritten question:
{standalone_question}

Answer:
"""

        response = model.generate_content(prompt)

        answer = getattr(response, "text", None)

        if not answer:
            answer = "I could not generate an answer from the available GitLab Handbook or Direction context."

        return {
            "answer": answer.strip(),
            "sources": format_sources(chunks)
        }

    except Exception as e:
        print("RAG PIPELINE ERROR:", str(e))

        return {
            "answer": f"Backend error while generating answer: {str(e)}",
            "sources": []
        }