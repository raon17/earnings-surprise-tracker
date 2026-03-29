import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
FMP_KEY = os.getenv("FMP_KEY")

def get_company_info(ticker):
    """Basic company info — name, sector, market cap."""
    try:
        info = yf.Ticker(ticker).info
        return {
            "name":       info.get("longName", ticker),
            "sector":     info.get("sector", "—"),
            "market_cap": info.get("marketCap", None),
        }
    except:
        return {"name": ticker, "sector": "—", "market_cap": None}

