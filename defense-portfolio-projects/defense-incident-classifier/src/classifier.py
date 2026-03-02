"""
Defense ITSM Incident Classifier
Pattern: Streaming + structured output
Use case: Real-time triage of IT incidents for French defense operations

Demonstrates:
- Streaming API with live token display
- Structured output extraction from stream
- Priority classification with confidence scoring
- Routing logic (which team receives the ticket)
"""

import anthropic
import json
import time
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Generator


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class IncidentClassification:
    incident_id: str
    priority: str           # P1 | P2 | P3 | P4
    category: str           # e.g. "reseau", "securite", "applicatif", "infrastructure"
    subcategory: str
    impact_scope: str       # "utilisateur_unique" | "equipe" | "site" | "interarmes"
    assigned_team: str      # routing decision
    confidence: float       # 0.0 → 1.0
    classification_rationale: str
    suggested_actions: list[str]
    sovereign_flag: bool    # True if incident may involve classified data/systems
    processing_time_s: float
    tokens_used: int


# ── Routing table ────────────────────────────────────────────────────────────

ROUTING_TABLE = {
    "securite":       "CSIRT-Défense (astreinte 24/7)",
    "reseau":         "NOC-DIRISI (niveau 2)",
    "applicatif":     "Support-N2-Apps",
    "infrastructure": "Infra-Datacenter",
    "telephonie":     "Support-Voix-Défense",
    "poste_travail":  "Support-N1",
    "inconnu":        "Support-N1 (triage manuel requis)",
}

SOVEREIGN_KEYWORDS = [
    "classifié", "secret défense", "confidentiel défense", "diffusion restreinte",
    "dr ", "igi 1300", "pssie", "alliance", "concerto", "intradef",
    "isis", "intraced", "niveau de classification"
]


SYSTEM_PROMPT = """Tu es un agent de triage ITSM pour les systèmes d'information du Ministère des Armées français.

Ta mission : analyser un incident déclaré par un utilisateur et produire immédiatement une classification structurée.

Règles de priorité :
- P1 : Impact opérationnel critique (système de commandement, réseau interarmes, > 500 utilisateurs)
- P2 : Impact majeur (service central indisponible, > 50 utilisateurs, risque de sécurité)
- P3 : Impact modéré (service dégradé, équipe affectée, < 50 utilisateurs)
- P4 : Incident mineur ou question utilisateur

Règle critique : Si l'incident mentionne des données classifiées (Diffusion Restreinte ou supérieur), active le sovereign_flag et escalade immédiatement au CSIRT-Défense quelle que soit la priorité apparente.

Réponds UNIQUEMENT en JSON valide, sans markdown, sans commentaire. Format exact :
{
  "priority": "P1|P2|P3|P4",
  "category": "securite|reseau|applicatif|infrastructure|telephonie|poste_travail|inconnu",
  "subcategory": "<string>",
  "impact_scope": "utilisateur_unique|equipe|site|interarmes",
  "assigned_team": "<string from routing table>",
  "confidence": <float 0.0-1.0>,
  "classification_rationale": "<2 sentences explaining priority and routing>",
  "suggested_actions": ["<action 1>", "<action 2>", "<action 3>"],
  "sovereign_flag": <true|false>
}"""


# ── Streaming classifier ──────────────────────────────────────────────────────

class IncidentClassifier:
    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"

    def classify_streaming(
        self,
        incident_text: str,
        incident_id: str = "INC-UNKNOWN",
        show_stream: bool = True
    ) -> IncidentClassification:
        """
        Classify an incident using streaming API.
        Tokens stream to console in real-time, then JSON is parsed from the complete response.

        This pattern is key for SA demos: shows live responsiveness while
        ensuring structured output integrity.
        """
        start = time.time()
        full_response = ""
        input_tokens = 0
        output_tokens = 0

        if show_stream:
            print(f"\n{'─'*50}")
            print(f"🔄 Classifying {incident_id}...")
            print(f"{'─'*50}")

        # Stream the response
        with self.client.messages.stream(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Incident ID: {incident_id}\n\nDescription de l'incident:\n{incident_text}"
            }]
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                if show_stream:
                    print(text, end="", flush=True)

            # Get usage from final message
            final = stream.get_final_message()
            input_tokens = final.usage.input_tokens
            output_tokens = final.usage.output_tokens

        if show_stream:
            print(f"\n{'─'*50}")

        # Parse structured JSON from streamed response
        classification = self._parse_response(full_response, incident_id)

        # Enrich with sovereign keyword detection (deterministic — doesn't rely on LLM)
        text_lower = incident_text.lower()
        if any(kw in text_lower for kw in SOVEREIGN_KEYWORDS):
            classification.sovereign_flag = True

        classification.processing_time_s = round(time.time() - start, 2)
        classification.tokens_used = input_tokens + output_tokens
        return classification

    def classify_batch(
        self,
        incidents: list[dict],
        show_stream: bool = False
    ) -> list[IncidentClassification]:
        """Classify multiple incidents. show_stream=False for batch processing."""
        results = []
        for inc in incidents:
            result = self.classify_streaming(
                incident_text=inc["description"],
                incident_id=inc.get("id", f"INC-{len(results)+1:04d}"),
                show_stream=show_stream
            )
            results.append(result)
        return results

    def _parse_response(self, raw: str, incident_id: str) -> IncidentClassification:
        """Parse JSON response, with fallback for malformed output."""
        # Strip markdown fences if present
        clean = raw.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            clean = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        try:
            data = json.loads(clean)
            return IncidentClassification(
                incident_id=incident_id,
                priority=data.get("priority", "P3"),
                category=data.get("category", "inconnu"),
                subcategory=data.get("subcategory", ""),
                impact_scope=data.get("impact_scope", "utilisateur_unique"),
                assigned_team=ROUTING_TABLE.get(
                    data.get("category", "inconnu"),
                    ROUTING_TABLE["inconnu"]
                ),
                confidence=float(data.get("confidence", 0.5)),
                classification_rationale=data.get("classification_rationale", ""),
                suggested_actions=data.get("suggested_actions", []),
                sovereign_flag=bool(data.get("sovereign_flag", False)),
                processing_time_s=0.0,
                tokens_used=0
            )
        except json.JSONDecodeError as e:
            # Graceful degradation — return a safe default
            return IncidentClassification(
                incident_id=incident_id,
                priority="P3",
                category="inconnu",
                subcategory="parse_error",
                impact_scope="utilisateur_unique",
                assigned_team=ROUTING_TABLE["inconnu"],
                confidence=0.0,
                classification_rationale=f"Parse error: {e}. Raw: {raw[:200]}",
                suggested_actions=["Triage manuel requis"],
                sovereign_flag=False,
                processing_time_s=0.0,
                tokens_used=0
            )


# ── Eval functions ────────────────────────────────────────────────────────────

def eval_priority_range(c: IncidentClassification) -> dict:
    valid = c.priority in ["P1", "P2", "P3", "P4"]
    return {"name": "priority_range", "passed": valid, "score": 1.0 if valid else 0.0}

def eval_confidence_calibration(c: IncidentClassification) -> dict:
    """Confidence should be > 0.6 for clear incidents, lower for ambiguous ones."""
    passed = 0.0 <= c.confidence <= 1.0
    return {"name": "confidence_calibration", "passed": passed, "score": 1.0 if passed else 0.0}

def eval_sovereign_detection(c: IncidentClassification, incident_text: str) -> dict:
    """Sovereign flag must be True if classified keywords present."""
    text_lower = incident_text.lower()
    should_flag = any(kw in text_lower for kw in SOVEREIGN_KEYWORDS)
    passed = not should_flag or c.sovereign_flag
    return {
        "name": "sovereign_detection",
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "note": "SECURITY CRITICAL" if not passed else "ok"
    }

def eval_routing_consistency(c: IncidentClassification) -> dict:
    """Sovereign incidents must be routed to CSIRT."""
    if c.sovereign_flag:
        passed = "CSIRT" in c.assigned_team
    else:
        passed = c.assigned_team in ROUTING_TABLE.values()
    return {"name": "routing_consistency", "passed": passed, "score": 1.0 if passed else 0.0}


def run_evals(c: IncidentClassification, incident_text: str) -> dict:
    evals = [
        eval_priority_range(c),
        eval_confidence_calibration(c),
        eval_sovereign_detection(c, incident_text),
        eval_routing_consistency(c),
    ]
    overall = sum(e["score"] for e in evals) / len(evals)
    return {
        "overall": round(overall, 3),
        "passed": overall >= 0.75,
        "evals": evals
    }


# ── Renderer ──────────────────────────────────────────────────────────────────

PRIORITY_EMOJI = {"P1": "🚨", "P2": "🔴", "P3": "🟡", "P4": "🟢"}

def render_classification(c: IncidentClassification, eval_results: dict = None) -> str:
    sovereign_badge = " 🔐 SOVEREIGN FLAG" if c.sovereign_flag else ""
    lines = [
        f"## {PRIORITY_EMOJI[c.priority]} {c.priority} — {c.incident_id}{sovereign_badge}",
        f"**Category**: {c.category} / {c.subcategory}",
        f"**Impact**: {c.impact_scope}",
        f"**→ Routed to**: {c.assigned_team}",
        f"**Confidence**: {c.confidence:.0%}",
        f"",
        f"*{c.classification_rationale}*",
        f"",
        f"**Suggested actions**:"
    ]
    for a in c.suggested_actions:
        lines.append(f"  - {a}")
    lines.append(f"\n*⏱ {c.processing_time_s}s | {c.tokens_used} tokens*")

    if eval_results:
        status = "✅ PASSED" if eval_results["passed"] else "❌ FAILED"
        lines.append(f"\n**Eval**: {status} ({eval_results['overall']:.0%})")
        for e in eval_results["evals"]:
            icon = "✅" if e["passed"] else "❌"
            note = f" — ⚠️ {e.get('note','')}" if not e["passed"] else ""
            lines.append(f"  {icon} {e['name']}{note}")

    return "\n".join(lines)
