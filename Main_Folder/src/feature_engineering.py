import pandas as pd
from pathlib import Path

INPUT_FILE = "Main_Folder/ds/processed/parsed_logs.csv"
OUTPUT_FILE = "Main_Folder/ds/processed/feature_logs.csv"

df = pd.read_csv(INPUT_FILE)

# --------------------------
# Severity Score
# --------------------------

df["Severity_Score"] = df["Severity"]

# --------------------------
# Protocol Risk
# --------------------------

protocol_risk = {
    "LINK": 2,
    "LINEPROTO": 2,
    "OSPF": 4,
    "BGP": 5,
    "SYS": 1
}

df["Protocol_Risk"] = (
    df["Protocol"]
    .map(protocol_risk)
    .fillna(1)
)

# --------------------------
# State Risk
# --------------------------

df["State_Risk"] = df["State"].apply(
    lambda x: 3 if x == "DOWN"
    else -2 if x == "UP"
    else 0
)

# --------------------------
# Incident Score
# --------------------------

df["Incident_Score"] = (
    df["Severity_Score"]
    + df["Protocol_Risk"]
    + df["State_Risk"]
)

# --------------------------
# Risk Level
# --------------------------

def classify(score):

    if score >= 12:
        return "CRITICAL"

    elif score >= 9:
        return "HIGH"

    elif score >= 5:
        return "MEDIUM"

    return "LOW"


df["Risk_Level"] = (
    df["Incident_Score"]
    .apply(classify)
)

Path(
    "Main_Folder/ds/processed"
).mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(df.head())

print(
    f"\nSaved to {OUTPUT_FILE}"
)