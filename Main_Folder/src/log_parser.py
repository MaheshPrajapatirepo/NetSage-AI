import pandas as pd
from pathlib import Path

RAW_LOG_FILE = "Main_Folder/data/raw_logs/sample_syslog.log"
OUTPUT_FILE = "data/processed/parsed_logs.csv"


def parse_log_line(log_line):

    log_line = log_line.strip()

    if not log_line:
        return None

    protocol = "UNKNOWN"
    severity = None
    event = "UNKNOWN"

    try:

        parts = log_line.split(":")

        header = parts[0]

        tokens = header.split("-")

        if len(tokens) >= 3:

            protocol = tokens[0].replace("%", "")

            severity = tokens[1]

            event = tokens[2]

        return {
            "Protocol": protocol,
            "Severity": severity,
            "Event": event,
            "Raw_Log": log_line
        }

    except Exception:

        return None


def main():

    parsed_logs = []

    with open(RAW_LOG_FILE, "r") as file:

        for line in file:

            parsed = parse_log_line(line)

            if parsed:
                parsed_logs.append(parsed)

    df = pd.DataFrame(parsed_logs)

    Path("data/processed").mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(df.head())

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()