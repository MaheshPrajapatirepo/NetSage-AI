import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "network_incidents.csv")

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def create_target(df):
    df = df.copy()
    df["Critical_Incident"] = df["Severity"].apply(lambda x: 1 if x == "Critical" else 0)
    return df

def encode_features(df):
    df = df.copy()
    # store category orders for consistent encoding at prediction time
    device_cats   = sorted(df["Device"].unique().tolist())
    location_cats = sorted(df["Location"].unique().tolist())
    incident_cats = sorted(df["Incident_Type"].unique().tolist())

    df["Device"]        = df["Device"].apply(lambda x: device_cats.index(x))
    df["Location"]      = df["Location"].apply(lambda x: location_cats.index(x))
    df["Incident_Type"] = df["Incident_Type"].apply(lambda x: incident_cats.index(x))

    categories = {
        "Device"       : device_cats,
        "Location"     : location_cats,
        "Incident_Type": incident_cats
    }
    return df, categories

FEATURES = [
    "Device",
    "Location",
    "Incident_Type",
    "CPU_Usage",
    "Memory_Usage",
    "Packet_Loss_Percentage",
    "Resource_Stress",
    "Network_Stress"
]

def get_features_and_target(df):
    X = df[FEATURES]
    y = df["Critical_Incident"]
    return X, y