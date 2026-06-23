TREND_KEYWORDS = [
 
    "generative ai",

    "agentic ai",
 
    "data center",
 
    "ai chips",
 
    "gpu",
 
    "semiconductor",
 
    "robotics",
 
    "autonomous vehicles",
 
    "machine learning",
 
    "cloud ai",
 
    "edge ai"

]
 
 
def detect_trends(text):
 
    trends = []
 
    text = text.lower()
 
    for keyword in TREND_KEYWORDS:
 
        if keyword in text:

            trends.append(keyword)
 
    return list(set(trends))
 