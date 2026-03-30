import pandas as pd
 
def add_growth(df):
    if df.empty:
        return df
 
    df = df.copy()
 
    for col in ["revenue", "eps", "net_income"]:
        if col not in df.columns:
            continue
        df[f"{col}_qoq"] = df[col].pct_change(1).mul(100).round(2)
        df[f"{col}_yoy"] = df[col].pct_change(4).mul(100).round(2)
 
    return df

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
        return df
 
    def label(pct):
        if pd.isna(pct): return "unknown"
        if pct > 3:      return "beat"
        if pct < -3:     return "miss"
        return "inline"
 
    df["result"] = df["surprise_pct"].apply(label)
    return df

if __name__ == "__main__":
    sample = pd.DataFrame({
        "date":       pd.date_range("2024-01-01", periods=6, freq="QE"),
        "revenue":    [20e9, 22e9, 25e9, 30e9, 35e9, 44e9],
        "eps":        [0.76, 0.89, 1.08, 1.30, 1.76, 2.10],
        "net_income": [5e9,  6e9,  7e9,  8e9, 10e9, 12e9],
    })
    result = add_growth(sample)
    print(result[["date","revenue","revenue_qoq","revenue_yoy","eps","eps_qoq"]])