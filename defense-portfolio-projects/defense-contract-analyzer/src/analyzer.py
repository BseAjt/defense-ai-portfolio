"""
Defense Contract Analyzer
Pattern: Document analysis — native PDF ingestion via Anthropic API (base64)
Use case: Multi-document contract review for French defense procurement

Demonstrates:
- Native PDF ingestion (no external parsing library needed)
- Multi-document context (compare several contract versions)
- Structured extraction with tool use
- Clause-level risk flagging
"""

import anthropic
import base64
import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime


# ── Data structures ──────────────────────────────────────────────────────────

@dataclass
class ContractClause:
    clause_id: str
    title: str
    risk_level: str          # "LOW" | "MEDIUM" | "HIGH" | "BLOCKER"
    risk_type: str           # e.g. "penalite", "resiliation", "souverainete", "ip"
    summary: str
    original_excerpt: str    # verbatim short quote from the contract
    recommendation: str

@dataclass
class ContractSummary:
    document_name: str
    parties: list[str]
    contract_value: str
    duration: str
    governing_law: str
    classification_requirements: str
    key_clauses: list[ContractClause]
    overall_risk: str        # "ACCEPTABLE" | "NEEDS_REVIEW" | "REJECT"
    executive_summary: str
    tokens_used: int
    processing_time_s: float
    analyzed_at: str

@dataclass
class MultiDocReport:
    documents_analyzed: int
    summaries: list[ContractSummary]
    cross_document_conflicts: list[str]
    consolidated_risk: str
    recommended_action: str


# ── Tools ────────────────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "extract_contract_metadata",
        "description": "Extract key metadata from the contract document.",
        "input_schema": {
            "type": "object",
            "properties": {
                "parties": {
                    "type": "array", "items": {"type": "string"},
                    "description": "List of contracting parties"
                },
                "contract_value": {"type": "string", "description": "Total contract value with currency"},
                "duration": {"type": "string", "description": "Contract duration and renewal options"},
                "governing_law": {"type": "string", "description": "Applicable law and jurisdiction"},
                "classification_requirements": {
                    "type": "string",
                    "description": "Data classification requirements (PSSIE, IGI 1300, SecNumCloud, etc.)"
                }
            },
            "required": ["parties", "contract_value", "duration", "governing_law", "classification_requirements"]
        }
    },
    {
        "name": "flag_risky_clause",
        "description": "Flag a contract clause as requiring attention. Call once per risky clause identified.",
        "input_schema": {
            "type": "object",
            "properties": {
                "clause_id": {"type": "string", "description": "Article or section reference (e.g. 'Article 12.3')"},
                "title": {"type": "string", "description": "Short clause title"},
                "risk_level": {
                    "type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "BLOCKER"],
                    "description": "Risk severity. BLOCKER = deal-stopper requiring legal/management escalation"
                },
                "risk_type": {
                    "type": "string",
                    "enum": ["penalite", "resiliation", "souverainete", "propriete_intellectuelle",
                             "responsabilite", "confidentialite", "sous_traitance", "exclusivite", "autre"]
                },
                "summary": {"type": "string", "description": "2-sentence risk summary"},
                "original_excerpt": {"type": "string", "description": "Verbatim excerpt (max 200 chars) from the clause"},
                "recommendation": {"type": "string", "description": "Specific recommended action or negotiation point"}
            },
            "required": ["clause_id", "title", "risk_level", "risk_type", "summary", "original_excerpt", "recommendation"]
        }
    },
    {
        "name": "emit_contract_verdict",
        "description": "Emit the final analysis verdict after reviewing all clauses.",
        "input_schema": {
            "type": "object",
            "properties": {
                "overall_risk": {
                    "type": "string", "enum": ["ACCEPTABLE", "NEEDS_REVIEW", "REJECT"],
                    "description": "Overall contract risk assessment"
                },
                "executive_summary": {
                    "type": "string",
                    "description": "3-5 sentence executive summary for non-legal stakeholders"
                }
            },
            "required": ["overall_risk", "executive_summary"]
        }
    }
]

SYSTEM_PROMPT = """Tu es un expert en droit des marchés publics de défense français et en contrats IT souverains.
Tu analyses des contrats pour identifier les clauses à risque pour un prestataire technologique (éditeur logiciel, intégrateur) répondant à des marchés défense.

Tes priorités d'analyse, dans l'ordre :
1. Clauses de souveraineté et localisation des données (PSSIE, IGI 1300, SecNumCloud) — toute ambiguïté est un risque BLOCKER
2. Pénalités et SLA (taux, plafond, mécanisme de calcul)
3. Propriété intellectuelle (cession de droits sur les développements spécifiques)
4. Clauses de résiliation (conditions, préavis, indemnisation)
5. Responsabilité et garanties

Procédure :
1. Utilise extract_contract_metadata en premier
2. Utilise flag_risky_clause pour chaque clause problématique identifiée (0 à N fois)
3. Utilise emit_contract_verdict en dernier

Sois précis et factuel. Cite le texte original. Ne recommande pas de refuser un contrat sans identifier une clause BLOCKER spécifique."""


# ── PDF loader ───────────────────────────────────────────────────────────────

def load_pdf_as_base64(path: str) -> str:
    """Load a PDF file and return base64-encoded content."""
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def make_pdf_content_block(pdf_b64: str, filename: str) -> dict:
    """Create an Anthropic API content block for a PDF document."""
    return {
        "type": "document",
        "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": pdf_b64
        },
        "title": filename,
        "citations": {"enabled": True}   # Enable source citations in responses
    }


# ── Core analyzer ────────────────────────────────────────────────────────────

class ContractAnalyzer:
    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-6"

    def analyze_pdf(self, pdf_path: str) -> ContractSummary:
        """
        Analyze a single contract PDF using native PDF ingestion.
        No external PDF parsing library required — Claude reads the PDF directly.
        """
        start = time.time()
        filename = Path(pdf_path).name

        print(f"  📄 Loading PDF: {filename}")
        pdf_b64 = load_pdf_as_base64(pdf_path)

        # Build message with PDF as a native document block
        messages = [{
            "role": "user",
            "content": [
                make_pdf_content_block(pdf_b64, filename),
                {
                    "type": "text",
                    "text": f"Analyse ce contrat de marché défense '{filename}'. Identifie toutes les clauses à risque et émets ton verdict."
                }
            ]
        }]

        metadata = None
        clauses = []
        verdict = None
        total_tokens = 0

        # Agentic loop
        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages
            )
            total_tokens += response.usage.input_tokens + response.usage.output_tokens

            tool_uses = [b for b in response.content if b.type == "tool_use"]
            tool_results = []

            for tu in tool_uses:
                inp = tu.input
                if tu.name == "extract_contract_metadata":
                    metadata = inp
                    result = {"status": "ok"}
                elif tu.name == "flag_risky_clause":
                    clauses.append(ContractClause(**inp))
                    result = {"status": "ok", "message": f"Clause {inp['clause_id']} ({inp['risk_level']}) enregistrée."}
                elif tu.name == "emit_contract_verdict":
                    verdict = inp
                    result = {"status": "ok"}
                else:
                    result = {"status": "error", "message": f"Unknown tool: {tu.name}"}

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tu.id,
                    "content": json.dumps(result)
                })

            messages.append({"role": "assistant", "content": response.content})
            if tool_results:
                messages.append({"role": "user", "content": tool_results})

            if response.stop_reason == "end_turn" or not tool_uses:
                break

        if not metadata or not verdict:
            raise RuntimeError(f"Incomplete analysis for {filename}")

        return ContractSummary(
            document_name=filename,
            parties=metadata.get("parties", []),
            contract_value=metadata.get("contract_value", "N/A"),
            duration=metadata.get("duration", "N/A"),
            governing_law=metadata.get("governing_law", "N/A"),
            classification_requirements=metadata.get("classification_requirements", "Non précisé"),
            key_clauses=clauses,
            overall_risk=verdict["overall_risk"],
            executive_summary=verdict["executive_summary"],
            tokens_used=total_tokens,
            processing_time_s=round(time.time() - start, 2),
            analyzed_at=datetime.now().isoformat()
        )

    def analyze_multiple(self, pdf_paths: list[str]) -> MultiDocReport:
        """
        Analyze multiple contract documents and detect cross-document conflicts.
        Each document is analyzed independently, then conflicts are surfaced.
        """
        summaries = []
        for path in pdf_paths:
            print(f"\n🔍 Analyzing: {Path(path).name}")
            summary = self.analyze_pdf(path)
            summaries.append(summary)
            print(f"   ✅ {summary.overall_risk} — {len(summary.key_clauses)} clauses flagged")

        conflicts = self._detect_conflicts(summaries) if len(summaries) > 1 else []

        risk_ranks = {"ACCEPTABLE": 0, "NEEDS_REVIEW": 1, "REJECT": 2}
        max_risk = max(summaries, key=lambda s: risk_ranks.get(s.overall_risk, 0))

        blockers = [c for s in summaries for c in s.key_clauses if c.risk_level == "BLOCKER"]
        if blockers or max_risk.overall_risk == "REJECT":
            action = "ESCALATE TO LEGAL — BLOCKER clauses identified. Do not sign without resolution."
        elif max_risk.overall_risk == "NEEDS_REVIEW":
            action = "NEGOTIATE — High-risk clauses require amendment before signature."
        else:
            action = "PROCEED — Standard review and signature workflow."

        return MultiDocReport(
            documents_analyzed=len(summaries),
            summaries=summaries,
            cross_document_conflicts=conflicts,
            consolidated_risk=max_risk.overall_risk,
            recommended_action=action
        )

    def _detect_conflicts(self, summaries: list[ContractSummary]) -> list[str]:
        """Detect conflicts between documents (e.g. conflicting governing law, IP clauses)."""
        conflicts = []
        laws = set(s.governing_law for s in summaries if s.governing_law != "N/A")
        if len(laws) > 1:
            conflicts.append(f"Conflicting governing law across documents: {', '.join(laws)}")

        classification_levels = set(s.classification_requirements for s in summaries)
        if len(classification_levels) > 1:
            conflicts.append(f"Inconsistent classification requirements: {', '.join(classification_levels)}")

        return conflicts


# ── Report renderer ──────────────────────────────────────────────────────────

RISK_EMOJI = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴", "BLOCKER": "🚫"}
VERDICT_EMOJI = {"ACCEPTABLE": "✅", "NEEDS_REVIEW": "⚠️", "REJECT": "❌"}

def render_summary(s: ContractSummary) -> str:
    lines = [
        f"# Contract Analysis — {s.document_name}",
        f"*{s.analyzed_at[:10]} | {s.tokens_used} tokens | {s.processing_time_s}s*",
        "",
        "## 📋 Contract Overview",
        f"- **Parties**: {', '.join(s.parties)}",
        f"- **Value**: {s.contract_value}",
        f"- **Duration**: {s.duration}",
        f"- **Governing Law**: {s.governing_law}",
        f"- **Classification**: {s.classification_requirements}",
        "",
        f"## {VERDICT_EMOJI[s.overall_risk]} Verdict: {s.overall_risk}",
        "",
        s.executive_summary,
        ""
    ]

    if s.key_clauses:
        lines.append(f"## ⚠️ Flagged Clauses ({len(s.key_clauses)})")
        for c in sorted(s.key_clauses, key=lambda x: ["LOW","MEDIUM","HIGH","BLOCKER"].index(x.risk_level), reverse=True):
            lines += [
                f"### {RISK_EMOJI[c.risk_level]} {c.clause_id} — {c.title}",
                f"**Risk**: {c.risk_level} | **Type**: {c.risk_type}",
                f"> {c.summary}",
                f"",
                f"*Excerpt*: \"{c.original_excerpt}\"",
                f"",
                f"**Recommendation**: {c.recommendation}",
                ""
            ]
    else:
        lines.append("## ✅ No significant clauses flagged.")

    return "\n".join(lines)
