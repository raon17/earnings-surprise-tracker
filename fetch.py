import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
FMP_KEY = os.getenv("FMP_KEY")

def get_company_info(ticker):
    """Basic company info name, sector, market cap from yfinance."""
    try:
        info = yf.Ticker(ticker).info
        return {
            "name":       info.get("longName", ticker),
            "sector":     info.get("sector", "—"),
            "market_cap": info.get("marketCap", None),
        }
    except:
        return {"name": ticker, "sector": "—", "market_cap": None}


def get_quarterly_financials(ticker):
    """Pulls quarterly income statement from yfinance and extracts Revenue, Net Income, Diluted EPS"""
    stock = yf.Ticker(ticker)
    df    = stock.quarterly_income_stmt

    if df is None or df.empty:
        print(f"No quarterly financials for {ticker}")
        return pd.DataFrame()

    rows = {
        "Total Revenue":  "revenue",
        "Net Income":     "net_income",
        "Diluted EPS":    "eps",
    }

    result = {}
    for yf_name, our_name in rows.items():
        if yf_name in df.index:
            result[our_name] = df.loc[yf_name]

    if not result:
        print(f"Could not find financials for {ticker}")
        return pd.DataFrame()

    out = pd.DataFrame(result)
    out.index = pd.to_datetime(out.index)
    out = out.sort_index(ascending=True)   
    out.index.name = "date"
    out = out.reset_index()

    print(f"Quarterly financials for {ticker}: {len(out)} quarters")
    return out
