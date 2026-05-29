# Project 1: India Temperature Trend Analysis

An analysis of 145 years of NASA surface temperature data, exploring global warming
patterns with a focus on India's latitude band and regional climate differences.

---

## Dataset

**Source:** NASA GISS Surface Temperature Analysis (GISTEMP v4)  
**Link:** https://data.giss.nasa.gov/gistemp/  
**File:** `ZonAnn.Ts+dSST.csv`  
**Coverage:** 1880–2025 | 15 latitude zones | Annual averages  
**Anomalies measured against:** 1951–1980 baseline average

---

## Visualisations

### Plot 1 — Global Temperature Anomaly (1880–2025)
Bar chart showing annual global temperature anomalies. Blue bars indicate
cooler-than-baseline years, red bars indicate warmer years. The shift from
predominantly blue to predominantly red post-1980 is clearly visible.

### Plot 2 — India Region Temperature Trend
Line chart of the equatorial–24°N latitude band (which covers India) with a
10-year rolling average overlay. Warming accelerates sharply and consistently
from around 1980 onwards.

### Plot 3 — Heatmap Across All Latitude Bands
A full spatial view of temperature anomalies across 8 latitude zones from
Arctic to Antarctic. Key observations:
- **Arctic amplification** is clearly visible — the poles warm 2–4x faster
- **India/Tropics** show steady post-1980 warming
- **Antarctica** shows more variable patterns due to Southern Ocean dynamics

---

## Key Findings

1. Global average temperature has risen by approximately **1.2°C** above the
   1951–1980 baseline by 2025
2. The warming signal in India's latitude band becomes consistent and
   accelerating from **1980 onwards**
3. The Arctic is warming significantly faster than the tropics —
   a well-documented phenomenon called **Arctic Amplification**
4. Pre-1980 temperature anomalies fluctuate around zero with no clear trend;
   post-1980 anomalies are almost exclusively positive

---

## Tools Used

- Python 3
- pandas — data loading and cleaning
- matplotlib — visualisation
- seaborn — heatmap

---

## Part of

[climate-data-portfolio](https://github.com/khnatz/climate-data-portfolio) —
a portfolio of climate data science projects built toward research at
IISc CAOS and ISRO.