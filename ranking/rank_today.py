import pandas as pd

from utils.yf_loader import load_daily_data
from features.liquidity import passes_liquidity_filter
from features.indicators import add_ema, add_atr
from features.trend import in_uptrend
from ml.predict import predict_today_probability
from ranking.trade_plan import compute_trade_plan


from features.market_regime import get_market_regime


def rank_today(universe_csv, top_n=5):
    # 1. Fetch Market Regime (NIFTY 50)
    nifty_df, market_status = get_market_regime()
    
    if market_status == "BEARISH":
        print("\n⚠️  MARKET REGIME WARNING: NIFTY 50 is below 50-day EMA (Bearish).")
        print("    Stricter filters will apply. Cash is a position.\n")

    universe = pd.read_csv(universe_csv)
    symbols = universe.iloc[:, 0].tolist()

    rows = []

    for symbol in symbols:
        print(f"Scoring {symbol}...")

        df = load_daily_data(symbol)
        if df is None or len(df) < 100:
            continue

        if not passes_liquidity_filter(df):
            continue

        df = add_ema(df, 10)
        df = add_ema(df, 15)
        df = add_atr(df, 14)

        if not in_uptrend(df):
            continue

        # ML + confidence (STEP 6)
        # Pass nifty_df for Relative Strength calc
        ml_prob, confidence, pattern, rule_score, financial_label = predict_today_probability(df, symbol, nifty_df)

        if ml_prob is None:
            continue
        
        # Hard Filter for Bearish Market: Only take 8+ score setups
        if market_status == "BEARISH" and rule_score < 8:
            continue

        trade = compute_trade_plan(df, ml_prob)

        rows.append({
            "symbol": symbol,
            "probability": round(ml_prob, 3),
            "confidence": confidence,
            "pattern": pattern,
            "rule_score": rule_score,
            "financials": financial_label,
            "tp1": trade["tp1"],
            "tp2": trade["tp2"],
            "tp3": trade["tp3"],
            "sl": trade["sl"],
            "trailing_sl": trade.get("trailing_sl", 0),
            "p_tp1": trade["p_tp1"],
            "p_tp2": trade["p_tp2"],
            "p_tp3": trade["p_tp3"],
        })

    if not rows:
        return pd.DataFrame()

    result = pd.DataFrame(rows)

    result = result.sort_values("confidence", ascending=False).head(top_n)
    result.insert(0, "rank", range(1, len(result) + 1))

    return result
