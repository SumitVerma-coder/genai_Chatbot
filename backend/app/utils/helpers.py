import re


def clean_question(question: str) -> str:
    return question.strip()


def extract_keywords(question: str):
    question = question.lower()

    stopwords = {
        "what", "is", "are", "the", "a", "an", "of", "to", "in", "for",
        "and", "or", "how", "does", "do", "about", "tell", "me", "gitlab",
        "please", "explain"
    }

    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]*\b", question)

    keywords = [
        word for word in words
        if word not in stopwords and len(word) > 2
    ]

    return keywords

def is_direction_question(question: str) -> bool:
    q = question.lower()

    direction_keywords = [
        "direction",
        "roadmap",
        "strategy",
        "vision",
        "future",
        "platform direction",
        "product direction",
    ]

    return any(keyword in q for keyword in direction_keywords)


def is_handbook_question(question: str) -> bool:
    q = question.lower()

    handbook_keywords = [
        "handbook",
        "values",
        "mission",
        "remote",
        "all remote",
        "asynchronous",
        "async",
        "dri",
        "directly responsible individual",
        "communication",
        "culture",
        "people group",
        "engineering handbook",
        "security handbook",
    ]

    return any(keyword in q for keyword in handbook_keywords)

def build_context(chunks):
    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"""
Source {index}
Title: {chunk.get("title", "Unknown")}
URL: {chunk.get("url", "")}
Content:
{chunk.get("text", "")}
"""
        )

    return "\n\n".join(context_parts)


def format_sources(chunks):
    sources = []

    seen_urls = set()

    for chunk in chunks:
        url = chunk.get("url", "")

        if url in seen_urls:
            continue

        seen_urls.add(url)

        sources.append({
            "title": chunk.get("title", "GitLab Handbook or Direction"),
            "url": url,
            "snippet": chunk.get("text", "")[:250] + "..."
        })

    return sources