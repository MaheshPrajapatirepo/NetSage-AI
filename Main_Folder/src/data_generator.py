import random
import pandas as pd
from datetime import datetime, timedelta
import os

devices = [
    "R1-Core",
    "R2-Branch",
    "SW1-Access",
    "SW2-Distribution",
    "FW1-Perimeter"
]

incident_types = [
    "Interface Down",
    "High CPU Usage",
    "Packet Loss",
    "Route Flapping",
    "Memory Utilization High",
    "BGP Neighbor Down",
    "Latency Spike"
]

locations = [
    "Mumbai",
    "Delhi",
    "Pune",
    "Bangalore"
]

def generate_data(n=1000, seed=42):
    random.seed(seed)
    logs = []
    start_time = datetime.now()

    for i in range(n):
        timestamp    = start_time + timedelta(minutes=i * 5)
        device       = random.choice(devices)
        location     = random.choice(locations)
        # Correlated telemetry profiles — realistic network behavior
        incident_profile = random.random()

        if incident_profile > 0.85:
            # Stressed network — everything high together
            cpu_usage    = random.randint(85, 100)
            memory_usage = random.randint(80, 95)
            packet_loss  = round(random.uniform(8, 15), 2)

        elif incident_profile > 0.60:
            # Moderate stress
            cpu_usage    = random.randint(60, 85)
            memory_usage = random.randint(55, 80)
            packet_loss  = round(random.uniform(3, 8), 2)

        else:
            # Normal operation
            cpu_usage    = random.randint(20, 60)
            memory_usage = random.randint(30, 55)
            packet_loss  = round(random.uniform(0, 3), 2)

        # Incident generation
        if packet_loss > 10:
            incident = random.choice(["Packet Loss", "Route Flapping", "BGP Neighbor Down"])
        elif cpu_usage > 90:
            incident = random.choice(["High CPU Usage", "Memory Utilization High"])
        else:
            incident = random.choice(incident_types)

        # Risk scoring
        risk_score = 0
        if cpu_usage    > 95: risk_score += 5
        elif cpu_usage  > 85: risk_score += 3
        if memory_usage > 90: risk_score += 3
        elif memory_usage > 80: risk_score += 1
        if packet_loss  > 10: risk_score += 4
        elif packet_loss > 8: risk_score += 2
        if incident == "BGP Neighbor Down" : risk_score += 4
        elif incident == "Interface Down"  : risk_score += 3
        elif incident == "Route Flapping"  : risk_score += 2

        # Severity assignment
        # Force Critical if multiple metrics are simultaneously extreme
        if cpu_usage >= 90 and memory_usage >= 90:
            risk_score += 5

        if cpu_usage >= 90 and incident in ["BGP Neighbor Down", "Interface Down"]:
            risk_score += 3

        if risk_score >= 9:
            severity = "Critical"
        elif risk_score >= 6:
            severity = random.choices(["Critical", "Major"],  weights=[0.85, 0.15])[0]
        elif risk_score >= 3:
            severity = random.choices(["Major", "Warning"],   weights=[0.80, 0.20])[0]
        else:
            severity = "Warning"

        logs.append({
            "Timestamp"             : timestamp,
            "Device"                : device,
            "Location"              : location,
            "Incident_Type"         : incident,
            "Severity"              : severity,
            "CPU_Usage"             : cpu_usage,
            "Memory_Usage"          : memory_usage,
            "Packet_Loss_Percentage": packet_loss,
            "Resource_Stress"       : cpu_usage + memory_usage,
            "Network_Stress"        : round(packet_loss * 10, 2)
        })

    return pd.DataFrame(logs)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_data(n=1000)
    df.to_csv("data/network_incidents.csv", index=False)
    print(f"✅ Dataset generated — {len(df)} rows saved to data/network_incidents.csv")
    print(f"\nSeverity distribution:\n{df['Severity'].value_counts()}")