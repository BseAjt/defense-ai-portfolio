# ⚡ Defense KB Cache Optimizer

> **Pattern: Prompt caching — cost & latency benchmarking**  
> Measure real savings when caching the GNOSE knowledge base

## What it does
Benchmarks prompt caching on a defense knowledge base, showing:
- Cache write cost (call 1) vs cache read cost (calls 2+)
- Real latency difference between cold and warm cache
- Projected savings at scale (850,000 GNOSE users)

## Key patterns demonstrated
| Pattern | Implementation |
|---------|----------------|
| **Prompt caching** | `cache_control: {type: ephemeral}` on KB content block |
| **Token tracking** | `cache_creation_input_tokens` vs `cache_read_input_tokens` |
| **Cost modeling** | Per-call USD cost with pricing breakdown |
| **Scale projection** | Monthly cost at 850K users × 10 queries |

## Quickstart
```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py           # Benchmark with built-in GNOSE KB
python main.py --calls 10  # Run 10 queries
python main.py --kb kb.txt --json  # Custom KB, JSON output
```
