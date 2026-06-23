class StrategicReasoner:
 
    def synthesize(self, evidence, signals):

        """

        Converts raw data → CEO-level insights

        """
 
        opportunities = []

        risks = []

        trends = []
 
        for e in evidence:

            text = e["text"].lower()
 
            if any(k in text for k in ["growth", "demand", "opportunity", "partnership"]):

                opportunities.append(e["title"])
 
            if any(k in text for k in ["risk", "ban", "regulation", "lawsuit", "competition"]):

                risks.append(e["title"])
 
            if any(k in text for k in ["ai", "chip", "data center", "gpu", "automation"]):

                trends.append(e["title"])
 
        return {

            "opportunities": list(set(opportunities)),

            "risks": list(set(risks)),

            "trends": list(set(trends))

        }
 