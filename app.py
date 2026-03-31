# ============================================================
# app.py — full earnings dashboard
# Run with: streamlit run app.py
# ============================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import yfinance as yf
from fetch     import get_company_info, get_quarterly_financials, get_eps_history, get_upcoming_earnings
from transform import add_growth, add_surprise, beat_streak

st.set_page_config(page_title="Earnings Dashboard", page_icon="📊", layout="wide")



# ── Sidebar ───────────────────────────────────────────────────
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

