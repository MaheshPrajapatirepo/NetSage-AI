import streamlit as st
import pandas as pd
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "src"))

from collector import generate_logs
from parser    import parse_logs
from features  import engineer_features
from inference import run_inference
from pattern import run_pattern_detection

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
RAW_LOG     = os.path.join(BASE_DIR, "AI-DIR/data/raw/sample_syslog.log")
PARSED_CSV  = os.path.join(BASE_DIR, "AI-DIR/data/processed/parsed_logs.csv")
FEATURE_CSV = os.path.join(BASE_DIR, "AI-DIR/data/processed/feature_logs.csv")
ALERTS_CSV  = os.path.join(BASE_DIR, "AI-DIR/data/processed/alerts.csv")

# ── page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="NetSage-AI",
    page_icon="🛰️",
    layout="wide"
)

# ── sidebar ──────────────────────────────────────────────────
st.sidebar.title("🛰️ NetSage-AI")
st.sidebar.markdown("AI-powered NOC assistant")
st.sidebar.divider()

if st.sidebar.button("▶ Run Pipeline", use_container_width=True):
    with st.spinner("running pipeline..."):
        generate_logs(output_path=RAW_LOG)
        parse_logs(input_path=RAW_LOG, output_path=PARSED_CSV)
        engineer_features(input_path=PARSED_CSV, output_path=FEATURE_CSV)
        run_inference(input_path=FEATURE_CSV, output_path=ALERTS_CSV)
    st.sidebar.success("pipeline complete")

st.sidebar.divider()
page = st.sidebar.radio(
    "view",
    ["Overview", "Alerts", "Patterns", "Raw Logs"]
)


# ── helpers ──────────────────────────────────────────────────
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


RISK_COLOR = {
    "CRITICAL": "🔴",
    "HIGH":     "🟠",
    "MEDIUM":   "🟡",
    "LOW":      "🟢",
}


# ── overview ─────────────────────────────────────────────────
if page == "Overview":
    st.title("Network Operations Overview")

    alerts_df  = load_csv(ALERTS_CSV)
    feature_df = load_csv(FEATURE_CSV)

    if alerts_df is None or feature_df is None:
        st.info("No data yet — click **Run Pipeline** in the sidebar.")
    else:
        # top metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Events",    len(feature_df))
        col2.metric("Total Alerts",    len(alerts_df))
        col3.metric("Critical",        len(alerts_df[alerts_df["risk_level"] == "CRITICAL"]))
        col4.metric("High",            len(alerts_df[alerts_df["risk_level"] == "HIGH"]))

        st.divider()

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Risk breakdown")
            risk_counts = feature_df["risk_level"].value_counts()
            st.bar_chart(risk_counts)

        with col_b:
            st.subheader("Events by protocol")
            proto_counts = feature_df["protocol"].value_counts()
            st.bar_chart(proto_counts)

        st.divider()
        st.subheader("Incident score over time")
        feature_df["timestamp"] = pd.to_datetime(feature_df["timestamp"])
        chart_df = feature_df.set_index("timestamp")[["incident_score"]]
        st.line_chart(chart_df)


# ── alerts ───────────────────────────────────────────────────
elif page == "Alerts":
    st.title("Active Alerts")

    alerts_df = load_csv(ALERTS_CSV)

    if alerts_df is None:
        st.info("No alerts yet — click **Run Pipeline** in the sidebar.")
    else:
        # filter controls
        col1, col2 = st.columns(2)
        with col1:
            risk_filter = st.multiselect(
                "Filter by risk level",
                ["CRITICAL", "HIGH", "MEDIUM"],
                default=["CRITICAL", "HIGH", "MEDIUM"]
            )
        with col2:
            proto_filter = st.multiselect(
                "Filter by protocol",
                alerts_df["protocol"].unique().tolist(),
                default=alerts_df["protocol"].unique().tolist()
            )

        filtered = alerts_df[
            alerts_df["risk_level"].isin(risk_filter) &
            alerts_df["protocol"].isin(proto_filter)
        ]

        st.markdown(f"showing **{len(filtered)}** alerts")
        st.divider()

        for _, row in filtered.iterrows():
            icon = RISK_COLOR.get(row["risk_level"], "⚪")
            with st.expander(f"{icon} [{row['risk_level']}] {row['protocol']} — {row['event']}"):
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**Timestamp**  \n{row['timestamp']}")
                c2.markdown(f"**Severity**  \n{row['severity']}")
                c3.markdown(f"**Score**  \n{row['incident_score']}")

                if pd.notna(row.get("interface")):
                    st.markdown(f"**Interface:** `{row['interface']}`")
                if pd.notna(row.get("neighbor")):
                    st.markdown(f"**Neighbor:** `{row['neighbor']}`")

                st.markdown("**Recommendations:**")
                for rec in str(row["recommendations"]).split(" | "):
                    st.markdown(f"- {rec}")


# ── patterns ─────────────────────────────────────────────────
elif page == "Patterns":
    st.title("Pattern Detection")

    feature_df = load_csv(FEATURE_CSV)

    if feature_df is None:
        st.info("No data yet — click **Run Pipeline** in the sidebar.")
    else:
        feature_df["timestamp"] = pd.to_datetime(feature_df["timestamp"])

        patterns = run_pattern_detection(
            input_path=FEATURE_CSV,
            output_path=os.path.join(BASE_DIR, "AI-DIR/data/processed/patterns.csv")
        )

        st.subheader("Protocol hotspots")
        st.dataframe(patterns["hotspots"], use_container_width=True)

        st.divider()
        st.subheader("Repeated incidents")
        if patterns["repeated"].empty:
            st.success("No repeated incidents found")
        else:
            st.dataframe(patterns["repeated"], use_container_width=True)

        st.divider()
        st.subheader("Hourly spikes")
        if not patterns["spikes"].empty:
            st.bar_chart(patterns["spikes"].set_index("hour")["event_count"])

        st.divider()
        st.subheader("Flapping neighbors")
        if patterns["flapping"].empty:
            st.success("No flapping neighbors detected")
        else:
            st.dataframe(patterns["flapping"], use_container_width=True)


# ── raw logs ─────────────────────────────────────────────────
elif page == "Raw Logs":
    st.title("Raw Logs")

    if not os.path.exists(RAW_LOG):
        st.info("No logs yet — click **Run Pipeline** in the sidebar.")
    else:
        with open(RAW_LOG, "r") as f:
            lines = f.readlines()

        st.markdown(f"**{len(lines)} log lines**")
        search = st.text_input("Search logs", placeholder="e.g. BGP, CRITICAL, 10.0.0.1")

        if search:
            lines = [l for l in lines if search.lower() in l.lower()]
            st.markdown(f"found **{len(lines)}** matches")

        st.code("".join(lines[-100:]), language="bash")