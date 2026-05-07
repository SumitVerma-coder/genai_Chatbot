import sys
import os
import time
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urlparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.mongodb import get_collection


SITEMAP_URLS = [
    "https://handbook.gitlab.com/sitemap.xml",
    "https://about.gitlab.com/sitemap.xml",
]

IMPORTANT_URLS = [
    "https://handbook.gitlab.com/",
    "https://handbook.gitlab.com/handbook/",
    "https://handbook.gitlab.com/handbook/company/mission/",
    "https://handbook.gitlab.com/handbook/values/",
    "https://handbook.gitlab.com/handbook/company/culture/all-remote/",
    "https://handbook.gitlab.com/handbook/company/culture/all-remote/asynchronous/",
    "https://handbook.gitlab.com/handbook/company/culture/all-remote/handbook-first/",
    "https://handbook.gitlab.com/handbook/people-group/directly-responsible-individuals/",

    "https://about.gitlab.com/direction/",
    "https://about.gitlab.com/direction/company/",
    "https://about.gitlab.com/direction/dev/",
    "https://about.gitlab.com/direction/ops/",
    "https://about.gitlab.com/direction/sec/",
    "https://about.gitlab.com/direction/data-science/",
]

MAX_URLS = 150


def clean_text(text: str) -> str:
    return " ".join(text.split())


def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 250):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def is_valid_content_url(url: str) -> bool:
    if not url:
        return False

    blocked_extensions = (
        ".png", ".jpg", ".jpeg", ".gif", ".svg",
        ".pdf", ".webp", ".mp4", ".zip"
    )

    if url.endswith(blocked_extensions):
        return False

    handbook_allowed_sections = [
        "https://handbook.gitlab.com/handbook/company/",
        "https://handbook.gitlab.com/handbook/values/",
        "https://handbook.gitlab.com/handbook/people-group/",
        "https://handbook.gitlab.com/handbook/product/",
        "https://handbook.gitlab.com/handbook/engineering/",
        "https://handbook.gitlab.com/handbook/security/",
    ]

    direction_prefix = "https://about.gitlab.com/direction/"

    if any(url.startswith(section) for section in handbook_allowed_sections):
        return True

    if url.startswith(direction_prefix):
        return True

    return False


def parse_sitemap(sitemap_url: str):
    print(f"Fetching sitemap: {sitemap_url}")

    response = requests.get(
        sitemap_url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0 GitLab Handbook Chatbot Student Project"
        }
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)

    namespace = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
    }

    urls = []

    for loc in root.findall(".//sm:loc", namespace):
        url = loc.text

        if not url:
            continue

        if url.endswith(".xml"):
            try:
                urls.extend(parse_sitemap(url))
            except Exception as e:
                print(f"Failed to parse nested sitemap: {url}")
                print(e)

        elif is_valid_content_url(url):
            urls.append(url)

    return urls


def fetch_sitemap_urls():
    urls = []

    for sitemap_url in SITEMAP_URLS:
        try:
            urls.extend(parse_sitemap(sitemap_url))
        except Exception as e:
            print(f"Failed to fetch sitemap: {sitemap_url}")
            print(e)

    unique_urls = list(dict.fromkeys(urls))

    return unique_urls[:MAX_URLS]


def scrape_page(url: str):
    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0 GitLab Handbook Chatbot Student Project"
        }
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else url
    text = clean_text(soup.get_text(separator=" "))

    return {
        "title": title,
        "url": url,
        "text": text,
    }


def get_source_type(url: str) -> str:
    if url.startswith("https://handbook.gitlab.com/"):
        return "handbook"

    if url.startswith("https://about.gitlab.com/direction/"):
        return "direction"

    return "unknown"


def ingest():
    collection = get_collection()

    sitemap_urls = fetch_sitemap_urls()

    urls = IMPORTANT_URLS + sitemap_urls
    urls = list(dict.fromkeys(urls))

    print(f"Found {len(urls)} total URLs from Handbook + Direction pages.")

    if not urls:
        print("No URLs found. Check sitemap URLs or filter conditions.")
        return

    collection.delete_many({})

    documents = []

    for index, url in enumerate(urls, start=1):
        try:
            print(f"[{index}/{len(urls)}] Scraping: {url}")

            page = scrape_page(url)
            chunks = chunk_text(page["text"])

            for chunk_index, chunk in enumerate(chunks):
                documents.append({
                    "title": page["title"],
                    "url": page["url"],
                    "source_type": get_source_type(page["url"]),
                    "chunk_index": chunk_index,
                    "text": chunk,
                })

            time.sleep(0.5)

        except Exception as e:
            print(f"Failed to scrape {url}")
            print(e)

    if documents:
        collection.insert_many(documents)

    print(f"Inserted {len(documents)} chunks into MongoDB.")


if __name__ == "__main__":
    ingest()