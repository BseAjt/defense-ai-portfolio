"""
Defense KB Cache Optimizer — CLI

Usage:
    python main.py              # Run benchmark with built-in GNOSE KB sample
    python main.py --kb file    # Use custom KB text file
    python main.py --calls N    # Number of queries to run (default: 6)
    python main.py --json       # Output as JSON
"""

import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(__file__))

from src.cache_optimizer import KBCacheOptimizer, render_report, DEFENSE_KB_DOCUMENTS, QUERIES


def main():
    parser = argparse.ArgumentParser(description="Defense KB Prompt Cache Optimizer")
    parser.add_argument("--kb", type=str, help="Path to knowledge base text file")
    parser.add_argument("--calls", type=int, default=6, help="Number of queries to run")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-call output")
    args = parser.parse_args()

    print("🛡️  Defense KB Cache Optimizer")
    print("Benchmarking prompt caching on GNOSE knowledge base...\n")

    kb_text = DEFENSE_KB_DOCUMENTS
    if args.kb:
        with open(args.kb, "r", encoding="utf-8") as f:
            kb_text = f.read()
        print(f"KB loaded from: {args.kb}")

    queries = QUERIES[:args.calls]
    print(f"KB size: ~{len(kb_text.split()):,} words | Queries: {len(queries)}\n")

    optimizer = KBCacheOptimizer()
    report = optimizer.run_benchmark(kb_text, queries, show_progress=not args.quiet)

    print("\n" + "="*60)

    if args.json:
        import dataclasses
        print(json.dumps(dataclasses.asdict(report), ensure_ascii=False, indent=2))
    else:
        print(render_report(report))


if __name__ == "__main__":
    main()
