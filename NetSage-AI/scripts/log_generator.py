import random
import pandas as pd
from datetime import datetime, timedelta

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

logs = []

start_time = datetime.now()

for i in range(500):

    timestamp = start_time + timedelta(minutes=i * 5)

    device = random.choice(devices)

    location = random.choice(locations)

    cpu_usage = random.randint(20, 100)

    memory_usage = random.randint(30, 95)

    packet_loss = round(random.uniform(0, 15), 2)

    # Incident generation
    if packet_loss > 10:
        incident = random.choice([
            "Packet Loss",
            "Route Flapping",
            "BGP Neighbor Down"
        ])

    elif cpu_usage > 90:
        incident = random.choice([
            "High CPU Usage",
            "Memory Utilization High"
        ])

    else:
        incident = random.choice(incident_types)

    # Risk scoring
    risk_score = 0

    if cpu_usage > 85:
        risk_score += 2

    if memory_usage > 90:
        risk_score += 2

    if packet_loss > 8:
        risk_score += 3

    if incident == "BGP Neighbor Down":
        risk_score += 3

    if incident == "Interface Down":
        risk_score += 2

    # Severity assignment
    if risk_score >= 6:
        severity = "Critical"

    elif risk_score >= 3:
        severity = "Major"

    else:
        severity = "Warning"

    logs.append({
        "Timestamp": timestamp,
        "Device": device,
        "Location": location,
        "Incident_Type": incident,
        "Severity": severity,
        "CPU_Usage": cpu_usage,
        "Memory_Usage": memory_usage,
        "Packet_Loss_Percentage": packet_loss,
        "Resource_Stress": cpu_usage + memory_usage,
        "Network_Stress": packet_loss * 10
    })

df = pd.DataFrame(logs)

df.to_csv(
    "../NetSage-AI/data/network_incidents.csv",
    index=False
)
print("Network incident dataset generated successfully.")