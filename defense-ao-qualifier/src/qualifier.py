"""
Defense AO Qualifier — Agentic qualification pipeline for French defense procurement.
Uses Claude claude-sonnet-4-6 with multi-step reasoning and tool use.
"""

import anthropic
import json
import time
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime


# ── Tool definitions (function calling) ─────────────────────────────────────

TOOLS = [
    {
        "name": "score_criterion",
        "description": (
            "Record a scored evaluation for a specific qualification criterion. "
            "Call this once per criterion after analysis."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "criterion": {
                    "type": "string",
                    "description": "Criterion name (e.g. 'conformite_reglementaire', 'fit_strategique')"
                },
                "score": {
                    "type": "integer",
                    "description": "Score from 0 to 10",
                    "minimum": 0,
                    "maximum": 10
                },
                "justification": {
                    "type": "string",
                    "description": "2-3 sentence justification grounded in the document"
                },
                "red_flags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of blocking issues identified, if any"
                }
            },
            "required": ["criterion", "score", "justification", "red_flags"]
        }
    },
    {
        "name": "extract_metadata",
        "description": "Extract structured metadata from the AO document.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reference": {"type": "string", "description": "AO reference number"},
                "entite_adjudicatrice": {"type": "string"},
                "objet": {"type": "string", "description": "Short description of the contract object"},
                "valeur_estimee": {"type": "string", "description": "Estimated contract value (€)"},
                "date_limite_remise": {"type": "string", "description": "Submission deadline"},
                "duree_marche": {"type": "string"},
                "classification": {"type": "string", "description": "Security classification if mentioned"},
                "procedure": {"type": "string", "description": "Procurement procedure type"}
            },
            "required": ["reference", "entite_adjudicatrice", "objet", "valeur_estimee", "date_limite_remise"]
        }
    },
    {
        "name": "emit_go_nogo",
        "description": "Emit the final Go/No-Go recommendation with synthesis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "decision": {
                    "type": "string",
                    "enum": ["GO", "NO-GO", "GO CONDITIONNEL"],
                    "description": "Final qualification decision"
                },
                "score_global": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 100,
                    "description": "Weighted global score out of 100"
                },
                "synthese": {
                    "type": "string",
                    "description": "Executive summary (3-5 sentences) for the account team"
                },
                "conditions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Required conditions if GO CONDITIONNEL, else empty list"
                },
                "next_steps": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Recommended immediate next steps"
                }
            },
            "required": ["decision", "score_global", "synthese", "conditions", "next_steps"]
        }
    }
]


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class CriterionScore:
    criterion: str
    score: int
    justification: str
    red_flags: list[str]

@dataclass
class AOMetadata:
    reference: str
    entite_adjudicatrice: str
    objet: str
    valeur_estimee: str
    date_limite_remise: str
    duree_marche: str = "N/A"
    classification: str = "Non précisé"
    procedure: str = "N/A"

@dataclass
class QualificationReport:
    metadata: AOMetadata
    criteria_scores: list[CriterionScore]
    decision: str
    score_global: int
    synthese: str
    conditions: list[str]
    next_steps: list[str]
    tokens_used: int
    processing_time_s: float
    generated_at: str


# ── Prompts ──────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Tu es un expert en qualification d'appels d'offres pour le secteur défense et sécurité national français.
Tu travailles pour une entreprise de conseil technologique (type ServiceNow, AWS, ou éditeur logiciel) qui répond à des marchés publics défense.

Ta mission est d'analyser un document d'appel d'offres et de produire une qualification rigoureuse selon 5 critères :

1. **conformite_reglementaire** — Exigences PSSIE, RGS, IGI 1300, hébergement souverain, qualification SecNumCloud, données sensibles
2. **fit_strategique** — Alignement avec les capacités de l'entreprise, références sectorielles, positionnement compétitif
3. **faisabilite_technique** — Complexité de l'implémentation, délais, dépendances techniques, intégration avec SI existant
4. **attractivite_commerciale** — Valeur du marché, marges estimées, durée, opportunités de renouvellement
5. **risques** — Risques contractuels, pénalités, dépendances clients, concurrence identifiée

Pour chaque critère : utilise l'outil `score_criterion`.
Pour les métadonnées : utilise `extract_metadata`.
Pour la décision finale : utilise `emit_go_nogo`.

Sois précis, factuel, et ancre chaque score dans le texte du document.
Ne commente pas ton processus — exécute directement les outils dans le bon ordre."""


# ── Core agent ───────────────────────────────────────────────────────────────

class AOQualifierAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"

    def qualify(self, ao_text: str) -> QualificationReport:
        """Run the full multi-step qualification pipeline on an AO document."""

        start = time.time()
        messages = [{"role": "user", "content": f"Voici le document d'appel d'offres à qualifier :\n\n---\n{ao_text}\n---\n\nProcède à la qualification complète."}]

        metadata = None
        criteria_scores = []
        go_nogo = None
        total_tokens = 0

        # Agentic loop — continue until model stops using tools
        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages
            )

            total_tokens += response.usage.input_tokens + response.usage.output_tokens

            # Collect tool calls from this turn
            tool_uses = [b for b in response.content if b.type == "tool_use"]
            tool_results = []

            for tool_use in tool_uses:
                name = tool_use.name
                inp = tool_use.input

                if name == "extract_metadata":
                    metadata = AOMetadata(**{k: inp.get(k, "N/A") for k in AOMetadata.__dataclass_fields__})
                    result = {"status": "ok", "message": "Métadonnées enregistrées."}

                elif name == "score_criterion":
                    cs = CriterionScore(
                        criterion=inp["criterion"],
                        score=inp["score"],
                        justification=inp["justification"],
                        red_flags=inp.get("red_flags", [])
                    )
                    criteria_scores.append(cs)
                    result = {"status": "ok", "message": f"Score {inp['criterion']} = {inp['score']}/10 enregistré."}

                elif name == "emit_go_nogo":
                    go_nogo = inp
                    result = {"status": "ok", "message": "Décision finale enregistrée."}

                else:
                    result = {"status": "error", "message": f"Outil inconnu : {name}"}

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": json.dumps(result)
                })

            # Append assistant turn + tool results to history
            messages.append({"role": "assistant", "content": response.content})
            if tool_results:
                messages.append({"role": "user", "content": tool_results})

            # Exit when model stops calling tools
            if response.stop_reason == "end_turn" or not tool_uses:
                break

        if not metadata or not go_nogo:
            raise RuntimeError("Pipeline incomplet : métadonnées ou décision manquantes.")

        return QualificationReport(
            metadata=metadata,
            criteria_scores=criteria_scores,
            decision=go_nogo["decision"],
            score_global=go_nogo["score_global"],
            synthese=go_nogo["synthese"],
            conditions=go_nogo.get("conditions", []),
            next_steps=go_nogo.get("next_steps", []),
            tokens_used=total_tokens,
            processing_time_s=round(time.time() - start, 2),
            generated_at=datetime.now().isoformat()
        )


# ── Report renderer ──────────────────────────────────────────────────────────

def render_report(report: QualificationReport) -> str:
    """Render a qualification report as a readable markdown string."""

    DECISION_EMOJI = {"GO": "✅", "NO-GO": "❌", "GO CONDITIONNEL": "⚠️"}
    emoji = DECISION_EMOJI.get(report.decision, "❓")

    lines = [
        f"# Rapport de Qualification AO — {report.metadata.reference}",
        f"*Généré le {report.generated_at[:10]} | {report.tokens_used} tokens | {report.processing_time_s}s*",
        "",
        "## 📋 Métadonnées",
        f"- **Entité** : {report.metadata.entite_adjudicatrice}",
        f"- **Objet** : {report.metadata.objet}",
        f"- **Valeur estimée** : {report.metadata.valeur_estimee}",
        f"- **Date limite** : {report.metadata.date_limite_remise}",
        f"- **Durée** : {report.metadata.duree_marche}",
        f"- **Classification** : {report.metadata.classification}",
        f"- **Procédure** : {report.metadata.procedure}",
        "",
        "## 📊 Scores par critère",
        ""
    ]

    WEIGHTS = {
        "conformite_reglementaire": 30,
        "fit_strategique": 25,
        "faisabilite_technique": 20,
        "attractivite_commerciale": 15,
        "risques": 10
    }

    for cs in report.criteria_scores:
        weight = WEIGHTS.get(cs.criterion, 20)
        bar = "█" * cs.score + "░" * (10 - cs.score)
        lines.append(f"### {cs.criterion.replace('_', ' ').title()} (pondération {weight}%)")
        lines.append(f"**Score : {cs.score}/10** `{bar}`")
        lines.append(f"> {cs.justification}")
        if cs.red_flags:
            lines.append("")
            for flag in cs.red_flags:
                lines.append(f"🚩 {flag}")
        lines.append("")

    lines += [
        "## 🎯 Décision",
        f"### {emoji} {report.decision} — Score global : {report.score_global}/100",
        "",
        f"{report.synthese}",
        ""
    ]

    if report.conditions:
        lines.append("### Conditions requises")
        for c in report.conditions:
            lines.append(f"- {c}")
        lines.append("")

    lines.append("### Prochaines étapes")
    for ns in report.next_steps:
        lines.append(f"1. {ns}")

    return "\n".join(lines)
