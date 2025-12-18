import pandas as pd
from utils.yf_loader import load_daily_data
from features.indicators import add_ema

def get_market_regime():
    """
    Fetches NIFTY 50 index (^NSEI) and determines market status.
    Returns:
        nifty_df (pd.DataFrame): DataFrame with columns [date, close, ema_50]
        status (str): "BULLISH" or "BEARISH"
    """
    print("Fetching NIFTY 50 data...")
    df = load_daily_data("^NSEI", period="1y")
    
    if df is None or len(df) < 50:
        print("Warning: Could not fetch NIFTY 50 data. Assuming Neutral/Bullish to allow scan.")
        return None, "NEUTRAL"

    df = add_ema(df, 50)
    current_close = df["close"].iloc[-1]
    ema_50 = df["ema_50"].iloc[-1]
    
    status = "BULLISH" if current_close > ema_50 else "BEARISH"
    return df, status

def calculate_rs(stock_df, nifty_df, lookback=50):
    """
    Calculates Relative Strength (Ratio) vs Nifty 50.
    Returns the RS score (slope of the ratio line) or simply the ratio trend.
    
    Simple implementation: 
    Rel Strength = (Stock/Stock_50d_ago) / (Nifty/Nifty_50d_ago)
    """
    if nifty_df is None or len(nifty_df) < lookback:
        return 0.0
    
    # Align dates (simple merge on date)
    # Ensure date columns are datetime
    stock_df["date"] = pd.to_datetime(stock_df["date"])
    nifty_df["date"] = pd.to_datetime(nifty_df["date"])
    
    merged = pd.merge(stock_df[["date", "close"]], nifty_df[["date", "close"]], on="date", how="inner", suffixes=("_stock", "_nifty"))
    
    if len(merged) < lookback:
        return 0.0
        
    current_ratio = merged["close_stock"].iloc[-1] / merged["close_stock"].iloc[-lookback]
    nifty_ratio = merged["close_nifty"].iloc[-1] / merged["close_nifty"].iloc[-lookback]
    
    rs_score = current_ratio / nifty_ratio
    return round(rs_score, 3)
