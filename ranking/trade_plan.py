def compute_trade_plan(df, probability):
    """
    Computes TP1, TP2, TP3, SL and their probabilities.
    """

    close = df["close"].iloc[-1]
    atr = df["atr_14"].iloc[-1]
    atr_pct = atr / close

    # Target percentages (ATR capped)
    tp1_pct = min(0.05, 1.2 * atr_pct)
    tp2_pct = min(0.10, 2.2 * atr_pct)
    tp3_pct = min(0.15, 3.5 * atr_pct)

    tp1 = close * (1 + tp1_pct)
    tp2 = close * (1 + tp2_pct)
    tp3 = close * (1 + tp3_pct)

    sl = close - atr
    trailing_sl = close - (1.5 * atr)

    # Probabilities
    p_tp1 = min(0.95, probability * 1.3)
    p_tp2 = probability
    p_tp3 = probability * 0.6

    return {
        "tp1": round(tp1, 2),
        "tp2": round(tp2, 2),
        "tp3": round(tp3, 2),
        "sl": round(sl, 2),
        "trailing_sl": round(trailing_sl, 2),
        "p_tp1": round(p_tp1, 2),
        "p_tp2": round(p_tp2, 2),
        "p_tp3": round(p_tp3, 2),
    }
