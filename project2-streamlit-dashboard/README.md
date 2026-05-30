# Project 2 — Streamlit Interactive Climate Dashboard

An interactive web dashboard for exploring India's temperature anomaly trends, built on top of the NASA GISS GISTEMP v4 dataset analysed in [Project 1](../project1-india-temperature/).

---

## Live Features

| Feature | Description |
|---|---|
| **Year range slider** | Filter all charts and metrics to any period from 1880–2025 |
| **India trend chart** | Annual anomaly + 10-year rolling average with above/below-zero fill |
| **Decade comparison** | Pick any two decades and compare average, peak, trough, and warming direction |
| **Download PNG** | Export the current filtered chart at 150 dpi |
| **Key findings sidebar** | Persistent summary of the five headline climate insights |

---

## Dataset

- **Source:** NASA GISS Surface Temperature Analysis (GISTEMP v4)
- **File:** `ZonAnn.Ts+dSST.csv`
- **Coverage:** 1880–2025
- **Region shown:** EQU–24°N (India's latitude band)
- **Anomalies measured against:** 1951–1980 baseline average

The CSV is bundled locally so the app loads instantly without a network request.

---

## How to Run

```bash
# Install dependencies
pip install streamlit pandas matplotlib requests

# Run
cd project2-streamlit-dashboard
streamlit run app.py
```

If `streamlit` isn't recognised, use:
```bash
python -m streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## Folder Structure

```
project2-streamlit-dashboard/
├── app.py                  # Streamlit dashboard
├── ZonAnn.Ts+dSST.csv      # NASA GISS dataset (local copy)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Key Findings

1. India's latitude band (EQU–24°N) has warmed consistently since **1980**
2. Post-1980 anomalies are almost exclusively **positive**
3. The 10-year rolling average shows a clear **accelerating trend**
4. The Arctic is warming **2–4× faster** than the tropics (Arctic Amplification)
5. Global average is now **~1.2°C** above the 1951–1980 baseline

---

## Tools Used

- Python 3, pandas, matplotlib, Streamlit
- VS Code
- Git + GitHub

---

