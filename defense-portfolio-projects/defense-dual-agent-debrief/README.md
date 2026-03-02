# 🤝 Defense Dual-Agent Debrief Synthesizer

> **Pattern: Multi-agent — Orchestrator + Specialist collaboration**  
> 3-step pipeline: plan → specialize → integrate

## What it does
Synthesizes project debriefs using two agents:
1. **OrchestratorAgent** identifies the 3 most critical dimensions
2. **SpecialistAgent** deep-dives each dimension independently (3 separate LLM calls)
3. **OrchestratorAgent** integrates findings into a coherent final report

## Key patterns demonstrated
| Pattern | Implementation |
|---------|----------------|
| **Multi-agent** | Orchestrator plans; Specialist executes; Orchestrator integrates |
| **Separation of concerns** | Each agent has a focused system prompt |
| **Token efficiency** | 3 targeted calls < 1 monolithic call for deep analysis |
| **Structured handoff** | JSON passed between agents as structured context |

## Quickstart
```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py             # Demo on DIADÈME Phase 2 debrief
python main.py --eval      # With eval suite
python main.py --file d.txt # Your own debrief
```
