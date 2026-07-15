import argparse
import sys
import os

# anchor all paths to where main.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# make src/ importable
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from collector import generate_logs
from parser    import parse_logs
from features  import engineer_features
from inference import run_inference
from train     import train

RAW_LOG     = os.path.join(BASE_DIR, "data/raw/sample_syslog.log")
PARSED_CSV  = os.path.join(BASE_DIR, "data/processed/parsed_logs.csv")
FEATURE_CSV = os.path.join(BASE_DIR, "data/processed/feature_logs.csv")
ALERTS_CSV  = os.path.join(BASE_DIR, "data/processed/alerts.csv")


def run_pipeline(skip_collect=False, skip_train=False):
    print("\n=== NetSage-AI ===\n")

    if not skip_collect:
        print("[1/4] collecting logs...")
        generate_logs(output_path=RAW_LOG)
    else:
        print("[1/4] skipping log collection")

    print("\n[2/4] parsing logs...")
    parse_logs(input_path=RAW_LOG, output_path=PARSED_CSV)

    print("\n[3/4] engineering features...")
    engineer_features(input_path=PARSED_CSV, output_path=FEATURE_CSV)

    print("\n[4/4] running inference...")
    run_inference(input_path=FEATURE_CSV, output_path=ALERTS_CSV)

    if not skip_train:
        print("\n[+] training model...")
        train(input_path=FEATURE_CSV)

    print("\n=== pipeline complete ===")
    print("outputs:")
    print(f"  {PARSED_CSV}")
    print(f"  {FEATURE_CSV}")
    print(f"  {ALERTS_CSV}")


def main():
    parser = argparse.ArgumentParser(
        description="NetSage-AI — AI-powered NOC log analysis pipeline"
    )
    parser.add_argument("--skip-collect", action="store_true", help="skip log generation")
    parser.add_argument("--skip-train",   action="store_true", help="skip model training")
    parser.add_argument("--infer-only",   action="store_true", help="run inference only")

    args = parser.parse_args()

    if args.infer_only:
        print("\n=== NetSage-AI — inference only ===\n")
        run_inference(input_path=FEATURE_CSV, output_path=ALERTS_CSV)
        return

    run_pipeline(
        skip_collect=args.skip_collect,
        skip_train=args.skip_train
    )


if __name__ == "__main__":
    main()