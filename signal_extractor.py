import sqlite3

import json
 
import spacy

from keybert import KeyBERT

from sentence_transformers import SentenceTransformer

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
 
from intelligence.risk_detector import detect_risks

from intelligence.opportunity_detector import detect_opportunities

from intelligence.trend_detector import detect_trends
 

# =====================================

# LOAD MODELS

# =====================================
 
print("Loading spaCy model...")

nlp = spacy.load("en_core_web_sm")
 
print("Loading BGE embedding model...")
 
embedding_model = SentenceTransformer(

    "BAAI/bge-small-en-v1.5"

)
 
# ✅ UPDATED KEYBERT (your requested change)

kw_model = KeyBERT(

    model=embedding_model

)
 
sentiment_model = SentimentIntensityAnalyzer()
 
 
# =====================================

# ENTITY EXTRACTION

# =====================================
 
def extract_entities(text):

    try:

        doc = nlp(text[:500000])

        entities = []
 
        for ent in doc.ents:

            if ent.label_ in ["ORG", "PERSON", "GPE"]:

                entities.append(ent.text)
 
        return list(set(entities))
 
    except Exception:

        return []
 
 
# =====================================

# KEYWORD EXTRACTION

# =====================================
 
def extract_keywords(text):

    try:

        text = text[:10000]
 
        keywords = kw_model.extract_keywords(

            text,

            top_n=10,

            keyphrase_ngram_range=(1, 3),

            stop_words="english"

        )
 
        return [k[0] for k in keywords]
 
    except Exception:

        return []
 
 
# =====================================

# SENTIMENT

# =====================================
 
def sentiment(text):

    score = sentiment_model.polarity_scores(text)

    compound = score["compound"]
 
    if compound >= 0.05:

        label = "positive"

    elif compound <= -0.05:

        label = "negative"

    else:

        label = "neutral"
 
    return label, compound
 
 
# =====================================

# IMPACT SCORE

# =====================================
 
def impact_score(risks, opportunities, trends):

    total = (

        len(risks)

        + len(opportunities)

        + len(trends)

    )
 
    if total >= 8:

        return "CRITICAL"

    elif total >= 5:

        return "HIGH"

    elif total >= 3:

        return "MEDIUM"

    else:

        return "LOW"
 
 
# =====================================

# MAIN PIPELINE

# =====================================
 
def run():

    conn = sqlite3.connect("intel.db")

    cursor = conn.cursor()
 
    cursor.execute("DELETE FROM strategic_signals")

    conn.commit()
 
    cursor.execute("""

        SELECT id, content

        FROM documents

    """)
 
    docs = cursor.fetchall()
 
    print(f"Processing {len(docs)} documents...")
 
    processed = 0
 
    for doc_id, text in docs:
 
        if not text:

            continue
 
        text = text.strip()
 
        if len(text) < 50:

            continue
 
        try:

            entities = extract_entities(text)

            keywords = extract_keywords(text)
 
            risks = detect_risks(text)

            opportunities = detect_opportunities(text)

            trends = detect_trends(text)
 
            sentiment_label, sentiment_score = sentiment(text)
 
            impact = impact_score(

                risks,

                opportunities,

                trends

            )
 
            cursor.execute("""

                INSERT INTO strategic_signals (

                    document_id,

                    sentiment,

                    sentiment_score,

                    risks,

                    opportunities,

                    trends,

                    keywords,

                    entities,

                    impact

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

            """, (

                doc_id,

                sentiment_label,

                sentiment_score,

                json.dumps(risks),

                json.dumps(opportunities),

                json.dumps(trends),

                json.dumps(keywords),

                json.dumps(entities),

                impact

            ))
 
            processed += 1
 
            if processed % 10 == 0:

                print(f"Processed {processed} documents...")
 
        except Exception as e:

            print(f"Error on document {doc_id}: {e}")

            continue
 
    conn.commit()

    conn.close()
 
    print(f"Strategic signals created for {processed} documents")
 
 
if __name__ == "__main__":

    run()
 