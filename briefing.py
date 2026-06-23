class CEOBriefing:
    def generate(self, recommendation):
        if not isinstance(recommendation, dict):
            return {
                "what_happened": "",
                "why_it_matters": "",
                "recommended_action": ""
            }

        what_happened = recommendation.get(
            "executive_summary",
            ""
        )

        why_it_matters = ""

        if "risk_assessment" in recommendation:
            why_it_matters = recommendation.get(
                "risk_assessment",
                ""
            )

        elif "expected_impact" in recommendation:
            why_it_matters = recommendation.get(
                "expected_impact",
                ""
            )

        elif "final_decision" in recommendation:
            why_it_matters = recommendation.get(
                "final_decision",
                {}
            ).get(
                "reasoning",
                ""
            )

        recommended_action = recommendation.get(
            "recommended_action",
            ""
        )

        if not recommended_action:
            recommended_action = recommendation.get(
                "final_decision",
                {}
            ).get(
                "action",
                ""
            )

        return {
            "what_happened": what_happened,
            "why_it_matters": why_it_matters,
            "recommended_action": recommended_action
        }