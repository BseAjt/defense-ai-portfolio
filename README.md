# Defense AI Portfolio — Claude API

> Agentic AI workflows built on the Anthropic Claude API  
> Applied to French defense & sovereign public sector use cases

---

## About

This portfolio demonstrates hands-on experience with the Anthropic Claude API across **5 distinct architectural patterns**, all grounded in real-world constraints from French defense IT deployments (PSSIE, IGI 1300, RGS v2, SecNumCloud).

**Context:** 15 years in French defense IT. Primary account: French Ministry of Armed Forces (850,000 users). These projects explore how frontier LLMs can be deployed responsibly in sovereign, regulated environments.

---

## Projects

| # | Project | Pattern | Defense Use Case |
|---|---------|---------|------------------|
| 1 | [defense-ao-qualifier](./defense-ao-qualifier) | Agentic loop · Tool use · Evals | Automatic qualification of defense RFPs |
| 2 | [defense-contract-analyzer](./defense-contract-analyzer) | Native PDF ingestion · Multi-document | Contract risk analysis |
| 3 | [defense-incident-classifier](./defense-incident-classifier) | Streaming · Structured output | Real-time ITSM incident triage |
| 4 | [defense-dual-agent-debrief](./defense-dual-agent-debrief) | Multi-agent · Orchestrator/Specialist | Project debrief synthesis |
| 5 | [defense-kb-cache-optimizer](./defense-kb-cache-optimizer) | Prompt caching · Cost benchmarking | GNOSE knowledge base optimization |

---

## Project Summaries

### 1. Defense AO Qualifier
Qualifies French defense procurement notices (Appels d'Offres) using a multi-turn agentic loop. Scores 5 criteria (regulatory compliance, strategic fit, technical feasibility, commercial attractiveness, risk) via tool use, then emits a weighted Go/No-Go decision.

**Key patterns:** `tool_use` · `agentic loop` · `LLM-as-judge evals` · `structured outputs`
```bash
cd defense-ao-qualifier && python main.py --eval
```

### 2. Defense Contract Analyzer
Analyzes defense IT contracts (PDFs) to flag risky clauses: sovereignty obligations, penalty structures, IP transfers, termination conditions. Uses Claude's native PDF ingestion — no external parsing library required.

**Key patterns:** `PDF base64 ingestion` · `citations enabled` · `multi-document comparison` · `agentic loop`
```bash
cd defense-contract-analyzer && python main.py --demo
```

### 3. Defense Incident Classifier
Classifies ITSM incidents P1–P4 in real-time with streaming API. Routes to the correct team and flags sovereign/classified data involvement. Includes a security-critical eval: classification boundary violations trigger immediate escalation.

**Key patterns:** `streaming` · `structured JSON output` · `deterministic evals` · `sovereign data detection`
```bash
cd defense-incident-classifier && python main.py --batch --eval
```

### 4. Dual-Agent Debrief Synthesizer
Synthesizes project debriefs using two collaborating agents: an Orchestrator that plans the analysis strategy and integrates findings, and a Specialist that deep-dives each dimension independently (3 separate LLM calls).

**Key patterns:** `multi-agent` · `orchestrator/specialist` · `structured handoff` · `JSON context passing`
```bash
cd defense-dual-agent-debrief && python main.py --eval
```

### 5. KB Cache Optimizer
Benchmarks prompt caching on the GNOSE defense knowledge base. Measures real cache_creation vs cache_read token costs, latency delta between cold and warm cache, and projects monthly savings at 850,000-user scale.

**Key patterns:** `prompt caching` · `cache_control ephemeral` · `cost modeling` · `scale projection`
```bash
cd defense-kb-cache-optimizer && python main.py --calls 6
```

---

## Sovereign Deployment Context

| Constraint | Implementation |
|------------|----------------|
| IGI 1300 | Classification-aware routing: NC data via API, DR data via sovereign endpoint |
| PSSIE | No sensitive data in prompts: field-level filtering before LLM context |
| SecNumCloud | Architecture patterns documented for SecNumCloud-qualified providers |
| Audit trail | All LLM calls logged with token counts, latency, and classification tier |

All projects are designed with French defense sovereignty constraints in mind.

---

## Technical Write-up

For the full architecture analysis of LLM deployment in French sovereign defense infrastructure:  
**[LLM Deployment in Sovereign French Defense Infrastructure](./docs/llm-sovereign-defense.md)**

Covers: regulatory landscape (PSSIE, IGI 1300, RGS, SecNumCloud), 3 deployment patterns, Claude-specific gaps and opportunities, eval framework for classified environments, integration with CONCERTO, ALLIANCE, ServiceNow DIADME.

---

## Quickstart

```bash
# Clone
git clone https://github.com/sherpers/defense-ai-portfolio
cd defense-ai-portfolio

# Install
pip install anthropic reportlab

# Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run any project
cd defense-ao-qualifier && python main.py --eval
```

**Requirements:** Python 3.11+ · `anthropic>=0.40.0` · API key from [console.anthropic.com](https://console.anthropic.com)

---

## Author

**Sébastien Herpers**  
Advisory Solution Consultant, French Defense & Public Sector  
15 years: Naval Group · Atos · ServiceNow · Ministry of Armed Forces (850,000 users)  
Organizer, GenAI Think Tank — École de Guerre Économique  
[LinkedIn](https://linkedin.com/in/sherpers)

---

*All use cases are fictional or based on publicly available information. No classified data is included.*
