# 📄 Defense Contract Analyzer

> **Pattern: Native PDF ingestion — multi-document contract review**  
> Built on the Anthropic Claude API — No external PDF parsing library required

## What it does
Analyzes French defense procurement contracts (PDFs) to flag risky clauses:
sovereignty obligations, penalty structures, IP transfers, termination conditions.
Uses Claude's **native PDF ingestion** — the document is passed directly as a base64 content block.

## Key patterns demonstrated
| Pattern | Implementation |
|---------|----------------|
| **Native PDF ingestion** | `source.type: base64, media_type: application/pdf` |
| **Agentic loop** | Tool use: extract_metadata → flag_risky_clause (×N) → emit_verdict |
| **Multi-document** | Sequential analysis + cross-document conflict detection |
| **Citations enabled** | `"citations": {"enabled": true}` on document block |

## Quickstart
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py --demo          # Generate synthetic contract + analyze
python main.py --file my.pdf   # Analyze your own contract
```
