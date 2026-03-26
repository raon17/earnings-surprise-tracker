import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import yfinance as yf

load_dotenv()
FMP_KEY = os.getenv("FMP_KEY")
AV_KEY  = os.getenv("AV_KEY")

# https://financialmodelingprep.com/developer/docs/earnings-calendar-free-api/

# Function to get upcoming earnings for the next 2 weeks
def get_upcoming_earnings():
    ''' {
    "symbol": "BABA",
    "date": "2026-03-19",
    "epsActual": 1.01,
    "epsEstimated": 1.65,
    "revenueActual": 40159119047,
    "revenueEstimated": 36042338708,
    "lastUpdated": "2026-03-26"
    },'''

    today    = datetime.today().strftime("%Y-%m-%d")
    in2weeks = (datetime.today() + timedelta(days=14)).strftime("%Y-%m-%d")

    r    = requests.get(
        "https://financialmodelingprep.com/stable/earnings-calendar",
        params={"from": today, "to": in2weeks, "apikey": FMP_KEY},
        timeout=10
    )
    data = r.json()

    if isinstance(data, dict):
        print("FMP error:", data)
        return pd.DataFrame()

    print(f"Upcoming earnings: {len(data)} companies")
    return pd.DataFrame(data)

# Function to get historical EPS data for a given ticker
def get_eps_history(ticker):
 
    stock = yf.Ticker(ticker)
    df    = stock.earnings_history
 
    if df is None or df.empty:
        print(f"  No EPS history found for {ticker}")
        return pd.DataFrame()
 
    df = df.rename(columns={
        "epsActual":       "eps",             
        "epsEstimate":     "epsEstimated",    
        "surprisePercent": "surprise_pct_raw" 
    })
 
    keep = [c for c in ["eps", "epsEstimated", "surprise_pct_raw"] if c in df.columns]
    df   = df[keep]
 
    df.index = pd.to_datetime(df.index)
    df.index.name = "date"
    df = df.reset_index()
 
    df = df.sort_values("date", ascending=False).reset_index(drop=True)
 
    print(f"EPS history for {ticker}: {len(df)} quarters found")
    return df
 

# Function to get historical stock price data for a given ticker
def get_stock_price(ticker):
 
    r = requests.get(
        "https://www.alphavantage.co/query",
        params = {
            "function":   "TIME_SERIES_DAILY",
            "symbol":     ticker,               
            "outputsize": "compact",            
            "apikey":     AV_KEY,
        },
        timeout = 10
    )
    data = r.json()
 
    prices = data.get("Time Series (Daily)")
    if not prices:
        print(f"Alpha Vantage error ({ticker}):", data)
        return pd.DataFrame()
 
    df = pd.DataFrame(prices).T # Transpose so dates become rows and ohlcv become columns
    df.index = pd.to_datetime(df.index)

    df.columns = ["open", "high", "low", "close", "volume"]  # Convert Alpha Vantage ugly column names to pretty
    df = df.astype(float)# Convert everything from strings to numbers
 
    df = df.sort_index(ascending=False)
 
    print(f" Price data for {ticker}: {len(df)} days found")
    return df
 
if __name__ == "__main__":
    print("\n ***** Testing ***** \n")
 
    print("** 1.Upcoming earnings **")
    df1 = get_upcoming_earnings()
    print(df1.head(5) if not df1.empty else "EMPTY —check FMP_KEY")
 
    print("\n** 2.EPS history **")
    df2 = get_eps_history("NVDA")
    print(df2.head(3) if not df2.empty else "EMPTY — check FMP_KEY")
 
    print("\n** 3.Stock price **")
    df3 = get_stock_price("NVDA")
    print(df3.head(3) if not df3.empty else "EMPTY — check AV_KEY")