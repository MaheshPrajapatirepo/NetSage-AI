import pandas as pd
import re
import os

# matches the exact format collector.py produces:
# 2024-01-15 10:23:45 CRITICAL BGP: BGP neighbor 10.0.0.1 is down
LOG_PATTERN = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<severity>CRITICAL|ERROR|WARNING|INFO)\s+"
    r"(?P<protocol>BGP|OSPF|EIGRP|STP|HSRP|ISIS):\s+"
    r"(?P<event>.+)"
)

# pull interface IPs out of the event string if present
INTERFACE_PATTERN = re.compile(r"GigabitEthernet\d+/\d+|FastEthernet\d+/\d+|Serial\d+/\d+/\d+|Loopback\d+")
NEIGHBOR_PATTERN  = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

# derive a short state from the event text
def extract_state(event):
    event_lower = event.lower()
    if any(w in event_lower for w in ["down", "idle", "blocking", "expired", "reset", "active route lost"]):
        return "down"
    if any(w in event_lower for w in ["up", "full", "forwarding", "active", "established"]):
        return "up"
    if any(w in event_lower for w in ["change", "changed", "topology", "flood"]):
        return "changed"
    if any(w in event_lower for w in ["warning", "stuck", "not received"]):
        return "degraded"
    return "unknown"


def parse_line(line):
    line = line.strip()
    if not line:
        return None

    match = LOG_PATTERN.match(line)
    if not match:
        return None  # skip malformed lines silently

    event     = match.group("event")
    interface = INTERFACE_PATTERN.search(event)
    neighbor  = NEIGHBOR_PATTERN.search(event)

    return {
        "timestamp": match.group("timestamp"),
        "severity":  match.group("severity"),
        "protocol":  match.group("protocol"),
        "event":     event,
        "interface": interface.group() if interface else None,
        "neighbor":  neighbor.group() if neighbor else None,
        "state":     extract_state(event),
    }


def parse_logs(input_path="AI-DIR/data/raw/sample_syslog.log",
               output_path="AI-DIR/data/processed/parsed_logs.csv"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"log file not found: {input_path}")

    with open(input_path, "r") as f:
        lines = f.readlines()

    records = []
    skipped = 0

    for line in lines:
        parsed = parse_line(line)
        if parsed:
            records.append(parsed)
        else:
            skipped += 1

    if not records:
        raise ValueError("no valid log lines found — check collector output")

    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    df.to_csv(output_path, index=False)
    print(f"parsed {len(df)} lines, skipped {skipped} → {output_path}")
    return df


if __name__ == "__main__":
    parse_logs()