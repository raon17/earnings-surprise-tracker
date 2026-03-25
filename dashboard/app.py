# dashboard/app.py
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
sys.path.append("..")
from fetch import fetch_upcoming_earnings, fetch_eps_history, fetch_price_after_earnings
from transform import calc_eps_surprise, calc_beat_streak, calc_price_reaction

# Page config
st.set_page_config(
    page_title="Earnings Tracker",
    layout="wide"
)
st.title("Stock Earnings Calendar & Surprise Tracker")

#  sidebar: company search
st.sidebar.header("Company Search")
ticker = st.sidebar.text_input("Enter ticker (e.g. AAPL)", value="AAPL").upper()

# tab layout
tab1, tab2, tab3 = st.tabs(["Upcoming Calendar", "Surprise Chart", "Company Deep-Dive"])

# tab 1: upcoming earnings calendar
with tab1:
    st.subheader("Upcoming earnings this week")

    @st.cache_data(ttl=3600)          # ttl=3600: cache for 1 hour
    def get_upcoming():
        return fetch_upcoming_earnings()

    upcoming = get_upcoming()

    if not upcoming.empty:
        st.dataframe(
            upcoming[["symbol", "date", "epsEstimated", "revenueEstimated"]].head(30),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No upcoming earnings data found. Check API key")