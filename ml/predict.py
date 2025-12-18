import numpy as np
import pandas as pd

from ml.confidence import compute_confidence
from ml.model import load_model

from features.indicators import (
    is_uptrend,
    ema_trend_strength,
    add_rsi,
    add_adx
)

from features.patterns import (
    classify_pattern,
    has_rejection_near_resistance
)

from features.liquidity import liquidity_pass
from features.financials import analyze_quarterly_financials

from utils.helpers import (
    has_bullish_candles,
    is_consolidating,
    volume_supports_breakout,
    is_near_resistance,
    compute_resistance
)
from utils.financials_loader import get_quarterly_financials

# Load trained & calibrated model
MODEL = load_model()


from features.market_regime import calculate_rs

def predict_today_probability(df, symbol, nifty_df=None):
    """
    Returns:
    - ml_probability (float)
    - confidence (float)
    - pattern (str)
    - rule_score (int)
    - financial_label (str)
    """

    # ------------------------
    # 1. BASIC FILTERS
    # ------------------------
    if not liquidity_pass(df):
        return None, None, None, 0, "Neutral"

    # ------------------------
    # 1.5. FINANCIAL ANALYSIS
    # ------------------------
    ticker = symbol if symbol.endswith(".NS") else symbol + ".NS"
    financials_df = get_quarterly_financials(ticker)
    financial_analysis = analyze_quarterly_financials(financials_df)
    financial_label = financial_analysis["financial_label"]
    financial_score = financial_analysis["financial_score"]

    uptrend = is_uptrend(df)
    bullish_candles = has_bullish_candles(df)
    consolidation = is_consolidating(df)
    volume_support = volume_supports_breakout(df)

    resistance = compute_resistance(df)
    near_res = is_near_resistance(df, resistance)

    # ------------------------
    # ADVANCED INDICATORS (Step 1 of Integration)
    # ------------------------
    df = add_rsi(df)
    df = add_adx(df)
    
    rsi_val = df["rsi_14"].iloc[-1] if "rsi_14" in df.columns else None
    
    # ADX Check (> 25 is strong trend)
    adx_val = df["adx_14"].iloc[-1] if "adx_14" in df.columns else 0
    strong_trend = adx_val > 25
    
    # Volatility Squeeze
    from features.indicators import get_volatility_squeeze
    vcp = get_volatility_squeeze(df)
    
    # Relative Strength (vs Nifty 50)
    rs_score = calculate_rs(df, nifty_df)
    
    # Weekly Trend Check (Resampling)
    # Convert daily to weekly
    try:
        # Ensure index is datetime
        df.index = pd.to_datetime(df["date"])
        weekly = df.resample('W').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})
        weekly["ema_20"] = weekly["close"].ewm(span=20, adjust=False).mean()
        weekly_trend = weekly["close"].iloc[-1] > weekly["ema_20"].iloc[-1] if len(weekly) > 20 else True
    except Exception as e:
        print(f"Warning: Weekly resample failed for {symbol}: {e}")
        weekly_trend = True # Default to True to not block

    # ------------------------
    # 2. PATTERN CLASSIFICATION
    # ------------------------
    pattern = classify_pattern(
        df=df,
        uptrend=uptrend,
        bullish_candles=bullish_candles,
        consolidation=consolidation,
        volume_support=volume_support,
        near_res=near_res,
        resistance=resistance,
        rsi_val=rsi_val
    )

    if pattern is None:
        return None, None, None, 0, financial_label

    # ------------------------
    # 3. RULE SCORE (0–10)
    # ------------------------
    rule_score = 0

    if uptrend:
        rule_score += 2
    if bullish_candles:
        rule_score += 1
    if consolidation:
        rule_score += 1
    if volume_support:
        rule_score += 1
    if near_res:
        rule_score += 1
    
    # Advanced Signals Bonus
    if strong_trend: # ADX > 25
        rule_score += 1
    if weekly_trend:
        rule_score += 1
    if vcp:
        rule_score += 1
    if rs_score > 1.05: # Outperforming by 5% over period
        rule_score += 1

    rule_score = min(rule_score, 10)

    # ------------------------
    # 4. ML FEATURES (MATCH TRAINING)
    # ------------------------
    features = np.array([
        rule_score / 10,                 # rule_score_norm
        ema_trend_strength(df),           # ema_trend_strength
        int(bullish_candles),             # bullish_candles
        int(consolidation),               # consolidation
        int(volume_support),              # volume_support
        int(near_res),                    # near_resistance
        financial_score,                  # results_score
        0.0                               # future expansion placeholder
    ]).reshape(1, -1)

    # ------------------------
    # 5. ML PROBABILITY
    # ------------------------
    ml_prob = MODEL.predict_proba(features)[0][1]

    # ------------------------
    # 6. CONFIDENCE SHAPING (STEP 6)
    # ------------------------
    rejection = has_rejection_near_resistance(df, resistance)

    confidence = compute_confidence(
        ml_prob=ml_prob,
        rule_score_norm=rule_score / 10,
        pattern=pattern,
        volume_support=int(volume_support),
        rejection=int(rejection),
        financial_score=financial_score
    )

    return float(ml_prob), confidence, pattern, rule_score, financial_label
