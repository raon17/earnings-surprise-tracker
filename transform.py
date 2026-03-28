import pandas as pd

#function 1 
def add_surprise(df):
 
    if df.empty:
        return df
 
    df = df.copy() 
 
    if "surprise_pct_raw" in df.columns:
        df["surprise_pct"] = (df["surprise_pct_raw"] * 100).round(2)

    elif "eps" in df.columns and "epsEstimated" in df.columns:
        df = df[df["epsEstimated"] != 0].reset_index(drop=True)  
        df["surprise_pct"] = (
            (df["eps"] - df["epsEstimated"]) / df["epsEstimated"].abs() * 100
        ).round(2)
 
    else:
        print("transform: missing EPS columns")
        return df
 
    def label(pct):
        if pd.isna(pct): return "unknown"
        if pct > 3:      return "beat"
        if pct < -3:     return "miss"
        return "inline"
 
    df["result"] = df["surprise_pct"].apply(label)
 
    return df

#function 2
def beat_streak(df):

    if df.empty or "result" not in df.columns:
        return 0
 
    streak      = 0
    last_result = None
 
    for result in df["result"]:
        if result in ("inline", "unknown"):
            continue               
        if last_result is None:
            last_result = result   
        if result != last_result:
            break                  
        streak += 1 if result == "beat" else -1
 
    return streak
 