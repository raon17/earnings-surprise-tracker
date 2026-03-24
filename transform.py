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
