import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
FMP_KEY = os.getenv("FMP_KEY")
AV_KEY  = os.getenv("AV_KEY")


def get_upcoming_earnings():
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

    print(f"✓ Upcoming earnings: {len(data)} companies")
    return pd.DataFrame(data)
