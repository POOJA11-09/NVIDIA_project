RISK_KEYWORDS = [
 
    "competition",

    "competitor",

    "lawsuit",

    "regulation",

    "regulatory",
 
    "investigation",

    "ban",

    "restriction",
 
    "shortage",

    "supply chain",
 
    "decline",

    "loss",

    "risk",
 
    "threat",

    "negative"

]
 
 
def detect_risks(text):
 
    risks = []
 
    text = text.lower()
 
    for keyword in RISK_KEYWORDS:
 
        if keyword in text:

            risks.append(keyword)
 
    return list(set(risks))
 