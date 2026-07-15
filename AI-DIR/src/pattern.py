import pandas as pd
import os

# pattern detection — finds recurring issues in the log data
# no ML needed here, just grouped analysis the way a NOC engineer
# would actually look at logs during a shift review


def load_features(path="AI-DIR/data/processed/feature_logs.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"feature logs not found: {path}")
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df


def protocol_hotspots(df):
    # which protocols are causing the most high/critical alerts
    high_risk = df[df["risk_level"].isin(["CRITICAL", "HIGH"])]
    summary = (
        high_risk.groupby("protocol")
        .agg(
            total_events=("protocol", "count"),
            avg_score=("incident_score", "mean"),
            critical_count=("risk_level", lambda x: (x == "CRITICAL").sum()),
            high_count=("risk_level", lambda x: (x == "HIGH").sum()),
        )
        .sort_values("total_events", ascending=False)
        .reset_index()
    )
    summary["avg_score"] = summary["avg_score"].round(2)
    return summary


def repeated_incidents(df, threshold=3):
    # find protocol + state combos that repeat more than threshold times
    # these are your recurring problems worth investigating
    grouped = (
        df.groupby(["protocol", "state", "risk_level"])
        .size()
        .reset_index(name="count")
    )
    repeated = grouped[grouped["count"] >= threshold].sort_values("count", ascending=False)
    return repeated


def hourly_spike(df):
    # find which hours had the most high risk events
    # useful for spotting patterns like nightly batch jobs causing flaps
    df = df.copy()
    df["hour"] = df["timestamp"].dt.hour
    high_risk = df[df["risk_level"].isin(["CRITICAL", "HIGH"])]
    hourly = (
        high_risk.groupby("hour")
        .size()
        .reset_index(name="event_count")
        .sort_values("event_count", ascending=False)
    )
    return hourly


def flapping_neighbors(df, threshold=2):
    # neighbors that go up and down repeatedly are flapping
    # filter only rows where neighbor is present
    df_n = df[df["neighbor"].notna()].copy()
    flap = (
        df_n.groupby(["neighbor", "protocol"])
        .agg(
            state_changes=("state", "nunique"),
            total_events=("neighbor", "count"),
        )
        .reset_index()
    )
    # flapping = neighbor appears multiple times with different states
    flap = flap[flap["total_events"] >= threshold].sort_values("total_events", ascending=False)
    return flap


def run_pattern_detection(input_path="AI-DIR/data/processed/feature_logs.csv",
                          output_path="AI-DIR/data/processed/patterns.csv"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = load_features(input_path)

    print("=== pattern detection ===\n")

    print("[ protocol hotspots ]")
    hotspots = protocol_hotspots(df)
    print(hotspots.to_string(index=False))

    print("\n[ repeated incidents ]")
    repeated = repeated_incidents(df)
    if repeated.empty:
        print("no repeated incidents found")
    else:
        print(repeated.to_string(index=False))

    print("\n[ hourly spikes ]")
    spikes = hourly_spike(df)
    if spikes.empty:
        print("no spikes found")
    else:
        print(spikes.head(5).to_string(index=False))

    print("\n[ flapping neighbors ]")
    flapping = flapping_neighbors(df)
    if flapping.empty:
        print("no flapping neighbors found")
    else:
        print(flapping.to_string(index=False))

    # save hotspots as the primary pattern output
    hotspots.to_csv(output_path, index=False)
    print(f"\npattern summary saved → {output_path}")

    return {
        "hotspots": hotspots,
        "repeated": repeated,
        "spikes":   spikes,
        "flapping": flapping,
    }


if __name__ == "__main__":
    run_pattern_detection()