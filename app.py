
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
