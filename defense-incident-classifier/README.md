# 🚨 Defense ITSM Incident Classifier

> **Pattern: Streaming + structured output**  
> Real-time triage of IT incidents for French defense operations

## What it does
Classifies ITSM incidents (P1→P4), routes to the correct team, and flags
sovereign/classified data involvement — in real-time with streaming.

## Key patterns demonstrated
| Pattern | Implementation |
|---------|----------------|
| **Streaming API** | `client.messages.stream()` with live token display |
| **Structured output** | JSON schema enforced via system prompt |
| **Sovereign flag** | Deterministic keyword detection + LLM classification |
| **Eval suite** | 4 evals including security-critical classification boundary |

## Quickstart
```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py                  # Demo: 2 incidents with live streaming
python main.py --batch --eval   # All 5 demo incidents + eval suite
python main.py --incident "..."  # Classify your own incident
```
