import sqlite3

import json

import time

import ollama
 
from ceo_agent.retriever import Retriever

from ceo_agent.ranker import EvidenceRanker

from ceo_agent.scorer import StrategyScorer

from ceo_agent.reasoner import StrategicReasoner

from ceo_agent.prompts import build_prompt
 
DB_PATH = "intel.db"
 
 
class CEOAgent:
 
    def __init__(self):
 
        self.retriever = Retriever()

        self.ranker = EvidenceRanker()

        self.scorer = StrategyScorer()

        self.reasoner = StrategicReasoner()
 
    # =========================

    # LOAD SIGNALS

    # =========================
 
    def load_signals(self):
 
        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()
 
        cursor.execute("""

            SELECT risks, opportunities, trends

            FROM strategic_signals

        """)
 
        data = cursor.fetchall()
 
        conn.close()
 
        return data
 
    # =========================

    # FORMAT SIGNALS

    # =========================
 
    def format_signals(self, data):
 
        return [

            {

                "risks": r[0],

                "opportunities": r[1],

                "trends": r[2]

            }

            for r in data

        ]
 
    # =========================

    # SAFE LLM CALL

    # =========================
 
    def call_llm(self, prompt):
 
        try:
 
            response = ollama.chat(

                model="qwen3:8b",

                messages=[

                    {

                        "role": "user",

                        "content": prompt

                    }

                ]

            )
 
            return response["message"]["content"]
 
        except Exception as e:
 
            return json.dumps({

                "error": str(e),

                "model": "qwen3:8b"

            })
 
    # =========================

    # JSON VALIDATION

    # =========================
 
    def parse_output(self, text):
 
        try:

            return json.loads(text)
 
        except Exception:

            return {

                "error": "invalid_json",

                "raw_output": text

            }
 
    # =========================

    # MAIN ENGINE

    # =========================
 
    def ask(self, question):
 
        start_time = time.time()
 
        # --------------------------------

        # STEP 1: RETRIEVE

        # --------------------------------
 
        raw_results = self.retriever.retrieve(question)
 
        if not raw_results:

            return {

                "error": "No evidence retrieved."

            }
 
        # --------------------------------

        # STEP 2: RANK

        # --------------------------------
 
        evidence_ranked = self.ranker.rank(

            raw_results,

            question

        )
 
        evidence_text = "\n".join([

            f"""

TITLE: {e.get('title', 'N/A')}
 
SOURCE: {e.get('source', 'N/A')}
 
URL: {e.get('url', 'N/A')}
 
TEXT:

{e.get('text', '')[:500]}

"""

            for e in evidence_ranked[:8]

        ])
 
        # --------------------------------

        # STEP 3: LOAD SIGNALS

        # --------------------------------
 
        signals_raw = self.load_signals()
 
        signals = self.format_signals(

            signals_raw

        )
 
        # --------------------------------

        # STEP 4: SCORE SIGNALS

        # --------------------------------
 
        scores = self.scorer.score_signals(

            signals

        )
 
        # --------------------------------

        # STEP 5: STRATEGIC REASONING

        # --------------------------------
 
        reasoning = self.reasoner.synthesize(

            evidence_ranked,

            signals

        )
 
        reasoning_text = (

            "\n".join(

                f"{k}: {v}"

                for k, v in reasoning.items()

            )

            if isinstance(reasoning, dict)

            else str(reasoning)

        )
 
      
        # --------------------------------
        # STEP 6: SMART QUESTION ROUTING
        # --------------------------------

        question_lower = question.lower()

        risk_keywords = [
            "risk",
            "risks",
            "threat",
            "challenge",
            "problem",
            "lawsuit",
            "ban",
            "regulation",
            "regulatory"
        ]

        opportunity_keywords = [
            "opportunity",
            "opportunities",
            "growth",
            "expand",
            "expansion",
            "market",
            "investment"
        ]

        if any(word in question_lower for word in risk_keywords):

            prompt = f"""
You are NVIDIA's Chief Risk Officer.

Question:
{question}

Risk Signals:
{json.dumps(scores.get("top_risks", {}), indent=2)}

Evidence:
{evidence_text}

Return ONLY valid JSON:

{{
    "executive_summary": "",
    "biggest_risks": [],
    "risk_assessment": "",
    "recommended_action": "",
    "confidence": 0.0
}}
"""

        elif any(word in question_lower for word in opportunity_keywords):

            prompt = f"""
You are NVIDIA's Chief Growth Officer.

Question:
{question}

Opportunity Signals:
{json.dumps(scores.get("top_opportunities", {}), indent=2)}

Evidence:
{evidence_text}

Return ONLY valid JSON:

{{
    "executive_summary": "",
    "top_opportunities": [],
    "expected_impact": "",
    "recommended_action": "",
    "confidence": 0.0
}}
"""

        else:

            prompt = build_prompt(
                question,
                evidence_text,
                reasoning_text,
                json.dumps(signals, indent=2),
                json.dumps(scores, indent=2)
            )
        # --------------------------------

        # STEP 7: LLM

        # --------------------------------
 
        raw_output = self.call_llm(prompt)
 
        parsed_output = self.parse_output(

            raw_output

        )
 
        total_time = round(

            time.time() - start_time,

            2

        )
 
        if isinstance(parsed_output, dict):
 
            parsed_output["execution_time_seconds"] = total_time

            parsed_output["model"] = "qwen3:8b"
 
        return parsed_output
 
 
# =========================

# RUN

# =========================
 
if __name__ == "__main__":
 
    agent = CEOAgent()
 
    print("\n🚀 NVIDIA CEO STRATEGIC AGENT READY\n")
 
    while True:
 
        q = input("CEO QUESTION: ")
 
        if q.lower() == "exit":

            break
 
        result = agent.ask(q)
 
        print("\n====================\n")
 
        print(

            json.dumps(

                result,

                indent=2

            )

        )
 
        print("\n====================\n")
 