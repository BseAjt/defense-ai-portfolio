"""
Defense AO Qualifier — CLI entrypoint

Usage:
    python main.py                          # Run on built-in sample AO
    python main.py --file path/to/ao.txt    # Run on a text file
    python main.py --eval                   # Run qualification + eval suite
    python main.py --json                   # Output as JSON
"""

import argparse
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from src.qualifier import AOQualifierAgent, render_report
from evals.eval_suite import run_eval_suite, render_eval_results
from examples.ao_sample import AO_SAMPLE_TEXT


def main():
    parser = argparse.ArgumentParser(description="Qualify a French defense procurement notice (AO)")
    parser.add_argument("--file", type=str, help="Path to AO text file")
    parser.add_argument("--eval", action="store_true", help="Run eval suite after qualification")
    parser.add_argument("--json", action="store_true", help="Output report as JSON")
    args = parser.parse_args()

    # Load AO text
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            ao_text = f.read()
        print(f"📄 AO chargé depuis : {args.file}")
    else:
        ao_text = AO_SAMPLE_TEXT
        print("📄 Utilisation de l'AO d'exemple (DIRISI-0847)")

    print("\n🔄 Qualification en cours...\n")

    agent = AOQualifierAgent()

    try:
        report = agent.qualify(ao_text)
    except Exception as e:
        print(f"❌ Erreur pipeline : {e}")
        sys.exit(1)

    # Output
    if args.json:
        import dataclasses
        print(json.dumps(dataclasses.asdict(report), ensure_ascii=False, indent=2))
    else:
        print(render_report(report))

    # Eval suite
    if args.eval:
        print("\n" + "─" * 60)
        print("🧪 Lancement de l'eval suite...\n")
        suite = run_eval_suite(report, ao_text)
        print(render_eval_results(suite))

    print(f"\n⏱  Temps de traitement : {report.processing_time_s}s | Tokens utilisés : {report.tokens_used}")


if __name__ == "__main__":
    main()
