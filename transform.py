# transform.py
import pandas as pd
import numpy as np

def calc_eps_surprise(df):
    df = df.copy()  
    df["surprise_pct"] = ((df["actualEarningResult"] - df["estimatedEarning"]) / df["estimatedEarning"].abs() * 100).round(2)                           

    def label(pct):
        if pct > 3:    return "beat"
        if pct < -3:   return "miss"
        return "inline"    

    df["result"] = df["surprise_pct"].apply(label)
    return df


def calc_beat_streak(df):

    df = df.sort_values("date", ascending=False)  
    streak = 0
    for result in df["result"]:
        if result == "beat":
            streak += 1
        else:
            break         
    return streak


def calc_price_reaction(eps_df, price_df, days_after=1):
    reactions = []

    for _, row in eps_df.iterrows():
        date = pd.to_datetime(row["date"])

        if date not in price_df.index:
            continue 

        future_dates = price_df.index[price_df.index > date]
        if len(future_dates) < days_after:
            continue

        next_day = future_dates[days_after - 1]
        price_before = price_df.loc[date, "close"]
        price_after  = price_df.loc[next_day, "close"]

        reaction_pct = ((price_after - price_before) / price_before * 100).round(2)
        reactions.append({ "date": date, "reaction_pct": reaction_pct })

    return pd.DataFrame(reactions)