from features.financials import analyze_quarterly_financials
from utils.financials_loader import get_quarterly_financials
import pandas as pd

symbol = "PRAJIND.NS"
print(f"Testing Financials Logic for {symbol}")

df = get_quarterly_financials(symbol)
if df is not None:
    print("Financials DF Shape:", df.shape)
    analysis = analyze_quarterly_financials(df)
    print("Result:", analysis)
else:
    print("DF is None")
