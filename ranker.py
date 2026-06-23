import numpy as np
 
 
class EvidenceRanker:
 
    def rank(self, results, query):
 
        ranked = []
 
        for r in results:
 
            score = r["score"]
 
            text = r["text"]
 
            # boost important keywords
            boost = 0
 
            keywords = ["nvidia", "ai", "gpu", "chip", "data center", "investment"]
 
            for k in keywords:
                if k.lower() in text.lower():
                    boost += 0.05
 
            final_score = score + boost
 
            ranked.append((final_score, r))
 
        ranked.sort(reverse=True, key=lambda x: x[0])
 
        return [r[1] for r in ranked]