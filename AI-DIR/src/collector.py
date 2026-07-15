import random
import datetime
import os

# log templates that reflect real NOC scenarios
# kept simple but realistic enough for pattern detection later

PROTOCOLS = ["BGP", "OSPF", "EIGRP", "STP", "HSRP", "ISIS"]
INTERFACES = ["GigabitEthernet0/0", "GigabitEthernet0/1", "FastEthernet0/0", "Serial0/0/0", "Loopback0"]
SEVERITIES = ["CRITICAL", "ERROR", "WARNING", "INFO"]
NEIGHBORS = ["10.0.0.1", "10.0.0.2", "192.168.1.1", "172.16.0.1"]

EVENTS = {
    "BGP": [
        "BGP neighbor {neighbor} is down",
        "BGP neighbor {neighbor} state changed to Idle",
        "BGP session with {neighbor} reset due to hold timer expired",
        "BGP neighbor {neighbor} is up",
    ],
    "OSPF": [
        "OSPF adjacency with {neighbor} on {interface} is down",
        "OSPF neighbor {neighbor} changed state to FULL",
        "OSPF dead interval expired on {interface}",
        "OSPF hello packet not received on {interface}",
    ],
    "EIGRP": [
        "EIGRP neighbor {neighbor} is down",
        "EIGRP adjacency reset on {interface}",
        "EIGRP stuck in active on {interface}",
        "EIGRP neighbor {neighbor} is up",
    ],
    "STP": [
        "STP topology change detected on {interface}",
        "STP port {interface} moved to blocking state",
        "STP root bridge changed on {interface}",
        "STP port {interface} moved to forwarding state",
    ],
    "HSRP": [
        "HSRP state change on {interface} to Active",
        "HSRP state change on {interface} to Standby",
        "HSRP group on {interface} is down",
    ],
    "ISIS": [
        "ISIS adjacency with {neighbor} is down",
        "ISIS LSP flood on {interface}",
        "ISIS neighbor {neighbor} state changed",
    ],
}

# severity weights — more warnings/errors than criticals to feel realistic
SEVERITY_WEIGHTS = {
    "CRITICAL": 0.10,
    "ERROR":    0.25,
    "WARNING":  0.40,
    "INFO":     0.25,
}


def pick_severity():
    r = random.random()
    cumulative = 0
    for severity, weight in SEVERITY_WEIGHTS.items():
        cumulative += weight
        if r <= cumulative:
            return severity
    return "INFO"


def generate_log_line(timestamp):
    protocol = random.choice(PROTOCOLS)
    interface = random.choice(INTERFACES)
    neighbor = random.choice(NEIGHBORS)
    severity = pick_severity()
    event_template = random.choice(EVENTS[protocol])
    event = event_template.format(neighbor=neighbor, interface=interface)

    # format: TIMESTAMP SEVERITY PROTOCOL: EVENT
    return f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} {severity} {protocol}: {event}"


def generate_logs(num_logs=200, output_path="AI-DIR/data/raw/sample_syslog.log"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    start_time = datetime.datetime.now() - datetime.timedelta(hours=6)
    logs = []

    for i in range(num_logs):
        # space logs out over 6 hours with small random jitter
        offset = datetime.timedelta(seconds=(i * 108) + random.randint(0, 30))
        timestamp = start_time + offset
        logs.append(generate_log_line(timestamp))

    with open(output_path, "w") as f:
        f.write("\n".join(logs) + "\n")

    print(f"generated {num_logs} log lines → {output_path}")
    return output_path


if __name__ == "__main__":
    generate_logs()