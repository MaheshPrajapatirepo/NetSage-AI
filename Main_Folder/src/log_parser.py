import pandas as pd
from pathlib import Path

RAW_LOG_FILE = "Main_Folder/ds/raw_logs/live_syslog.log"
OUTPUT_FILE = "Main_Folder/ds/processed/parsed_logs.csv"


def parse_log_line(log_line):

    log_line = log_line.strip()

    if not log_line:
        return None

    protocol = "UNKNOWN"
    severity = None
    event = "UNKNOWN"

    parsed = {
        "Protocol": protocol,
        "Severity": severity,
        "Event": event,
        "Interface": None,
        "Neighbor": None,
        "State": None,
        "Raw_Log": log_line
    }

    try:

        # Parse header
        header = log_line.split(":")[0]

        tokens = header.split("-")

        if len(tokens) >= 3:
            parsed["Protocol"] = tokens[0].replace("%", "")
            parsed["Severity"] = int(tokens[1])
            parsed["Event"] = tokens[2]

        # Interface extraction
        if "Interface" in log_line:
            try:
                parsed["Interface"] = (
                    log_line
                    .split("Interface")[1]
                    .split(",")[0]
                    .strip()
                )
            except Exception:
                pass

        # OSPF Neighbor extraction
        if "Nbr " in log_line:
            try:
                parsed["Neighbor"] = (
                    log_line
                    .split("Nbr ")[1]
                    .split()[0]
                    .strip()
                )
            except Exception:
                pass

        # BGP Neighbor extraction
        if "neighbor" in log_line.lower():
            try:
                parsed["Neighbor"] = (
                    log_line
                    .split("neighbor")[1]
                    .strip()
                    .split()[0]
                )
            except Exception:
                pass

        # State detection
        lower_log = log_line.lower()

        if "changed state to down" in lower_log:
            parsed["State"] = "DOWN"

        elif "changed state to up" in lower_log:
            parsed["State"] = "UP"

        elif "from full to down" in lower_log:
            parsed["State"] = "DOWN"

        elif "neighbor" in lower_log and " down" in lower_log:
            parsed["State"] = "DOWN"

        elif "neighbor" in lower_log and " up" in lower_log:
            parsed["State"] = "UP"

        return parsed

    except Exception as e:

        print(f"Error parsing line: {log_line}")
        print(e)

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

    print("\nParsed Logs Preview:\n")
    print(df.head())

    print(f"\nTotal Logs Parsed: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()