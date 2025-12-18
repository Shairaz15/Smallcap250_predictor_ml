import pandas as pd
import numpy as np
from features.indicators import add_ema, add_atr, add_rsi, is_uptrend
from features.patterns import classify_pattern
from utils.yf_loader import load_daily_data

def run_backtest(symbol, days=200):
    """
    Simulates the strategy on the last N days for a single symbol.
    Logic is simplified: Enter if setup exists, Exit at TP1 or SL.
    """
    print(f"Backtesting {symbol} for last {days} days...")
    
    df = load_daily_data(symbol)
    if df is None or len(df) < days + 50:
        print("Not enough data.")
        return

    # Slice relevant data but keep enough for indicators
    df = df.tail(days + 50).copy()

    # Calculate Indicators
    df = add_ema(df, 10)
    df = add_ema(df, 15)
    df = add_atr(df, 14)
    df = add_rsi(df, 14)

    trades = []
    in_trade = False
    entry_price = 0
    tp1 = 0
    sl = 0
    entry_date = None

    for i in range(50, len(df)):
        # Simulate "Today"
        idx = df.index[i]
        today_data = df.iloc[:i+1] # Data available up to today
        
        current_close = df["close"].iloc[i]
        
        # Check Exit if in trade
        if in_trade:
            if df["high"].iloc[i] >= tp1:
                trades.append({
                    "entry_date": entry_date,
                    "exit_date": idx,
                    "result": "WIN",
                    "return_pct": (tp1 - entry_price) / entry_price
                })
                in_trade = False
            elif df["low"].iloc[i] <= sl:
                trades.append({
                    "entry_date": entry_date,
                    "exit_date": idx,
                    "result": "BOSS",
                    "return_pct": (sl - entry_price) / entry_price
                })
                in_trade = False
            continue

        # Check Entry Logic (Simplified for Backtest speed)
        # We re-use logic parts without the heavy ML prediction for speed in this simple test
        # or we could mock it. Here we stick to Rule-Based triggers.
        uptrend = is_uptrend(today_data)
        
        # Simplified "Near Resistance" check
        # (Copying simplified version of compute_resistance logic or just using raw price action)
        # For this simple backtest, we just assume purely pattern-based.
        
        # Skip for now if complicated, let's just use SMA crossover as a dummy or re-implement parts.
        # Ideally we import the exact logic.
        
        if uptrend and df["rsi_14"].iloc[i] < 70:
            # Assume entry
            entry_price = current_close
            atr = df["atr_14"].iloc[i]
            tp1 = entry_price + (1.5 * atr)
            sl = entry_price - atr
            entry_date = idx
            in_trade = True

    # Report
    print(f"\n--- Backtest Results for {symbol} ---")
    if not trades:
        print("No trades taken.")
        return

    wins = [t for t in trades if t["result"] == "WIN"]
    losses = [t for t in trades if t["result"] == "LOSS"]
    
    win_rate = len(wins) / len(trades)
    avg_return = pd.DataFrame(trades)["return_pct"].mean()

    print(f"Total Trades: {len(trades)}")
    print(f"Win Rate: {win_rate:.2%}")
    print(f"Avg Return: {avg_return:.2%}")
    print("-------------------------------------")

if __name__ == "__main__":
    run_backtest("IIFL.NS")
