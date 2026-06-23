import re

from collections import Counter
 
class DataNormalizer:
 
    def normalize_keywords(self, signals, key):
 
        words = []
 
        for s in signals:
 
            if isinstance(s, dict):

                raw = s.get(key, "")
 
            else:

                raw = str(s)
 
            # HARD CLEANING (CRITICAL FIX)

            raw = raw.replace("[", "")

            raw = raw.replace("]", "")

            raw = raw.replace('"', "")

            raw = raw.replace("'", "")
 
            parts = re.split(r"[,\|;\n]+", raw)
 
            for p in parts:

                clean = p.strip().lower()
 
                if clean and clean not in ["none", "null", "nan", ""]:

                    words.append(clean)
 
        return Counter(words)
 