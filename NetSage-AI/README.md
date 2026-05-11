# NetSage AI

AI-Powered Network Incident Monitoring & Prediction System

---

# Project Overview

I built NetSage AI to combine my networking background with the Data Science and Machine Learning concepts I’ve been learning.

The idea behind this project was simple:

simulate how a small Network Operations Center (NOC) monitoring system could collect telemetry, analyze incidents, and predict whether a network issue may become critical.

The project generates simulated network incident data from routers, switches, and firewalls, then processes the data through:

* Exploratory Data Analysis (EDA)
* Feature Engineering
* Machine Learning
* Interactive Dashboard Visualization

The dashboard allows users to:

* monitor incident trends
* analyze packet loss and device behavior
* view operational risk scores
* predict critical incidents using ML

This project helped me understand how networking concepts and Machine Learning can work together in a practical way.

---

# Features

## Network Telemetry Simulation

Generates synthetic but realistic:

* CPU utilization
* Memory utilization
* Packet loss
* Device incidents
* Network severity levels

---

## Exploratory Data Analysis (EDA)

Visualizes:

* Incident frequency
* Severity distribution
* Device analytics
* Packet loss patterns

---

## Machine Learning Prediction

Predicts:

* Critical network incidents

Using:

* Random Forest Classifier
* Feature engineering
* Risk-based telemetry correlation

---

## Operational Risk Scoring

Calculates:

* Real-time operational risk score

Based on:

* CPU usage
* Memory usage
* Packet loss
* Device criticality
* Incident type
* Location impact

---

## Interactive Streamlit Dashboard

Provides:

* Real-time visualization
* Incident analytics
* Prediction engine
* Risk monitoring interface

---

# Tech Stack

| Category            | Technology   |
| ------------------- | ------------ |
| Language            | Python       |
| Data Processing     | Pandas       |
| Visualization       | Matplotlib   |
| Machine Learning    | Scikit-learn |
| Dashboard           | Streamlit    |
| Model Serialization | Joblib       |
| Version Control     | Git & GitHub |

---

# Project Architecture

```text
Network Telemetry Generator
            ↓
Generated CSV Dataset
            ↓
Exploratory Data Analysis
            ↓
Feature Engineering
            ↓
Random Forest Model Training
            ↓
Saved ML Model (.pkl)
            ↓
Streamlit Dashboard
            ↓
Critical Incident Prediction
```

---

# Folder Structure

```text
NetSage-AI/
│
├── data/
│   └── network_incidents.csv
│
├── models/
│   └── decision_tree_model.pkl
│
├── notebooks/
│   ├── eda.ipynb
│   └── ml_model.ipynb
│
├── scripts/
│   └── log_generator.py
│
├── visuals/
│
├── app.py
├── requirements.txt
├── setup.py
├── template.py
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <your-repository-link>
cd NetSage-AI
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Generate Network Dataset

```bash
python3 scripts/log_generator.py
```

---

# Run Streamlit Dashboard

```bash
streamlit run app.py
```

---

# Machine Learning Workflow

## Input Features

* Device
* Location
* Incident Type
* CPU Usage
* Memory Usage
* Packet Loss Percentage
* Resource Stress
* Network Stress

---

## Target Prediction

* Critical Incident

---

## Model Used

Random Forest Classifier

---

## Feature Engineering

Additional engineered features:

```python
Resource_Stress = CPU + Memory

Network_Stress = PacketLoss * 10
```

---

# Dashboard Capabilities

The dashboard includes:

* Incident analytics
* Severity monitoring
* Device-wise analysis
* Packet loss distribution
* Interactive incident prediction
* Operational risk score visualization

---

# Future Improvements

Potential future enhancements:

* SNMP trap simulation
* Syslog integration
* Real-time streaming telemetry
* Prometheus/Grafana integration
* Kafka-based event pipelines
* Deep Learning anomaly detection
* Multi-vendor network support
* Real Cisco syslog ingestion

---

# Use Case

As someone working in networking, I wanted to build something that connects traditional NOC monitoring concepts with Data Science workflows.

This project demonstrates how telemetry-like network data can be:

* generated
* analyzed
* visualized
* used for ML-based predictions

The goal was not to build a production-grade enterprise monitoring system, but to create a realistic learning project that combines:

* networking
* Python automation
* analytics
* machine learning
* dashboard development

---

# Screenshots

Add screenshots inside:

```text
visuals/
```

Recommended screenshots:

* Main dashboard
* Prediction engine
* Risk score section
* Analytics charts

---

# Author

Mahi

CCNA Certified | Network Engineer | Learning Data Science & AI
