import pandas as pd
from pathlib import Path

INPUT_FILE = "Main_Folder/ds/processed/feature_logs.csv"
OUTPUT_FILE = "Main_Folder/ds/processed/alerts.csv"


def generate_recommendation(row):

    protocol = row["Protocol"]
    state = row["State"]
    risk = row["Risk_Level"]

    if protocol == "BGP" and state == "DOWN":
        return (
            "Verify neighbor reachability | "
            "Check BGP session status | "
            "Validate routing policies"
        )

    elif protocol == "OSPF" and state == "DOWN":
        return (
            "Check OSPF adjacency | "
            "Verify interface connectivity | "
            "Review hello/dead timers"
        )

    elif protocol == "LINK" and state == "DOWN":
        return (
            "Check physical connectivity | "
            "Verify interface status | "
            "Review recent changes"
        )

    elif protocol == "LINEPROTO" and state == "DOWN":
        return (
            "Verify Layer-2 connectivity | "
            "Check encapsulation settings"
        )

    elif protocol == "SYS":
        return (
            "Review configuration changes"
        )

    return "No action required"


def main():

    df = pd.read_csv(INPUT_FILE)

    alerts = df[
        df["Risk_Level"].isin(
            ["HIGH", "CRITICAL"]
        )
    ].copy()

    alerts["Recommendation"] = alerts.apply(
        generate_recommendation,
        axis=1
    )

    Path(
        "Main_Folder/ds/processed"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    alerts.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nGenerated Alerts:\n")

    print(
        alerts[
            [
                "Protocol",
                "Event",
                "State",
                "Risk_Level",
                "Recommendation"
            ]
        ]
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()