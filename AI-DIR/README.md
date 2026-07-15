# NetSage-AI

AI-powered NOC assistant — analyzes network logs, scores risk, and recommends actions.

---

## Setup

```bash
git clone https://github.com/yourusername/NetSage-AI.git
cd NetSage-AI/AI-DIR
pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

Options:
```bash
python main.py --skip-collect    # use existing logs
python main.py --skip-train      # skip ML training
python main.py --infer-only      # alerts only
```

---

## Structure

AI-DIR/
├── src/
│   ├── collector.py
│   ├── parser.py
│   ├── features.py
│   ├── inference.py
│   └── train.py
├── data/
│   ├── raw/
│   └── processed/
└── main.py

---

## Roadmap

- [x] Log collection
- [x] Parsing
- [x] Risk scoring
- [x] Alerts + recommendations
- [x] ML training
- [ ] Pattern detection
- [ ] Streamlit dashboard
- [ ] Docker ingestion
- [ ] Streamlit Cloud deployment