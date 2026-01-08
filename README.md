# NIFTY Smallcap 250 Stock Screening System

A rule-based screening and ranking system for NIFTY Smallcap 250 stocks, augmented with a simple machine learning classifier. This project is designed for **educational and research purposes only**.

---

## Overview

This system scans approximately 250 stocks in the NIFTY Smallcap 250 index daily, applying technical filters and a logistic regression model to produce a ranked list of candidate stocks. It is a **screening tool**, not an automated trading system, predictive oracle, or guaranteed profit generator.

The output is a daily ranked list of stocks that meet certain technical and fundamental criteria. All decisions remain with the human user.

---

## Scope

### What This System Does

- Downloads daily OHLCV (Open, High, Low, Close, Volume) data from Yahoo Finance.
- Computes technical indicators: EMA (10, 15, 20), RSI (14), ADX (14), ATR (14).
- Applies rule-based filters: trend direction, relative strength vs. NIFTY 50, volatility contraction patterns (VCP), weekly trend alignment.
- Assigns a heuristic rule score (0–10) based on how many criteria a stock satisfies.
- Uses a Logistic Regression classifier to estimate the probability of a specified price move within 5 trading days.
- Combines rule scores, ML probability, and financial health scores into a final confidence ranking.
- Outputs a ranked list of top 10 candidates with supporting metrics.

### What This System Does NOT Do

- **Predict future prices with certainty.** The model outputs probabilities, not guarantees.
- **Execute trades automatically.** This is a screening tool only.
- **Account for transaction costs, slippage, or liquidity constraints.**
- **Provide financial advice.** The output is for research and learning purposes.
- **Work reliably in all market regimes.** Performance may degrade in sideways or highly volatile markets.
- **Guarantee profitability.** Past patterns do not guarantee future results.

---

## Data Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT                                   │
│   OHLCV data (Yahoo Finance) for ~250 Smallcap stocks           │
│   + NIFTY 50 index data for relative strength calculation       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FEATURE ENGINEERING                          │
│   • EMA (10, 15, 20)     • RSI (14)        • ADX (14)           │
│   • ATR (14)             • VCP detection   • Weekly trend       │
│   • Relative Strength vs NIFTY 50                               │
│   • Quarterly financial health score                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RULE-BASED FILTERING                         │
│   • Liquidity filter (minimum volume)                           │
│   • Uptrend check (price > EMA)                                 │
│   • ADX > 25 (strong trend)                                     │
│   • RS > 1.05 (outperforming index)                             │
│   • Pattern classification (Breakout, Pullback, Momentum, etc.) │
│                                                                 │
│   Output: Rule Score (0–10)                                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ML SCORING                                   │
│   Calibrated Logistic Regression                                │
│   Input features:                                               │
│     • Normalized rule score                                     │
│     • EMA trend strength                                        │
│     • Boolean flags (bullish candles, consolidation, etc.)      │
│     • Financial health score                                    │
│                                                                 │
│   Output: Probability estimate (0–1)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIDENCE CALCULATION                       │
│   Final Score = 0.55 × ML_prob                                  │
│               + 0.30 × Rule_score_normalized                    │
│               + 0.15 × Pattern_bonus                            │
│               + Financial_adjustment                            │
│               - Penalties (no volume support, rejection, etc.)  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT                                       │
│   Top 10 ranked stocks with:                                    │
│     • Confidence score    • Pattern type     • Rule score       │
│     • Financial label     • Trailing stop level                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Machine Learning Component

### Model Choice: Logistic Regression

Logistic Regression was chosen for the following reasons:

1. **Interpretability.** Coefficients are directly interpretable, which aids in debugging and understanding model behavior.
2. **Calibration.** With probability calibration, outputs can be interpreted as approximate probabilities rather than arbitrary scores.
3. **Low variance.** Simple models are less prone to overfitting on noisy financial data with limited samples.
4. **Baseline appropriateness.** For a student project, a simple model is more defensible than complex alternatives that may overfit.

### What "68% Accuracy" Means

If the model reports ~68% accuracy, this refers to:

- **Label definition:** Binary classification—whether the stock price moved above a threshold (e.g., +X%) within 5 trading days.
- **Evaluation method:** Train/test split or cross-validation on historical labeled data.
- **Time horizon:** 5 trading days forward from the screening date.

**Important caveats:**

- Accuracy alone is a weak metric for imbalanced classes. Precision, recall, and confusion matrices are more informative.
- The label threshold and time horizon directly affect reported accuracy.
- Historical accuracy does not guarantee future performance.
- Market regime shifts (e.g., bull → bear) can invalidate trained patterns.

### Model Limitations

- **Small feature set.** The model uses only 8 features, limiting its discriminative power.
- **Label leakage risk.** If labels were constructed using data overlapping with features, reported metrics may be inflated.
- **Non-stationarity.** Financial markets are non-stationary; patterns that worked historically may not persist.
- **No ensemble or regularization tuning.** The baseline model does not incorporate advanced regularization or stacking.
- **Limited validation.** Walk-forward or expanding-window validation is not implemented; standard train/test splits can lead to look-ahead bias.

---

## Backtesting and Validation

### Current Backtesting Implementation

The included `simple_backtest.py` provides a basic simulation:

- Iterates through historical data for a single stock.
- Simulates entries based on simplified rule-based criteria (uptrend + RSI < 70).
- Uses ATR-based take-profit (1.5 × ATR) and stop-loss (1 × ATR).
- Reports win rate and average return.

### Limitations of the Backtest

| Limitation | Impact |
|------------|--------|
| Single-stock execution | No portfolio-level analysis |
| Simplified entry logic | Does not mirror full prediction pipeline |
| No transaction costs | Overstates net returns |
| No slippage modeling | Ignores execution reality |
| Fixed TP/SL ratios | Does not adapt to volatility regimes |
| No walk-forward validation | Potential look-ahead bias |
| No benchmark comparison | Cannot assess if system beats buy-and-hold |

**Honest Assessment:** The backtest is a proof-of-concept, not a rigorous validation framework. Results should be treated as indicative, not definitive.

---

## Assumptions and Failure Cases

### Key Assumptions

1. **Data quality.** Yahoo Finance data is accurate and timely.
2. **Market hours.** Scans run after market close; next-day prices are used for hypothetical entries.
3. **Liquidity.** Assumes sufficient liquidity to enter/exit at expected prices.
4. **Trend persistence.** Assumes short-term trends continue for 1–5 days.
5. **No major gaps.** Does not model overnight gap risk or limit-up/limit-down scenarios.

### Known Failure Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Sharp market reversal (e.g., sudden bearish news) | Model may generate signals just before a crash |
| Low-liquidity stocks slipping through filters | Execution may differ significantly from backtested prices |
| Extended sideways/range-bound markets | Low signal quality; many false positives |
| Corporate actions (splits, mergers) | Data artifacts may trigger spurious signals |
| API rate limits or data outages | Pipeline may fail silently or produce stale results |

---

## Project Structure

```
├── backtesting/           # Simple backtesting engine
│   └── simple_backtest.py
├── data/                  # Cached historical data
├── features/              # Feature engineering modules
│   ├── indicators.py      # EMA, RSI, ADX, ATR, VCP
│   ├── patterns.py        # Pattern classification
│   ├── market_regime.py   # Relative strength calculation
│   ├── financials.py      # Quarterly financial analysis
│   └── liquidity.py       # Volume filters
├── ml/                    # Machine learning components
│   ├── model.py           # Model loading
│   ├── model.pkl          # Serialized trained model
│   ├── predict.py         # Inference pipeline
│   └── confidence.py      # Score combination logic
├── output/                # Daily output CSVs
├── ranking/               # Ranking and trade plan logic
├── universe/              # Stock universe definition
│   └── smallcap_250.csv
├── utils/                 # Helper utilities
├── run_daily.py           # Main entry point
├── server.py              # Optional web dashboard
└── requirements.txt       # Python dependencies
```

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run daily scan
python run_daily.py

# Run backtest on a single stock
python -m backtesting.simple_backtest
```

---

## What This Project Demonstrates

This project is intended as a portfolio piece demonstrating practical skills, not a production trading system.

### Technical Skills Demonstrated

| Skill Area | Implementation |
|------------|----------------|
| **Data Engineering** | Fetching, cleaning, and caching OHLCV data from external APIs |
| **Feature Engineering** | Computing technical indicators (EMA, RSI, ADX, ATR, VCP) from raw price data |
| **Rule-Based Systems** | Implementing interpretable filtering logic with clear thresholds |
| **Machine Learning** | Training and deploying a calibrated logistic regression classifier |
| **Model Integration** | Combining ML outputs with heuristic scores in a weighted ensemble |
| **Backtesting Fundamentals** | Simulating historical trades with entry/exit logic and performance metrics |
| **Code Organization** | Modular project structure separating concerns (features, ML, ranking, utils) |
| **Evaluation Discipline** | Documenting limitations, assumptions, and failure modes |

### Lessons in Practical ML Limitations

1. **Noisy labels.** Stock movements are influenced by countless factors; binary labels oversimplify reality.
2. **Non-stationarity.** Market patterns evolve; static models degrade over time.
3. **Overfitting risk.** With limited data and many potential features, simple models are often more robust.
4. **Metric choice matters.** Accuracy can be misleading; domain-appropriate metrics (e.g., Sharpe ratio, max drawdown) are more informative.
5. **Validation complexity.** Standard train/test splits are insufficient for time-series data; walk-forward validation is preferred but more complex.

---

## Disclaimer

This project is built for **educational and research purposes only**. It is **not financial advice**. Trading in securities involves significant risk of loss. Users should consult a SEBI-registered investment advisor before making any investment decisions.

Past performance of any model, backtested or otherwise, does not guarantee future results. The authors make no claims regarding the profitability or reliability of this system.
