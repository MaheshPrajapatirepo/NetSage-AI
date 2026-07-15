import pandas as pd
import os

# severity and protocol risk values are based on real NOC impact levels
# higher number = higher risk

SEVERITY_SCORE = {
    "CRITICAL": 4,
    "ERROR":    3,
    "WARNING":  2,
    "INFO":     1,
}

PROTOCOL_RISK = {
    "BGP":   5,  # BGP down = potential full routing loss
    "ISIS":  5,
    "OSPF":  4,
    "EIGRP": 3,
    "HSRP":  3,  # redundancy loss but not routing itself
    "STP":   2,  # layer 2, contained impact
}

STATE_RISK = {
    "down":     4,
    "degraded": 3,
    "changed":  2,
    "up":       0,
    "unknown":  1,
}


def calculate_incident_score(row):
    # weighted formula — severity carries the most weight
    severity = SEVERITY_SCORE.get(row["severity"], 1)
    protocol = PROTOCOL_RISK.get(row["protocol"], 1)
    state    = STATE_RISK.get(row["state"], 1)
    return round((severity * 0.5) + (protocol * 0.3) + (state * 0.2), 2)


def assign_risk_level(score):
    if score >= 4.0:
        return "CRITICAL"
    if score >= 3.0:
        return "HIGH"
    if score >= 2.0:
        return "MEDIUM"
    return "LOW"


def engineer_features(input_path="data/processed/parsed_logs.csv",
                      output_path="data/processed/feature_logs.csv"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"parsed logs not found: {input_path}")

    df = pd.read_csv(input_path, parse_dates=["timestamp"])

    # map scores
    df["severity_score"] = df["severity"].map(SEVERITY_SCORE).fillna(1).astype(int)
    df["protocol_risk"]  = df["protocol"].map(PROTOCOL_RISK).fillna(1).astype(int)
    df["state_risk"]     = df["state"].map(STATE_RISK).fillna(1).astype(int)

    # incident score and risk level
    df["incident_score"] = df.apply(calculate_incident_score, axis=1)
    df["risk_level"]     = df["incident_score"].apply(assign_risk_level)

    # rolling event count — how many events in last 10 minutes per protocol
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["event_count_10m"] = (
        df.groupby("protocol")["timestamp"]
        .transform(lambda x: x.expanding().count())
        .astype(int)
    )

    df.to_csv(output_path, index=False)
    print(f"features engineered for {len(df)} records → {output_path}")
    return df


if __name__ == "__main__":
    engineer_features()