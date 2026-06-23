import re
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================
# CONFIG
# =========================

OPPORTUNITY_KEYWORDS = [
    "partnership",
    "investment",
    "expansion",
    "growth",
    "acquisition",
    "innovation",
    "new market",
    "ai adoption",
    "demand",
    "revenue",
    "opportunity"
]

NEGATION_PATTERNS = [
    r"\bno\b",
    r"\bnot\b",
    r"\bnever\b",
    r"\bwithout\b",
    r"\black of\b",
    r"\babsence of\b"
]

# =========================
# MODEL (same family as your RAG)
# =========================
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


# Pre-embed keywords once (VERY IMPORTANT optimization)
keyword_embeddings = model.encode(OPPORTUNITY_KEYWORDS, normalize_embeddings=True)


# =========================
# UTILS
# =========================

def is_negated(text, keyword):
    """
    Detect simple negation near keyword
    """
    pattern = rf"(no|not|never|without|lack of|absence of).{{0,40}}{keyword}"
    return re.search(pattern, text.lower()) is not None


def cosine_sim(a, b):
    return np.dot(a, b)


# =========================
# MAIN DETECTOR
# =========================

def detect_opportunities(text, threshold=0.55):
    """
    Returns structured opportunity intelligence for RAG + CEO agent
    """

    if not text:
        return {
            "opportunities": [],
            "confidence": 0.0
        }

    text_clean = text.lower()

    text_embedding = model.encode([text_clean], normalize_embeddings=True)[0]

    detected = []

    for i, keyword in enumerate(OPPORTUNITY_KEYWORDS):

        # semantic similarity
        score = cosine_sim(text_embedding, keyword_embeddings[i])

        if score >= threshold:

            # negation filtering
            if is_negated(text_clean, keyword):
                continue

            detected.append({
                "opportunity": keyword,
                "confidence": float(round(score, 3)),
                "evidence": text[:200]
            })

    # sort by confidence
    detected = sorted(detected, key=lambda x: x["confidence"], reverse=True)

    return {
        "opportunities": detected,
        "top_score": detected[0]["confidence"] if detected else 0.0,
        "count": len(detected)
    }


# =========================
# TEST
# =========================
if __name__ == "__main__":

    sample_text = """
    NVIDIA is expanding its AI partnerships with cloud providers.
    The company is seeing strong demand for GPUs and increased revenue growth.
    """

    result = detect_opportunities(sample_text)

    import json
    print(json.dumps(result, indent=2))