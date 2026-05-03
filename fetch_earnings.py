import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost:5432/earnings")

TICKERS = ["AMD", "MSFT", "NVDA", "TSLA"]


def fetch_earnings(ticker):
    stock = yf.Ticker(ticker)
    df = stock.earnings_dates

    if df is None:
        return None

    df = df.reset_index()
    df["ticker"] = ticker

    return df[["ticker", "Earnings Date", "EPS Estimate", "Reported EPS"]]

def save_to_db(df):
    df.columns = ["ticker", "report_date", "eps_estimate", "eps_actual"]
    df.to_sql("earnings", engine, if_exists="append", index=False)


while True:
    for t in TICKERS:
        df = fetch_earnings(t)
        if df is not None:
            save_to_db(df)

    print("Updated...")
    time.sleep(3600)


if __name__ == "__main__":
    while True:
        for t in TICKERS:
            df = fetch_earnings(t)
            if df is not None:
                save_to_db(df)

        print("Updated...")
        time.sleep(3600)