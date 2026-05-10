import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="NetSage AI",
    layout="wide",
    page_icon="📡"
)

# --------------------------------
# LOAD DATA + MODEL
# --------------------------------

df = pd.read_csv("data/network_incidents.csv")

model = joblib.load("models/decision_tree_model.pkl")

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("NetSage AI")

st.sidebar.markdown("""
AI-Powered NOC Monitoring System

Features:
- Incident Analytics
- ML Prediction
- Operational Risk Analysis
- Network Telemetry Insights
""")

# --------------------------------
# HEADER
# --------------------------------

st.title("NetSage AI")
st.subheader("AI-Powered Network Incident Monitoring Dashboard")

# --------------------------------
# METRICS
# --------------------------------

critical_count = len(df[df["Severity"] == "Critical"])

major_count = len(df[df["Severity"] == "Major"])

warning_count = len(df[df["Severity"] == "Warning"])

avg_cpu = round(df["CPU_Usage"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Critical Incidents", critical_count)

col2.metric("Major Incidents", major_count)

col3.metric("Warning Incidents", warning_count)

col4.metric("Average CPU Usage", f"{avg_cpu}%")

st.divider()

# --------------------------------
# CHART SECTION
# --------------------------------

left_col, right_col = st.columns(2)

# INCIDENT FREQUENCY
with left_col:

    st.subheader("Incident Frequency")

    incident_counts = df["Incident_Type"].value_counts()

    fig1, ax1 = plt.subplots(figsize=(8, 5))

    incident_counts.plot(
        kind="bar",
        ax=ax1
    )

    plt.xticks(rotation=45)

    st.pyplot(fig1)

# SEVERITY DISTRIBUTION
with right_col:

    st.subheader("Severity Distribution")

    severity_counts = df["Severity"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(6, 6))

    severity_counts.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax2
    )

    plt.ylabel("")

    st.pyplot(fig2)

st.divider()

# --------------------------------
# DEVICE ANALYTICS
# --------------------------------

left_col2, right_col2 = st.columns(2)

with left_col2:

    st.subheader("Device Incident Count")

    device_counts = df["Device"].value_counts()

    fig3, ax3 = plt.subplots(figsize=(8, 5))

    device_counts.plot(
        kind="bar",
        ax=ax3
    )

    plt.xticks(rotation=45)

    st.pyplot(fig3)

with right_col2:

    st.subheader("Packet Loss Distribution")

    fig4, ax4 = plt.subplots(figsize=(8, 5))

    ax4.hist(df["Packet_Loss_Percentage"])

    st.pyplot(fig4)

st.divider()

# --------------------------------
# PREDICTION SECTION
# --------------------------------

st.header("Critical Incident Prediction Engine")

pred_col1, pred_col2, pred_col3 = st.columns(3)

with pred_col1:

    cpu = st.slider(
        "CPU Usage",
        0,
        100,
        50
    )

    memory = st.slider(
        "Memory Usage",
        0,
        100,
        50
    )

with pred_col2:

    packet_loss = st.slider(
        "Packet Loss %",
        0.0,
        15.0,
        2.0
    )

    device = st.selectbox(
        "Device",
        df["Device"].unique()
    )

with pred_col3:

    location = st.selectbox(
        "Location",
        df["Location"].unique()
    )

    incident = st.selectbox(
        "Incident Type",
        df["Incident_Type"].unique()
    )

# --------------------------------
# FEATURE ENGINEERING
# --------------------------------

resource_stress = cpu + memory

network_stress = packet_loss * 10

# ENCODING
device_encoded = list(df["Device"].unique()).index(device)

location_encoded = list(df["Location"].unique()).index(location)

incident_encoded = list(df["Incident_Type"].unique()).index(incident)

# PREDICTION DATA
prediction_data = [[
    device_encoded,
    location_encoded,
    incident_encoded,
    cpu,
    memory,
    packet_loss,
    resource_stress,
    network_stress
]]

prediction = model.predict(prediction_data)

# --------------------------------
# RISK SCORE
# --------------------------------

risk_score = (
    cpu * 0.3 +
    memory * 0.2 +
    packet_loss * 5
)

# DEVICE IMPACT
if device == "FW1-Perimeter":
    risk_score += 10

elif device == "R1-Core":
    risk_score += 7

# INCIDENT IMPACT
if incident == "BGP Neighbor Down":
    risk_score += 25

elif incident == "Interface Down":
    risk_score += 20

elif incident == "Route Flapping":
    risk_score += 15

# LOCATION IMPACT
if location == "Mumbai":
    risk_score += 5

# --------------------------------
# RESULTS
# --------------------------------

st.divider()

result_col1, result_col2 = st.columns(2)

with result_col1:

    st.metric(
        "Operational Risk Score",
        round(risk_score, 2)
    )

with result_col2:

    if prediction[0] == 1:

        st.error(
            "Critical Incident Predicted"
        )

    else:

        st.success(
            "Non-Critical Incident Predicted"
        )

# --------------------------------
# RAW DATA
# --------------------------------

st.divider()

with st.expander("View Raw Dataset"):

    st.dataframe(df)