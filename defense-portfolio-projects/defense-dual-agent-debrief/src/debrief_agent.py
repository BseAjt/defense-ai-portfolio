"""
Defense Dual-Agent Debrief Synthesizer
Pattern: Multi-agent — Orchestrator + Specialist collaboration
Use case: Synthesis of operational/project debriefs for French defense IT

Architecture:
  OrchestratorAgent  — plans the synthesis strategy, assigns tasks to specialist
  SpecialistAgent    — deep-dives on a specific dimension (technical, regulatory, risk)
  OrchestratorAgent  — integrates specialist findings into final report

This demonstrates the core multi-agent pattern:
  - One agent cannot do everything well alone
  - Specialist agents produce higher-quality analysis on narrow domains
  - Orchestrator maintains coherence and avoids contradictions between specialists

Real value: A DIRISI project debrief has 4 orthogonal dimensions
(technical, regulatory, operational, financial) — each needs different expertise.
"""

import anthropic
import json
import time
from dataclasses import dataclass
from datetime import datetime


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class SpecialistReport:
    dimension: str
    findings: list[str]
    risks: list[str]
    recommendations: list[str]
    confidence: float

@dataclass
class DebriefSynthesis:
    project_name: str
    specialist_reports: list[SpecialistReport]
    key_lessons: list[str]
    blockers_identified: list[str]
    action_items: list[dict]   # [{owner, action, deadline, priority}]
    executive_summary: str
    overall_health: str        # "GREEN" | "AMBER" | "RED"
    total_tokens: int
    processing_time_s: float
    generated_at: str


# ── Agent definitions ─────────────────────────────────────────────────────────

ORCHESTRATOR_SYSTEM = """Tu es l'agent orchestrateur d'une synthèse de debrief projet défense.

Ton rôle :
1. Analyser le compte-rendu de debrief fourni
2. Identifier les 3 dimensions les plus critiques à approfondir (parmi : technique, réglementaire, opérationnel, financier, RH/équipe, sécurité)
3. Pour chaque dimension choisie, formuler une question d'analyse précise pour le spécialiste
4. Après avoir reçu les analyses spécialistes, les intégrer en une synthèse cohérente

Dans ce premier tour, réponds UNIQUEMENT avec un JSON structuré :
{
  "dimensions_to_analyze": [
    {"dimension": "<nom>", "specialist_query": "<question précise pour le spécialiste>"},
    ...
  ],
  "rationale": "<pourquoi ces 3 dimensions>"
}"""

SPECIALIST_SYSTEM = """Tu es un expert spécialiste en analyse de projets IT défense souverains.
On te fournit le compte-rendu d'un debrief projet et une dimension spécifique à analyser en profondeur.

Réponds UNIQUEMENT avec un JSON structuré :
{
  "dimension": "<nom de la dimension>",
  "findings": ["<constat 1>", "<constat 2>", ...],
  "risks": ["<risque 1>", "<risque 2>", ...],
  "recommendations": ["<recommandation 1>", ...],
  "confidence": <float 0.0-1.0>
}

Sois factuel et ancré dans le texte du debrief. Max 5 éléments par liste."""

INTEGRATION_SYSTEM = """Tu es l'agent orchestrateur en phase finale d'intégration.
Tu as reçu les analyses de 3 spécialistes sur un debrief projet défense.

Ton rôle : produire la synthèse intégrée finale. Réponds UNIQUEMENT avec un JSON :
{
  "key_lessons": ["<leçon 1>", "<leçon 2>", "<leçon 3>"],
  "blockers_identified": ["<bloquant 1>", ...],
  "action_items": [
    {"owner": "<rôle>", "action": "<action>", "deadline": "<délai>", "priority": "HIGH|MEDIUM|LOW"},
    ...
  ],
  "executive_summary": "<3-5 phrases pour le COMEX>",
  "overall_health": "GREEN|AMBER|RED"
}

Synthétise les analyses sans les répéter. Identifie les contradictions entre spécialistes si présentes."""


# ── Dual-Agent Orchestrator ──────────────────────────────────────────────────

class DualAgentDebriefSynthesizer:

    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"
        self.total_tokens = 0

    def _call(self, system: str, messages: list, label: str = "") -> str:
        """Single LLM call with token tracking."""
        if label:
            print(f"  🤖 {label}...")
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system,
            messages=messages
        )
        self.total_tokens += response.usage.input_tokens + response.usage.output_tokens
        return response.content[0].text

    def _parse_json(self, raw: str) -> dict:
        """Parse JSON, stripping markdown fences if needed."""
        clean = raw.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            clean = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        return json.loads(clean)

    def synthesize(self, debrief_text: str, project_name: str = "Project") -> DebriefSynthesis:
        """
        Run the full dual-agent synthesis pipeline:
        Step 1: Orchestrator plans — identifies dimensions to analyze
        Step 2: Specialist analyzes each dimension (separate LLM call per dimension)
        Step 3: Orchestrator integrates all specialist findings
        """
        start = time.time()
        self.total_tokens = 0

        print(f"\n🛡️  Dual-Agent Debrief Synthesis — {project_name}")
        print("="*55)

        # ── Step 1: Orchestrator planning ────────────────────────────────────
        print("\n📋 STEP 1 — Orchestrator: Planning analysis dimensions")
        plan_raw = self._call(
            system=ORCHESTRATOR_SYSTEM,
            messages=[{
                "role": "user",
                "content": f"Debrief projet '{project_name}':\n\n{debrief_text}\n\nIdentifie les 3 dimensions critiques."
            }],
            label="Orchestrator planning"
        )

        plan = self._parse_json(plan_raw)
        dimensions = plan.get("dimensions_to_analyze", [])
        print(f"  ✅ {len(dimensions)} dimensions identified: {[d['dimension'] for d in dimensions]}")
        print(f"  Rationale: {plan.get('rationale', '')[:120]}...")

        # ── Step 2: Specialist analysis per dimension ─────────────────────────
        print("\n🔬 STEP 2 — Specialist: Deep analysis per dimension")
        specialist_reports = []

        for dim in dimensions:
            report_raw = self._call(
                system=SPECIALIST_SYSTEM,
                messages=[{
                    "role": "user",
                    "content": (
                        f"Debrief projet '{project_name}':\n\n{debrief_text}\n\n"
                        f"Dimension à analyser: {dim['dimension']}\n"
                        f"Question spécifique: {dim['specialist_query']}"
                    )
                }],
                label=f"Specialist [{dim['dimension']}]"
            )

            report_data = self._parse_json(report_raw)
            specialist_reports.append(SpecialistReport(
                dimension=report_data.get("dimension", dim["dimension"]),
                findings=report_data.get("findings", []),
                risks=report_data.get("risks", []),
                recommendations=report_data.get("recommendations", []),
                confidence=float(report_data.get("confidence", 0.7))
            ))
            print(f"  ✅ {dim['dimension']}: {len(specialist_reports[-1].findings)} findings, {len(specialist_reports[-1].risks)} risks")

        # ── Step 3: Orchestrator integration ─────────────────────────────────
        print("\n🔗 STEP 3 — Orchestrator: Integrating specialist reports")

        specialist_summary = json.dumps(
            [{"dimension": r.dimension, "findings": r.findings,
              "risks": r.risks, "recommendations": r.recommendations}
             for r in specialist_reports],
            ensure_ascii=False, indent=2
        )

        integration_raw = self._call(
            system=INTEGRATION_SYSTEM,
            messages=[{
                "role": "user",
                "content": (
                    f"Projet: {project_name}\n\n"
                    f"Analyses spécialistes:\n{specialist_summary}\n\n"
                    f"Debrief original (résumé):\n{debrief_text[:1000]}...\n\n"
                    f"Produis la synthèse intégrée finale."
                )
            }],
            label="Orchestrator integration"
        )

        integration = self._parse_json(integration_raw)
        print(f"  ✅ Integration complete — Overall health: {integration.get('overall_health', '?')}")

        return DebriefSynthesis(
            project_name=project_name,
            specialist_reports=specialist_reports,
            key_lessons=integration.get("key_lessons", []),
            blockers_identified=integration.get("blockers_identified", []),
            action_items=integration.get("action_items", []),
            executive_summary=integration.get("executive_summary", ""),
            overall_health=integration.get("overall_health", "AMBER"),
            total_tokens=self.total_tokens,
            processing_time_s=round(time.time() - start, 2),
            generated_at=datetime.now().isoformat()
        )


# ── Eval functions ────────────────────────────────────────────────────────────

def eval_specialist_coverage(synthesis: DebriefSynthesis) -> dict:
    """All specialist reports should have findings."""
    all_have_findings = all(len(r.findings) > 0 for r in synthesis.specialist_reports)
    return {"name": "specialist_coverage", "passed": all_have_findings,
            "score": 1.0 if all_have_findings else 0.0}

def eval_action_items_complete(synthesis: DebriefSynthesis) -> dict:
    """Action items must have owner, action, deadline, priority."""
    required_keys = {"owner", "action", "deadline", "priority"}
    complete = all(required_keys.issubset(set(item.keys())) for item in synthesis.action_items)
    has_items = len(synthesis.action_items) > 0
    passed = complete and has_items
    return {"name": "action_items_complete", "passed": passed, "score": 1.0 if passed else 0.5 if has_items else 0.0}

def eval_health_status_valid(synthesis: DebriefSynthesis) -> dict:
    valid = synthesis.overall_health in ["GREEN", "AMBER", "RED"]
    return {"name": "health_status_valid", "passed": valid, "score": 1.0 if valid else 0.0}

def eval_no_empty_summary(synthesis: DebriefSynthesis) -> dict:
    has_summary = len(synthesis.executive_summary) > 50
    return {"name": "executive_summary_present", "passed": has_summary, "score": 1.0 if has_summary else 0.0}

def run_evals(synthesis: DebriefSynthesis) -> dict:
    evals = [
        eval_specialist_coverage(synthesis),
        eval_action_items_complete(synthesis),
        eval_health_status_valid(synthesis),
        eval_no_empty_summary(synthesis),
    ]
    overall = sum(e["score"] for e in evals) / len(evals)
    return {"overall": round(overall, 3), "passed": overall >= 0.75, "evals": evals}


# ── Renderer ──────────────────────────────────────────────────────────────────

HEALTH_EMOJI = {"GREEN": "🟢", "AMBER": "🟡", "RED": "🔴"}

def render_synthesis(s: DebriefSynthesis, eval_results: dict = None) -> str:
    lines = [
        f"# Debrief Synthesis — {s.project_name}",
        f"*{s.generated_at[:10]} | {s.total_tokens} tokens | {s.processing_time_s}s | 3 specialist agents*",
        "",
        f"## {HEALTH_EMOJI[s.overall_health]} Overall Health: {s.overall_health}",
        "",
        s.executive_summary,
        "",
        "## 🔬 Specialist Analyses",
    ]

    for r in s.specialist_reports:
        lines.append(f"\n### {r.dimension} (confidence: {r.confidence:.0%})")
        if r.findings:
            lines.append("**Findings:**")
            for f in r.findings: lines.append(f"  - {f}")
        if r.risks:
            lines.append("**Risks:**")
            for risk in r.risks: lines.append(f"  - ⚠️ {risk}")
        if r.recommendations:
            lines.append("**Recommendations:**")
            for rec in r.recommendations: lines.append(f"  - → {rec}")

    if s.key_lessons:
        lines += ["", "## 💡 Key Lessons"]
        for l in s.key_lessons: lines.append(f"  - {l}")

    if s.blockers_identified:
        lines += ["", "## 🚫 Blockers"]
        for b in s.blockers_identified: lines.append(f"  - {b}")

    if s.action_items:
        lines += ["", "## ✅ Action Items"]
        prio_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        sorted_actions = sorted(s.action_items, key=lambda x: prio_order.get(x.get("priority","LOW"), 2))
        for a in sorted_actions:
            p = a.get("priority", "")
            emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(p, "")
            lines.append(f"  {emoji} **{a.get('owner','')}** — {a.get('action','')} *(by {a.get('deadline','')})*")

    if eval_results:
        status = "✅ PASSED" if eval_results["passed"] else "❌ FAILED"
        lines += ["", f"## Eval: {status} ({eval_results['overall']:.0%})"]
        for e in eval_results["evals"]:
            icon = "✅" if e["passed"] else "❌"
            lines.append(f"  {icon} {e['name']}")

    return "\n".join(lines)
