import pandas as pd
import numpy as np


# -------------------------
# EMA CORE
# -------------------------
def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()


# -------------------------
# ADD EMA (FLEXIBLE)
# -------------------------
def add_ema(df, period):
    """
    Adds EMA column for given period.
    Example: add_ema(df, 10) -> ema_10
    """

    col = f"ema_{period}"

    if col not in df.columns:
        df[col] = ema(df["close"], period)

    return df


# -------------------------
# ATR CORE
# -------------------------
def atr(df, period=14):
    high = df["high"]
    low = df["low"]
    close = df["close"]

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)

    return tr.rolling(period).mean()


# -------------------------
# ADD ATR
# -------------------------
def add_atr(df, period=14):
    """
    Adds ATR column.
    """

    col = f"atr_{period}"

    if col not in df.columns:
        df[col] = atr(df, period)

    return df


# -------------------------
# TREND LOGIC
# -------------------------
def is_uptrend(df, lookback=20):
    """
    Uptrend definition:
    - EMA(10) > EMA(15)
    - Close above EMA(15)
    """

    if len(df) < lookback:
        return False

    df = add_ema(df, 10)
    df = add_ema(df, 15)

    return (
        df["ema_10"].iloc[-1] > df["ema_15"].iloc[-1]
        and df["close"].iloc[-1] > df["ema_15"].iloc[-1]
    )


# -------------------------
# ML FEATURE
# -------------------------
def ema_trend_strength(df):
    """
    Normalized EMA distance (ML feature).
    """

    if len(df) < 20:
        return 0.0

    df = add_ema(df, 10)
    df = add_ema(df, 15)

    return float(
        (df["ema_10"].iloc[-1] - df["ema_15"].iloc[-1])
        / df["ema_15"].iloc[-1]
    )


# -------------------------
# RSI INDICATOR
# -------------------------
def add_rsi(df, period=14):
    """
    Adds RSI column.
    Uses Wilder's Smoothing.
    """
    col = f"rsi_{period}"
    
    if col in df.columns:
        return df

    delta = df["close"].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)

    # Wilder's Smoothing
    ma_up = up.ewm(com=period - 1, adjust=False, min_periods=period).mean()
    ma_down = down.ewm(com=period - 1, adjust=False, min_periods=period).mean()

    rs = ma_up / ma_down
    df[col] = 100 - (100 / (1 + rs))

    return df


# -------------------------
# ADX INDICATOR
# -------------------------
def add_adx(df, period=14):
    """
    Computes ADX (Trend Strength).
    """
    if f"adx_{period}" in df.columns:
        return df
        
    plus_dm = df["high"].diff()
    minus_dm = df["low"].diff()
    
    plus_dm = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0.0)
    minus_dm = np.where((minus_dm > plus_dm) & (minus_dm > 0), -minus_dm, 0.0)
    
    tr = atr(df, period=1) # True Range for 1 period
    
    # Smooth
    tr_smooth = pd.Series(tr).rolling(period).sum()
    plus_dm_smooth = pd.Series(plus_dm).rolling(period).sum()
    minus_dm_smooth = pd.Series(minus_dm).rolling(period).sum()
    
    plus_di = 100 * (plus_dm_smooth / tr_smooth)
    minus_di = 100 * (minus_dm_smooth / tr_smooth)
    
    dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(period).mean()
    
    df[f"adx_{period}"] = adx
    return df


# -------------------------
# VCP / VOLATILITY SQUEEZE
# -------------------------
def get_volatility_squeeze(df, lookback=10, avg_lookback=50):
    """
    Returns True if recent volatility (std dev) is < 50% of historical average.
    """
    if len(df) < avg_lookback:
        return False
        
    df["log_ret"] = np.log(df["close"] / df["close"].shift(1))
    
    recent_std = df["log_ret"].tail(lookback).std()
    hist_std = df["log_ret"].tail(avg_lookback).std()
    
    return recent_std < (hist_std * 0.5)
