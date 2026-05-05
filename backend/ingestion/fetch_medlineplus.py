import time
import requests
from bs4 import BeautifulSoup

MEDLINEPLUS_API = "https://wsearch.nlm.nih.gov/ws/query"

SEARCH_TERMS = [
    "diabetes",
    "hypertension",
    "heart disease",
    "asthma",
    "cancer",
    "depression",
    "anxiety disorder",
    "arthritis",
    "stroke",
    "pneumonia",
    "kidney disease",
    "liver disease",
    "thyroid",
    "anemia",
    "obesity",
    "COPD",
    "HIV",
    "tuberculosis",
    "epilepsy",
    "migraine",
    "Parkinson disease",
    "Alzheimer disease",
    "multiple sclerosis",
    "osteoporosis",
    "lupus",
]


def _fetch_topics(term: str, retmax: int = 3) -> list[dict]:
    params = {"db": "healthTopics", "term": term, "retmax": retmax}
    try:
        resp = requests.get(MEDLINEPLUS_API, params=params, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  Warning: failed to fetch '{term}': {e}")
        return []

    soup = BeautifulSoup(resp.content, "lxml-xml")
    docs = []
    for doc_tag in soup.find_all("document"):
        url = doc_tag.get("url", "")
        title_tag = doc_tag.find("content", {"name": "title"})
        summary_tag = doc_tag.find("content", {"name": "FullSummary"})
        snippet_tag = doc_tag.find("content", {"name": "snippet"})

        title = title_tag.get_text(strip=True) if title_tag else ""

        text = ""
        if summary_tag:
            # FullSummary contains HTML; strip tags to get plain text
            inner = BeautifulSoup(summary_tag.get_text(), "html.parser")
            text = inner.get_text(separator=" ", strip=True)
        elif snippet_tag:
            text = snippet_tag.get_text(strip=True)

        if title and text and len(text) > 50:
            docs.append({"source": "medlineplus", "topic": title, "url": url, "text": text})
    return docs


def fetch_medlineplus_docs(max_docs: int = 45) -> list[dict]:
    seen_keys: set[str] = set()
    all_docs: list[dict] = []

    for term in SEARCH_TERMS:
        if len(all_docs) >= max_docs:
            break
        batch = _fetch_topics(term, retmax=3)
        added = 0
        for doc in batch:
            key = doc["url"] or doc["topic"]
            if key not in seen_keys and len(all_docs) < max_docs:
                seen_keys.add(key)
                all_docs.append(doc)
                added += 1
        print(f"  '{term}': +{added} new  (total {len(all_docs)})")
        time.sleep(0.3)

    return all_docs
