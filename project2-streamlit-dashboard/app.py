import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="India Climate Dashboard",
    page_icon="🌡️",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f1117;
    color: #e8e6e3;
}
h1, h2, h3 { font-family: 'DM Serif Display', serif; color: #f5f0e8; }
.stApp { background-color: #0d1b2a; }
.finding-card {
    background: #132338;
    border-left: 3px solid #e63946;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.88rem;
    line-height: 1.5;
    color: #c9c5be;
}
.sidebar-header { font-family: 'DM Serif Display', serif; font-size: 1.1rem; color: #f5f0e8; margin-bottom: 8px; }
[data-testid="stSidebar"] { background-color: #0d1b2a; border-right: 1px solid #1e2436; }
div[data-testid="metric-container"] {
    background: #161b27;
    border: 1px solid #254560;
    border-radius: 10px;
    padding: 14px;
}
.stDownloadButton > button {
    background: #e63946 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Load data with timeout ──────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    import os

    local_path = "ZonAnn.Ts+dSST.csv"

    # Try local file first
    if os.path.exists(local_path):
        df = pd.read_csv(local_path)
    else:
        # Fallback: try fetching from NASA
        url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv"
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            df = pd.read_csv(io.StringIO(response.text))
        except Exception as e:
            st.error(f"CSV not found locally and NASA fetch failed: {e}\n\nPlace ZonAnn.Ts+dSST.csv next to app.py and restart.")
            st.stop()

    df.columns = df.columns.str.strip()
    df = df[pd.to_numeric(df['Year'], errors='coerce').notna()].copy()
    df['Year'] = df['Year'].astype(int)
    return df

with st.spinner("Loading climate data…"):
    df = load_data()


# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌡️ India Climate\nTemperature Trend Explorer")
    st.markdown("---")

    st.markdown('<p class="sidebar-header">Year Range</p>', unsafe_allow_html=True)
    year_min, year_max = int(df['Year'].min()), int(df['Year'].max())
    year_range = st.slider(
        "Select range",
        min_value=year_min, max_value=year_max,
        value=(1950, year_max),
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown('<p class="sidebar-header">Decade Comparison</p>', unsafe_allow_html=True)
    decades_available = list(range((year_min // 10) * 10, (year_max // 10) * 10 + 1, 10))
    decade_a = st.selectbox("Decade A", options=decades_available, index=len(decades_available) - 3)
    decade_b = st.selectbox("Decade B", options=decades_available, index=len(decades_available) - 1)

    st.markdown("---")
    st.markdown('<p class="sidebar-header">Key Findings</p>', unsafe_allow_html=True)
    findings = [
        "India's latitude band has warmed consistently since 1980.",
        "Post-1980 anomalies are almost exclusively positive.",
        "The 10-year rolling average reveals a clear accelerating trend.",
        "The Arctic is warming 2–4× faster than the tropics.",
        "Global average is now ~1.2°C above the 1951–1980 baseline.",
    ]
    for f in findings:
        st.markdown(f'<div class="finding-card">{f}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Data: NASA GISS GISTEMP v4 · Baseline: 1951–1980")


# ─── Filter ──────────────────────────────────────────────────────────────────
filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()
india_col = 'EQU-24N'


# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("# India Temperature Trend Dashboard")
st.markdown(f"*Showing {year_range[0]}–{year_range[1]} · NASA GISS GISTEMP v4 · Baseline: 1951–1980*")
st.markdown("")

# ─── Metrics ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
latest_anomaly = round(filtered[india_col].iloc[-1], 2)
avg_anomaly    = round(filtered[india_col].mean(), 2)
max_anomaly    = round(filtered[india_col].max(), 2)
warmest_year   = int(filtered.loc[filtered[india_col].idxmax(), 'Year'])

col1.metric("Latest Anomaly",  f"{latest_anomaly:+.2f} °C", f"Year {filtered['Year'].iloc[-1]}")
col2.metric("Period Average",  f"{avg_anomaly:+.2f} °C")
col3.metric("Peak Anomaly",    f"{max_anomaly:+.2f} °C", f"{warmest_year}")
col4.metric("Years Analysed",  f"{year_range[1] - year_range[0] + 1}")
st.markdown("")

# ─── Main chart ──────────────────────────────────────────────────────────────
st.markdown("### India Region Trend (EQU–24°N)")

fig, ax = plt.subplots(figsize=(14, 5))
fig.patch.set_facecolor('#0f1117')
ax.set_facecolor('#0f1117')

ax.plot(filtered['Year'], filtered[india_col],
        color='#e8a030', linewidth=1, alpha=0.45, label='Annual anomaly')

rolling = filtered[india_col].rolling(window=10, center=True).mean()
ax.plot(filtered['Year'], rolling,
        color='#78c4a8', linewidth=2.5, label='10-year rolling average')

ax.axhline(0, color='#5a6075', linewidth=0.9, linestyle='--')
ax.fill_between(filtered['Year'], filtered[india_col], 0,
                where=filtered[india_col] > 0, alpha=0.12, color='#d64e1e')
ax.fill_between(filtered['Year'], filtered[india_col], 0,
                where=filtered[india_col] < 0, alpha=0.12, color='#3a9bcc')

# Decade shading
for dec, shade_col in [(decade_a, '#b8d4e8'), (decade_b, '#d4a870')]:
    ax.axvspan(dec, dec + 9, alpha=0.08, color=shade_col)
    ylim = ax.get_ylim()
    ax.text(dec + 4.5, ylim[0] + 0.03, f"{dec}s",
            ha='center', fontsize=8, color=shade_col, alpha=0.85)

ax.set_xlabel('Year', fontsize=11, color='#6a9ab8')
ax.set_ylabel('Temperature Anomaly (°C)', fontsize=11, color='#6a9ab8')
ax.tick_params(colors='#9ea3b0', labelsize=10)
for spine in ax.spines.values():
    spine.set_edgecolor('#254560')
ax.legend(fontsize=10, framealpha=0, labelcolor='#c9c5be')
ax.annotate('Baseline: 1951–1980 average', xy=(0.01, 0.03),
            xycoords='axes fraction', fontsize=8, color='#254560')
plt.tight_layout()

st.pyplot(fig)

buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=150, facecolor='#0d1b2a')
buf.seek(0)
st.download_button(
    label="⬇ Download Chart as PNG",
    data=buf,
    file_name=f"india_temp_trend_{year_range[0]}_{year_range[1]}.png",
    mime="image/png"
)
plt.close(fig)

# ─── Decade comparison ───────────────────────────────────────────────────────
st.markdown("")
st.markdown("### Decade Comparison")

def decade_stats(dec):
    d = df[(df['Year'] >= dec) & (df['Year'] <= dec + 9)][india_col]
    if d.empty:
        return None
    return {
        "mean":  round(d.mean(), 3),
        "max":   round(d.max(), 3),
        "min":   round(d.min(), 3),
        "trend": "Warming ↑" if d.iloc[-1] > d.iloc[0] else "Cooling ↓"
    }

col_a, col_b = st.columns(2)
stats_a = decade_stats(decade_a)
stats_b = decade_stats(decade_b)

with col_a:
    st.markdown(f"**{decade_a}s**")
    if stats_a:
        st.metric("Average anomaly", f"{stats_a['mean']:+.3f} °C")
        st.metric("Peak",   f"{stats_a['max']:+.3f} °C")
        st.metric("Trough", f"{stats_a['min']:+.3f} °C")
        st.caption(stats_a['trend'])

with col_b:
    st.markdown(f"**{decade_b}s**")
    if stats_b:
        delta = round(stats_b['mean'] - stats_a['mean'], 3) if stats_a else None
        st.metric("Average anomaly", f"{stats_b['mean']:+.3f} °C",
                  delta=f"{delta:+.3f} °C vs {decade_a}s" if delta is not None else None)
        st.metric("Peak",   f"{stats_b['max']:+.3f} °C")
        st.metric("Trough", f"{stats_b['min']:+.3f} °C")
        st.caption(stats_b['trend'])

st.markdown("")
st.caption("Built with Streamlit · Data: NASA GISS · github.com/khnatz/climate-data-portfolio")
