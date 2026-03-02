"""
Eval framework — Measures qualification report quality across 4 dimensions.
Each eval uses Claude as a judge (LLM-as-judge pattern).
"""

import anthropic
import json
from dataclasses import dataclass
from typing import Callable
from src.qualifier import QualificationReport, render_report


@dataclass
class EvalResult:
    eval_name: str
    score: float          # 0.0 → 1.0
    passed: bool
    rationale: str


@dataclass
class EvalSuiteResult:
    report_reference: str
    evals: list[EvalResult]
    overall_score: float
    passed: bool


# ── Individual eval functions ────────────────────────────────────────────────

def eval_criteria_coverage(report: QualificationReport) -> EvalResult:
    """All 5 expected criteria must be present."""
    expected = {
        "conformite_reglementaire",
        "fit_strategique",
        "faisabilite_technique",
        "attractivite_commerciale",
        "risques"
    }
    found = {cs.criterion for cs in report.criteria_scores}
    missing = expected - found
    score = 1.0 if not missing else max(0.0, (5 - len(missing)) / 5)
    return EvalResult(
        eval_name="criteria_coverage",
        score=score,
        passed=not missing,
        rationale=f"Critères manquants : {missing}" if missing else "Tous les critères sont présents."
    )


def eval_score_range(report: QualificationReport) -> EvalResult:
    """All criterion scores must be in [0, 10] and score_global in [0, 100]."""
    issues = []
    for cs in report.criteria_scores:
        if not (0 <= cs.score <= 10):
            issues.append(f"{cs.criterion}: {cs.score} hors plage")
    if not (0 <= report.score_global <= 100):
        issues.append(f"score_global={report.score_global} hors plage")
    passed = not issues
    return EvalResult(
        eval_name="score_range",
        score=1.0 if passed else 0.0,
        passed=passed,
        rationale="; ".join(issues) if issues else "Tous les scores sont dans les plages attendues."
    )


def eval_decision_consistency(report: QualificationReport) -> EvalResult:
    """Decision must be consistent with score_global."""
    score = report.score_global
    decision = report.decision
    consistent = (
        (decision == "GO" and score >= 65) or
        (decision == "GO CONDITIONNEL" and 40 <= score < 65) or
        (decision == "NO-GO" and score < 40)
    )
    return EvalResult(
        eval_name="decision_consistency",
        score=1.0 if consistent else 0.0,
        passed=consistent,
        rationale=(
            f"Cohérent : {decision} avec score {score}/100"
            if consistent else
            f"Incohérent : {decision} avec score {score}/100"
        )
    )


def eval_justification_quality(report: QualificationReport, ao_text: str) -> EvalResult:
    """LLM-as-judge: are justifications grounded in the document?"""
    client = anthropic.Anthropic()

    justifications_text = "\n".join(
        f"- {cs.criterion}: {cs.justification}"
        for cs in report.criteria_scores
    )

    prompt = f"""Tu es un évaluateur expert. Ci-dessous, le document AO original et les justifications produites par un agent de qualification.

DOCUMENT AO (extrait) :
{ao_text[:3000]}

JUSTIFICATIONS :
{justifications_text}

Évalue si les justifications sont :
1. Ancrées dans le contenu réel du document (pas inventées)
2. Précises et factuelles
3. Suffisamment détaillées

Réponds UNIQUEMENT en JSON avec ce format :
{{"score": <float entre 0 et 1>, "rationale": "<explication courte>"}}"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        result = json.loads(response.content[0].text)
        score = float(result["score"])
        return EvalResult(
            eval_name="justification_quality",
            score=score,
            passed=score >= 0.7,
            rationale=result.get("rationale", "")
        )
    except Exception as e:
        return EvalResult(
            eval_name="justification_quality",
            score=0.0,
            passed=False,
            rationale=f"Erreur parsing judge: {e}"
        )


def eval_red_flags_relevance(report: QualificationReport) -> EvalResult:
    """Red flags, if present, should be non-empty strings."""
    all_flags = [flag for cs in report.criteria_scores for flag in cs.red_flags]
    if not all_flags:
        # Acceptable if score is high
        avg_score = sum(cs.score for cs in report.criteria_scores) / max(len(report.criteria_scores), 1)
        passed = avg_score >= 7
        return EvalResult(
            eval_name="red_flags_relevance",
            score=1.0 if passed else 0.5,
            passed=passed,
            rationale="Aucun red flag — cohérent avec les scores élevés." if passed else "Aucun red flag malgré des scores bas."
        )
    empty = [f for f in all_flags if not f.strip()]
    score = 1.0 if not empty else max(0.0, (len(all_flags) - len(empty)) / len(all_flags))
    return EvalResult(
        eval_name="red_flags_relevance",
        score=score,
        passed=score >= 0.8,
        rationale=f"{len(all_flags)} red flags identifiés, {len(empty)} vides."
    )


# ── Eval suite runner ────────────────────────────────────────────────────────

def run_eval_suite(report: QualificationReport, ao_text: str) -> EvalSuiteResult:
    """Run all evals and return aggregated results."""

    evals = [
        eval_criteria_coverage(report),
        eval_score_range(report),
        eval_decision_consistency(report),
        eval_justification_quality(report, ao_text),
        eval_red_flags_relevance(report),
    ]

    overall = sum(e.score for e in evals) / len(evals)

    return EvalSuiteResult(
        report_reference=report.metadata.reference,
        evals=evals,
        overall_score=round(overall, 3),
        passed=overall >= 0.75
    )


def render_eval_results(suite: EvalSuiteResult) -> str:
    lines = [
        f"# Eval Results — {suite.report_reference}",
        f"**Score global : {suite.overall_score:.1%}** | {'✅ PASSED' if suite.passed else '❌ FAILED'}",
        ""
    ]
    for e in suite.evals:
        status = "✅" if e.passed else "❌"
        lines.append(f"### {status} {e.eval_name} — {e.score:.1%}")
        lines.append(f"> {e.rationale}")
        lines.append("")
    return "\n".join(lines)
