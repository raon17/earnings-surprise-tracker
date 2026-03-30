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
 
if __name__ == "__main__":
    pass