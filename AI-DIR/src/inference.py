import pandas as pd
import os

# recommendations mapped to each protocol + state combination
# written the way a NOC engineer would actually respond

RECOMMENDATIONS = {
    "BGP": {
        "down": [
            "Check BGP neighbor reachability with ping/traceroute",
            "Verify BGP session config — AS numbers, peer IP",
            "Check if hold timer expired — review keepalive intervals",
            "Validate routing policies and prefix filters",
        ],
        "degraded": [
            "Monitor BGP session stability",
            "Review route flap history",
            "Check interface utilization on peering link",
        ],
        "changed": [
            "Review route table changes",
            "Check if planned maintenance is in progress",
            "Verify no unauthorized config changes",
        ],
    },
    "OSPF": {
        "down": [
            "Verify OSPF hello/dead intervals match on both sides",
            "Check interface MTU — mismatches break adjacency",
            "Confirm area IDs match between neighbors",
            "Check authentication config if enabled",
        ],
        "degraded": [
            "Review OSPF neighbor state history",
            "Check for duplicate router IDs",
            "Monitor CPU on routing device",
        ],
        "changed": [
            "Review LSA flooding — check for topology changes",
            "Verify no unauthorized OSPF config changes",
        ],
    },
    "EIGRP": {
        "down": [
            "Check EIGRP neighbor reachability",
            "Verify AS number matches on both sides",
            "Review K-values — must match for adjacency",
            "Check interface for hello packet drops",
        ],
        "degraded": [
            "Monitor stuck-in-active queries",
            "Check bandwidth and delay metrics",
        ],
        "changed": [
            "Review topology table changes",
            "Check for route summarization issues",
        ],
    },
    "STP": {
        "down": [
            "Identify root bridge and verify priority",
            "Check for port fast/BPDU guard events",
            "Look for physical loop in topology",
        ],
        "degraded": [
            "Monitor topology change notifications (TCN)",
            "Check MAC address table flapping",
        ],
        "changed": [
            "Verify root bridge has not changed unexpectedly",
            "Review recent switch port changes",
            "Check for new devices added to network",
        ],
    },
    "HSRP": {
        "down": [
            "Check active/standby router reachability",
            "Verify HSRP group number and VIP config",
            "Review hello and hold timers",
        ],
        "changed": [
            "Identify why failover occurred",
            "Check if primary router had an issue",
            "Verify preemption settings",
        ],
        "degraded": [
            "Monitor HSRP state flapping",
            "Check uplink of standby router",
        ],
    },
    "ISIS": {
        "down": [
            "Verify IS-IS net address and area config",
            "Check interface passive/active setting",
            "Review authentication if configured",
        ],
        "degraded": [
            "Monitor LSP flooding rate",
            "Check for adjacency flapping",
        ],
        "changed": [
            "Review recent topology changes",
            "Check for new IS-IS neighbors added",
        ],
    },
}

DEFAULT_RECOMMENDATION = ["Investigate the event manually — no specific playbook found"]


def get_recommendations(protocol, state):
    protocol_map = RECOMMENDATIONS.get(protocol, {})
    return protocol_map.get(state, DEFAULT_RECOMMENDATION)


def run_inference(input_path="AI-DIR/data/processed/feature_logs.csv",
                  output_path="AI-DIR/data/processed/alerts.csv"):

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"feature logs not found: {input_path}")

    df = pd.read_csv(input_path, parse_dates=["timestamp"])

    # only generate alerts for medium risk and above
    alerts = df[df["risk_level"].isin(["CRITICAL", "HIGH", "MEDIUM"])].copy()

    if alerts.empty:
        print("no alerts generated — all events are LOW risk")
        return alerts

    alerts["recommendations"] = alerts.apply(
        lambda row: " | ".join(get_recommendations(row["protocol"], row["state"])),
        axis=1
    )

    # order by incident score descending so highest risk is on top
    alerts = alerts.sort_values("incident_score", ascending=False).reset_index(drop=True)

    cols = [
        "timestamp", "severity", "protocol", "event",
        "interface", "neighbor", "state",
        "incident_score", "risk_level", "recommendations"
    ]
    alerts[cols].to_csv(output_path, index=False)

    print(f"generated {len(alerts)} alerts → {output_path}")
    print(f"\nrisk breakdown:")
    print(alerts["risk_level"].value_counts().to_string())
    return alerts


if __name__ == "__main__":
    run_inference()