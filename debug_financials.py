import yfinance as yf
import pandas as pd

symbol = "PRAJIND.NS"
print(f"Fetching financials for {symbol}...")
stock = yf.Ticker(symbol)
qf = stock.quarterly_financials

if qf is None or qf.empty:
    print("Quarterly financials is None or Empty.")
else:
    print("\n--- Columns (Dates) ---")
    print(qf.columns)
    print("\n--- Index (Rows) ---")
    print(qf.index)
    
    print("\n--- First few rows ---")
    print(qf.head())

    # Test our logic
    print("\n--- Logic Test ---")
    latest_quarter = qf.iloc[:, 0]
    previous_quarter = qf.iloc[:, 1]
    
    revenue_keys = ['Total Revenue', 'Operating Revenue', 'Revenue']
    for key in revenue_keys:
        print(f"Checking key '{key}': In Latest? {key in latest_quarter.index}, In Previous? {key in previous_quarter.index}")
        if key in latest_quarter.index:
            print(f"  Value Latest: {latest_quarter[key]}")
        if key in previous_quarter.index:
            print(f"  Value Previous: {previous_quarter[key]}")
