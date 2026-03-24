# fetch.py
import requests
import pandas as pd
import time

FMP_KEY = ""
AV_KEY  = ""        

# Get upcoming earnings dates 
def fetch_upcoming_earnings():
    url = f"https://financialmodelingprep.com/api/v3/earning_calendar?apikey={FMP_KEY}"
    response = requests.get(url)          
    data = response.json()                
    df = pd.DataFrame(data)              
    return df

# Get historical EPS surprises for ONE company 
def fetch_eps_history(ticker):
    url = f"https://financialmodelingprep.com/api/v3/earnings-surprises/{ticker}?apikey={FMP_KEY}"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    return df

#  FUNCTION 3: Get post-earnings price reaction 
def fetch_price_after_earnings(ticker):
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY&symbol={ticker}"
        f"&outputsize=compact&apikey={AV_KEY}"
    )
    response = requests.get(url)
    data = response.json()

    prices = data.get("Time Series (Daily)", {})
    df = pd.DataFrame(prices).T          
    df.index = pd.to_datetime(df.index)  
    df.columns = ["open", "high", "low", "close", "volume"]
    df = df.astype(float)                
    return df