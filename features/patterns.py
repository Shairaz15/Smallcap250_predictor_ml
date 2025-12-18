def classify_pattern(
    df,
    uptrend,
    bullish_candles,
    consolidation,
    volume_support,
    near_res,
    resistance,
    rsi_val=None
):
    """
    Classifies stock into one dominant pattern.
    Applies rejection filter near resistance.
    """
    
    # 🔴 RSI FILTER: Avoid buying overbought
    if rsi_val is not None and rsi_val > 75:
        return None

    # 🔴 HARD FILTER: reject fake breakouts
    if near_res:
        if has_rejection_near_resistance(df, resistance):
            return None

    # 1. Tight Base
    if consolidation and volume_support:
        return "TIGHT_BASE"

    # 2. Breakout Setup
    if near_res and uptrend and bullish_candles:
        return "BREAKOUT_SETUP"

    # 3. Near 52W / Resistance high
    if near_res and uptrend and not consolidation:
        return "NEAR_52W_HIGH"

    # 4. Pullback continuation
    if uptrend and bullish_candles and not near_res:
        return "PULLBACK_CONTINUATION"

    # 5. Momentum fallback
    if uptrend:
        return "MOMENTUM"

    return None

def has_rejection_near_resistance(df, resistance, lookback=3, wick_ratio_threshold=0.4):
    """
    Detects bearish rejection near resistance using upper wick analysis.

    Returns True if rejection exists (i.e., setup should be rejected).
    """

    recent = df.tail(lookback)

    rejection_count = 0

    for _, row in recent.iterrows():
        high = row["high"]
        low = row["low"]
        open_ = row["open"]
        close = row["close"]

        candle_range = high - low
        if candle_range == 0:
            continue

        upper_wick = high - max(open_, close)
        upper_wick_ratio = upper_wick / candle_range

        is_bearish_or_small = close <= open_ or abs(close - open_) / candle_range < 0.25

        if upper_wick_ratio >= wick_ratio_threshold and is_bearish_or_small:
            rejection_count += 1

    # If 2 or more rejection candles near resistance → reject
    return rejection_count >= 2

