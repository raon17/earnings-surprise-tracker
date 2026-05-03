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

if __name__ == "__main__":
    all_earnings = []
    for ticker in TICKERS:
        earnings = fetch_earnings(ticker)
        if earnings is not None:
            all_earnings.append(earnings)

    if all_earnings:
        combined_df = pd.concat(all_earnings, ignore_index=True)
        save_to_db(combined_df)
        print("Earnings data saved to database.")
    else:
        print("No earnings data found.")
        