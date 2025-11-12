import json
from pathlib import Path
from typing import Dict, Any, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load snippets on import
KB_PATH = Path(__file__).parent / "kb" / "snippets.json"

with open(KB_PATH, "r", encoding="utf-8") as f:
    DOCS: List[Dict[str, Any]] = json.load(f)


def _build_corpus(docs: List[Dict[str, Any]]) -> Tuple[TfidfVectorizer, Any, List[Dict[str, Any]]]:
    """Create a TF-IDF matrix from lightweight fields for quick retrieval."""
    texts = [
        " ".join([
            d.get("framework", ""),
            d.get("section", ""),
            d.get("title", ""),
            d.get("summary_notes", "")
        ])
        for d in docs
    ]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)
    return vectorizer, matrix, docs


_VECTORIZER, _MATRIX, _DOCS = _build_corpus(DOCS)


def retrieve_best(query: str, top_k: int = 1) -> List[Tuple[Dict[str, Any], float]]:
    """Return top_k docs by cosine similarity."""
    if not query.strip():
        return []
    q_vec = _VECTORIZER.transform([query])
    scores = cosine_similarity(q_vec, _MATRIX)[0]
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    results = []
    for idx, score in ranked[:top_k]:
        results.append((_DOCS[idx], float(score)))
    return results


def analyze_query(query: str) -> Dict[str, Any]:
    """Analyze user query and return best-matching compliance snippet."""
    hits = retrieve_best(query, top_k=1)
    if not hits:
        return {
            "ok": False,
            "message": "No strong match found. Try specifying a framework or section (e.g., 'GDPR Article 30')."
        }

    doc, score = hits[0]

    # Confidence heuristic (0-1)
    confidence = max(0.0, min(1.0, score))

    # Quote from official source
    quote = doc.get("source_excerpt", "").strip()
    if not quote:
        quote = "(Official excerpt not yet added.)"

    # Action guidance / summary
    notes = doc.get("summary_notes", "").strip()
    actions = []
    if notes:
        for piece in [p.strip() for p in notes.replace(";", ".").split(".")]:
            if piece:
                actions.append(piece)

    return {
        "ok": True,
        "framework": doc.get("framework"),
        "section": doc.get("section"),
        "title": doc.get("title"),
        "quote": quote,
        "actions": actions,
        "citation": {
            "source_url": doc.get("source_url"),
            "last_reviewed": doc.get("last_reviewed")
        },
        "confidence": round(confidence, 3)
    }
