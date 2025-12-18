import pandas as pd

def analyze_quarterly_financials(financials_df):
    """
    Analyzes the quarterly financials to determine if the performance is "Good", "Bad", or "Neutral".

    Args:
        financials_df (pd.DataFrame): DataFrame with quarterly financial data from yfinance.

    Returns:
        dict: A dictionary containing 'financial_label' ("Good", "Bad", "Neutral") and
              'financial_score' (0.1, -0.1, 0).
    """
    result = {
        "financial_label": "Neutral",
        "financial_score": 0.0
    }

    if financials_df is None:
        print("DEBUG: Financials dataframe is None.")
        return result
    if financials_df.empty:
        print("DEBUG: Financials dataframe is empty.")
        return result

    try:
        # yfinance quarterly_financials has the most recent quarter as the first column.
        if len(financials_df.columns) < 2:
            print(f"DEBUG: Not enough quarterly data to compare (columns: {len(financials_df.columns)}).")
            return result
            
        # Get the two most recent quarters
        latest_quarter = financials_df.iloc[:, 0]
        previous_quarter = financials_df.iloc[:, 1]

        # Robust Key Lookup (Total Revenue vs Operating Revenue)
        revenue_keys = ['Total Revenue', 'Operating Revenue', 'Revenue']
        latest_revenue = None
        previous_revenue = None

        for key in revenue_keys:
            if key in latest_quarter.index and key in previous_quarter.index:
                latest_revenue = latest_quarter[key]
                previous_revenue = previous_quarter[key]
                break
        
        if latest_revenue is None:
            return {"financial_label": "Neutral (NoKey)", "financial_score": 0.0}

        # Ensure values are numeric
        try:
            latest_revenue = float(latest_revenue)
            previous_revenue = float(previous_revenue)
        except Exception as conversion_e:
            print(f"DEBUG: Could not convert revenue to float: {conversion_e}")
            return {"financial_label": "Neutral (TypeErr)", "financial_score": 0.0}

        if previous_revenue == 0:
            result["financial_label"] = 0.5 # Default if prev revenue is 0
            result["financial_score"] = 0.0
        else:
            growth = (latest_revenue - previous_revenue) / previous_revenue
            
            # Map growth to score: 0% grow -> 0.5. +25% -> 1.0. -25% -> 0.0
            score = 0.5 + (growth * 2)
            score = max(0.0, min(1.0, score)) # Clamp
            
            result["financial_label"] = round(score, 2)
            
            # ML Bonus: Scale 0-1 back to approx -0.1 to +0.1
            # 0.5 -> 0.0
            # 1.0 -> 0.1
            # 0.0 -> -0.1
            result["financial_score"] = (score - 0.5) * 0.2

    except Exception as e:
        print(f"Could not analyze financial data: {e}")
        # Return neutral if any error occurs
        return {
            "financial_label": f"Neutral ({type(e).__name__})",
            "financial_score": 0.0
        }

    return result
