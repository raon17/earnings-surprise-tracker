
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from fetch import get_company_info, get_quarterly_financials, get_eps_history, get_upcoming_earnings
from transform import add_growth, add_surprise, beat_streak

# sidebar
with st.sidebar:
    st.title("Earnings Dashboard")
    ticker = st.text_input("Ticker", value="NVDA").upper().strip()
    st.caption("Data: yfinance + FMP")
    st.divider()
    st.markdown("**Quick picks**")
    cols = st.columns(2)
    for i, t in enumerate(["AAPL","MSFT","NVDA","TSLA"]):
        if cols[i % 2].button(t, use_container_width=True):
            ticker = t

# Load data 
@st.cache_data(ttl=3600)
def load_all(t):
    info = get_company_info(t)
    fin_df = add_growth(get_quarterly_financials(t))
    eps_df = add_surprise(get_eps_history(t))
    cal_df = get_upcoming_earnings()
    return info, fin_df, eps_df, cal_df

info, fin_df, eps_df, cal_df = load_all(ticker)

if fin_df.empty:
    st.error(f"No data for **{ticker}**. Try AAPL, MSFT, NVDA or TSLA.")
    st.stop()

# Format large numbers
def fmt(n):
    if pd.isna(n):   return "—"
    if n >= 1e9:     return f"${n/1e9:.1f}B"
    if n >= 1e6:     return f"${n/1e6:.1f}M"
    return f"${n:.2f}"

# HEADER
st.title(f"{info['name']}  ({ticker})")
st.caption(f"{info['sector']}  | Market cap: {fmt(info['market_cap'])} ")
st.divider()

# KPI CARDS 

latest = fin_df.iloc[-1]
prev = fin_df.iloc[-2] if len(fin_df) > 1 else latest

def delta(col):
    val = latest.get(f"{col}_qoq")
    if pd.isna(val): return None
    return f"{val:+.1f}% QoQ"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue",    fmt(latest.get("revenue")),    delta("revenue"))
c2.metric("Net Income", fmt(latest.get("net_income")), delta("net_income"))
c3.metric("EPS",        f"${latest.get('eps', 0):.2f}", delta("eps"))

# Beat streak from eps_df
streak = beat_streak(eps_df) if not eps_df.empty else 0
c4.metric("Beat streak", f"{streak} qtrs", "in a row" if streak > 1 else "")

st.divider()

# DATE FILTER
min_date = fin_df["date"].min().date()
max_date = fin_df["date"].max().date()

col_p, col_s, col_e = st.columns([1,1,1])
with col_p:
    preset = st.selectbox("Range", ["All time", "Custom"], index=0)
with col_s:
    start_date = st.date_input("Start", value=min_date, min_value=min_date, max_value=max_date)
with col_e:
    end_date   = st.date_input("End",   value=max_date, min_value=min_date, max_value=max_date)
if preset == "All time":
    start_date, end_date = min_date, max_date

mask = (fin_df["date"] >= pd.Timestamp(start_date)) & (fin_df["date"] <= pd.Timestamp(end_date))
filtered = fin_df[mask].copy()

st.caption(f"Showing {len(filtered)} quarters  ·  {start_date.strftime('%b %Y')} → {end_date.strftime('%b %Y')}")
st.divider()

# Revenue chart with QoQ growth line
st.subheader("Revenue")

fig_rev = go.Figure()
fig_rev.add_trace(go.Bar(
    x    = filtered["date"],
    y    = filtered["revenue"],
    name = "Revenue",
    marker_color = "#378ADD",
    text = filtered["revenue"].apply(lambda x: fmt(x)),
    textposition = "outside",
))
# QoQ growth line on secondary axis
if "revenue_qoq" in filtered.columns:
    fig_rev.add_trace(go.Scatter(
        x    = filtered["date"],
        y    = filtered["revenue_qoq"],
        name = "QoQ growth %",
        mode = "lines+markers",
        line = dict(color="#EF9F27", width=2),
        yaxis = "y2",
    ))


