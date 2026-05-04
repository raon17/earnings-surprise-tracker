import yfinance as yf
import datetime
import logging


WATCHLIST = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "JPM", "BAC", "GS", "MS", "AMD", "INTC", "QCOM", "V", "MA", "PYPL", "WMT", "COST", "TGT", "DIS", "NFLX", "SPOT",
]

def fetch_ticker(ticker: str):

    try:
        t = yf.Ticker(ticker)
        cal = t.calendar
        info = t.info

        if not cal or "Earnings Date" not in cal:
            return None

        dates = cal["Earnings Date"]
        if not dates:
            return None

        today = datetime.date.today()
        nearest = min(
            dates,
            key=lambda d: abs((d.date() if hasattr(d, "date") else d) - today)
        )
        report_date = nearest.date().isoformat() if hasattr(nearest, "date") else str(nearest)
