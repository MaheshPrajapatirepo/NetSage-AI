"""
app.py — NetSage AI Streamlit Dashboard
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os

# ── Page Config ───────────────────────────────────────────────────
st.set_page_config(
    page_title = "NetSage AI",
    page_icon  = "📡",
    layout     = "wide"
)

# ── Load Data & Models ────────────────────────────────────────────
df         = pd.read_csv("data/network_incidents.csv")
model      = joblib.load("models/netsage_model.pkl")
scaler     = joblib.load("models/netsage_scaler.pkl")
categories = joblib.load("models/netsage_categories.pkl")

# ── Header ────────────────────────────────────────────────────────
st.title("📡 NetSage AI")
st.subheader("AI-Powered Network Incident Monitoring Dashboard")
st.divider()

# ── Tabs ──────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📊 Analytics Dashboard",
    "🤖 Prediction Engine",
    "🗃️ Raw Data"
])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — ANALYTICS DASHBOARD
# ══════════════════════════════════════════════════════════════════
with tab1:

    # ── Metrics ──────────────────────────────────────────────────
    critical_count = len(df[df["Severity"] == "Critical"])
    major_count    = len(df[df["Severity"] == "Major"])
    warning_count  = len(df[df["Severity"] == "Warning"])
    avg_cpu        = round(df["CPU_Usage"].mean(), 2)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔴 Critical Incidents", critical_count)
    col2.metric("🟠 Major Incidents",    major_count)
    col3.metric("🟡 Warning Incidents",  warning_count)
    col4.metric("💻 Avg CPU Usage",      f"{avg_cpu}%")

    st.divider()

    # ── Charts Row 1 ─────────────────────────────────────────────
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Incident Frequency")
        incident_counts = df["Incident_Type"].value_counts()
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        incident_counts.plot(kind="bar", ax=ax1, color='steelblue')
        ax1.set_xlabel("Incident Type")
        ax1.set_ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()

    with right_col:
        st.subheader("Severity Distribution")
        severity_counts = df["Severity"].value_counts()
        fig2, ax2 = plt.subplots(figsize=(6, 6))
        severity_counts.plot(
            kind="pie", autopct="%1.1f%%", ax=ax2,
            colors=['#ff4444', '#ff8800', '#ffcc00']
        )
        plt.ylabel("")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    st.divider()

    # ── Charts Row 2 ─────────────────────────────────────────────
    left_col2, right_col2 = st.columns(2)

    with left_col2:
        st.subheader("Device Incident Count")
        device_counts = df["Device"].value_counts()
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        device_counts.plot(kind="bar", ax=ax3, color='mediumpurple')
        ax3.set_xlabel("Device")
        ax3.set_ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close()

    with right_col2:
        st.subheader("Packet Loss Distribution")
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        ax4.hist(df["Packet_Loss_Percentage"], bins=20, color='tomato', edgecolor='white')
        ax4.set_xlabel("Packet Loss %")
        ax4.set_ylabel("Frequency")
        plt.tight_layout()
        st.pyplot(fig4)
        plt.close()

# ══════════════════════════════════════════════════════════════════
# TAB 2 — PREDICTION ENGINE
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("🤖 Critical Incident Prediction Engine")
    st.markdown("Enter network telemetry values to predict if an incident will become **Critical**.")
    st.divider()

    pred_col1, pred_col2, pred_col3 = st.columns(3)

    with pred_col1:
        cpu     = st.slider("CPU Usage (%)",    0,   100,  50)
        memory  = st.slider("Memory Usage (%)", 0,   100,  50)

    with pred_col2:
        packet_loss = st.slider("Packet Loss (%)", 0.0, 15.0, 2.0)
        device      = st.selectbox("Device",   categories["Device"])

    with pred_col3:
        location = st.selectbox("Location",     categories["Location"])
        incident = st.selectbox("Incident Type", categories["Incident_Type"])

    # ── Encode inputs ─────────────────────────────────────────────
    device_encoded   = categories["Device"].index(device)
    location_encoded = categories["Location"].index(location)
    incident_encoded = categories["Incident_Type"].index(incident)

    resource_stress = cpu + memory
    network_stress  = round(packet_loss * 10, 2)

    input_data = [[
        device_encoded,
        location_encoded,
        incident_encoded,
        cpu,
        memory,
        packet_loss,
        resource_stress,
        network_stress
    ]]

    input_scaled = scaler.transform(input_data)
    prediction   = model.predict(input_scaled)
    proba        = model.predict_proba(input_scaled)[0][1] * 100

    # ── Risk Score ────────────────────────────────────────────────
    risk_score = cpu * 0.3 + memory * 0.2 + packet_loss * 5

    if device   == "FW1-Perimeter"   : risk_score += 10
    elif device == "R1-Core"         : risk_score += 7

    if incident == "BGP Neighbor Down": risk_score += 25
    elif incident == "Interface Down" : risk_score += 20
    elif incident == "Route Flapping" : risk_score += 15

    if location == "Mumbai": risk_score += 5

    # ── Results ───────────────────────────────────────────────────
    st.divider()
    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric("Operational Risk Score", round(risk_score, 2))

    with result_col2:
        st.metric("Critical Probability", f"{proba:.1f}%")

    with result_col3:
        if prediction[0] == 1:
            st.error("🚨 Critical Incident Predicted")
        else:
            st.success("✅ Non-Critical Incident Predicted")

    # ── Telemetry Summary ─────────────────────────────────────────
    st.divider()
    st.subheader("📋 Telemetry Summary")
    summary = pd.DataFrame([{
        "Device"        : device,
        "Location"      : location,
        "Incident Type" : incident,
        "CPU Usage"     : f"{cpu}%",
        "Memory Usage"  : f"{memory}%",
        "Packet Loss"   : f"{packet_loss}%",
        "Resource Stress": resource_stress,
        "Network Stress" : network_stress,
        "Risk Score"     : round(risk_score, 2),
        "Prediction"     : "Critical" if prediction[0] == 1 else "Non-Critical"
    }])
    st.dataframe(summary, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3 — RAW DATA
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("🗃️ Network Incident Dataset")
    st.markdown(f"**Total Records:** {len(df)} | **Columns:** {len(df.columns)}")
    st.dataframe(df, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────
st.divider()
st.caption("Built by Mahesh Prajapati · NetSage AI · Powered by scikit-learn + Streamlit")