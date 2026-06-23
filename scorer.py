from collections import Counter
 
class StrategyScorer:
 
    def score_signals(self, signals):
 
        all_risks = []

        all_opportunities = []

        all_trends = []
 
        for s in signals:

            all_risks += str(s.get("risks", "")).split(",")

            all_opportunities += str(s.get("opportunities", "")).split(",")

            all_trends += str(s.get("trends", "")).split(",")
 
        return {

            "risk_score": len(all_risks),

            "opportunity_score": len(all_opportunities),

            "trend_score": len(all_trends),

            "top_risks": Counter(all_risks).most_common(5),

            "top_opportunities": Counter(all_opportunities).most_common(5),

            "top_trends": Counter(all_trends).most_common(5),

        }
 