# 📡 NetSage AI

An AI-powered Network Operations Center (NOC) monitoring and incident prediction system built with Python, scikit-learn, and Streamlit.

---

## 📸 App Screenshots

![Dashboard](visuals/dashboard_overview.png)
![Prediction Engine](visuals/prediction_engine.png)

---

## 🎯 Project Goals

| Goal | Type | Model |
|------|------|-------|
| Predict critical network incidents | Classification | Random Forest |
| Monitor network telemetry in real-time | Dashboard | Streamlit |
| Score operational risk | Rule-based scoring | Custom logic |

---

## 🗂️ Project Structure

```
NetSage-AI/
│
├── app.py                  ← Streamlit dashboard
├── main.py                 ← Full pipeline runner
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── data_generator.py   ← Generates synthetic network data
│   ├── data_loader.py      ← Load, encode, prepare features
│   ├── train.py            ← Cross validation + train model
│   ├── evaluate.py         ← Metrics + confusion matrix + feature importance
│   └── export_model.py     ← Save & load .pkl files
│
├── data/
│   └── network_incidents.csv   ← Generated dataset
│
├── models/                 ← Saved after running main.py
│   ├── netsage_model.pkl
│   ├── netsage_scaler.pkl
│   └── netsage_categories.pkl
│
├── outputs/                ← Saved plots
│   ├── confusion_matrix.png
│   └── feature_importance.png
│
└── visuals/                ← App screenshots
    ├── dashboard_overview.png
    └── prediction_engine.png
```

---

## ⚙️ Setup & Installation

### 1. Clone the project
```bash
git clone https://github.com/MaheshPrajapatirepo/NetSage-AI.git
cd NetSage-AI
```

### 2. Activate environment
```bash
conda activate ml_env
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### Step 1 — Run full pipeline (generates data + trains model)
```bash
python main.py
```

### Step 2 — Launch Streamlit app
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

---

## 🧠 Model & Results

### Overfitting Fix
The original model was overfitting due to unrestricted tree depth. Fixed by:

| Parameter | Before | After |
|-----------|--------|-------|
| `max_depth` | None | 8 |
| `min_samples_leaf` | 1 | 5 |
| `min_samples_split` | 2 | 10 |
| `max_features` | None | `sqrt` |

### Classification Results

| Model | Accuracy | ROC-AUC |
|-------|----------|---------|
| Logistic Regression | — | — |
| Decision Tree | — | — |
| **Random Forest** ✅ | **—** | **—** |

> 📌 Fill in after running `main.py`

---

## 📡 Simulated Network Telemetry

| Feature | Description |
|---------|-------------|
| `Device` | Router / Switch / Firewall |
| `Location` | Mumbai, Delhi, Pune, Bangalore |
| `Incident_Type` | BGP Down, Interface Down, Packet Loss, etc. |
| `CPU_Usage` | 20–100% |
| `Memory_Usage` | 30–95% |
| `Packet_Loss_Percentage` | 0–15% |
| `Resource_Stress` | CPU + Memory |
| `Network_Stress` | Packet Loss × 10 |

---

## 🖥️ Streamlit App Features

### Tab 1 — 📊 Analytics Dashboard
- Critical / Major / Warning incident counts
- Incident frequency bar chart
- Severity distribution pie chart
- Device incident count
- Packet loss histogram

### Tab 2 — 🤖 Prediction Engine
- Interactive sliders for telemetry input
- Critical incident prediction
- Operational risk score
- Telemetry summary table

### Tab 3 — 🗃️ Raw Data
- Full dataset viewer

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Core language |
| pandas | Data manipulation |
| scikit-learn | ML model |
| Streamlit | Dashboard |
| seaborn / matplotlib | Visualizations |
| joblib | Model serialization |

---

## 👤 Author

**Mahesh Prajapati**
🔗 [GitHub](https://github.com/MaheshPrajapatirepo)

---

## 📝 Notes

- Data is synthetically generated using `src/data_generator.py`
- Run `main.py` before `app.py` to generate models
- All outputs saved to `outputs/` folder automatically