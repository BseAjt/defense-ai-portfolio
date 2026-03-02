# 🛡️ Defense AO Qualifier

> **Agentic qualification pipeline for French defense procurement notices**  
> Built on the Anthropic Claude API — Multi-step reasoning with tool use and integrated evals

---

## What it does

This project automates the qualification of French defense procurement notices (Appels d'Offres) using an **agentic Claude workflow**. Given a raw AO document, the pipeline:

1. **Extracts structured metadata** (entity, value, deadline, classification level)
2. **Scores 5 qualification criteria** via function calling:
   - Regulatory compliance (PSSIE, RGS, IGI 1300, SecNumCloud)
   - Strategic fit
   - Technical feasibility
   - Commercial attractiveness
   - Risk profile
3. **Emits a weighted Go / No-Go / Go Conditionnel decision**
4. **Runs an eval suite** measuring output quality (coverage, consistency, groundedness)

The agent uses a **multi-turn agentic loop** — it calls tools iteratively until the full qualification is complete, without requiring step-by-step orchestration from the caller.

---

## Architecture

```
main.py                    # CLI entrypoint
src/
  qualifier.py             # Core agent — agentic loop + tool handling
evals/
  eval_suite.py            # 5 eval functions including LLM-as-judge
examples/
  ao_sample.py             # Synthetic AO fixture (DIRISI-style)
```

### Key design patterns

| Pattern | Where |
|---|---|
| **Tool use / function calling** | `TOOLS` in `qualifier.py` — 3 tools: `extract_metadata`, `score_criterion`, `emit_go_nogo` |
| **Agentic loop** | `AOQualifierAgent.qualify()` — iterates until `stop_reason == "end_turn"` |
| **LLM-as-judge eval** | `eval_justification_quality()` — uses `claude-haiku` to assess groundedness |
| **Deterministic evals** | Coverage, range validation, decision consistency |
| **Structured outputs** | Python dataclasses → JSON serializable reports |

---

## Quickstart

```bash
git clone https://github.com/<your-handle>/defense-ao-qualifier
cd defense-ao-qualifier
pip install -r requirements.txt

export ANTHROPIC_API_KEY="sk-ant-..."

# Run on built-in sample AO
python main.py

# Run with eval suite
python main.py --eval

# Run on your own AO file
python main.py --file path/to/ao.txt --eval

# JSON output
python main.py --json
```

---

## Sample output

```
# Rapport de Qualification AO — AO-2025-DIRISI-0847

## 📋 Métadonnées
- Entité : Direction Interarmées des Réseaux d'Infrastructure (DIRISI)
- Objet : Plateforme ITSM souveraine avec capacités d'automatisation IA
- Valeur estimée : 8 500 000 EUR
- Date limite : 2025-09-30
- Classification : Diffusion Restreinte (DR)

## 📊 Scores par critère
### Conformite Reglementaire (30%)
Score : 8/10  ████████░░
> Exigences PSSIE, RGS v2, IGI 1300 et hébergement territoire national explicitement mentionnées...

[...]

## 🎯 Décision
### ✅ GO — Score global : 74/100
Ce marché présente un fort alignement avec nos capacités ITSM défense...
```

---

## Eval suite

```
# Eval Results — AO-2025-DIRISI-0847
Score global : 91.0% | ✅ PASSED

✅ criteria_coverage — 100.0%
✅ score_range — 100.0%
✅ decision_consistency — 100.0%
✅ justification_quality — 85.0%
✅ red_flags_relevance — 80.0%
```

---

## Context & motivation

French defense procurement operates under strict regulatory constraints (PSSIE, IGI 1300, RGS, SecNumCloud) that make manual qualification time-intensive. This pipeline was built to explore how **LLM agents with structured tool use** can reduce qualification time from hours to minutes, while maintaining auditability through explainable scores and red flags.

The eval framework demonstrates a **shift from vibe-based LLM usage to measurable, repeatable outputs** — a prerequisite for deploying AI in regulated enterprise environments.

---

## Disclaimer

The sample AO (`examples/ao_sample.py`) is entirely fictional and created for testing purposes only. No real procurement information is included.

---

*Built with [Anthropic Claude API](https://docs.anthropic.com) · Python 3.11+*
