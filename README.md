# Stock-analyser

A small-cap stock analysis and pick generator that:

- extracts features from price data,
- classifies price patterns,
- ranks and predicts top picks using a trained model,
- saves trade charts and top-picks CSVs.

Quick start
-----------
1. Install required Python packages (examples used in the code):
   - pandas
   - mplfinance
   - numpy
   - yfinance (or the data loader you use)

2. Run the daily pipeline:

   python run_daily.py

   This script runs the feature extraction, prediction and ranking pipeline and writes results to the output/ directory (CSV files named like top_picks_YYYY-MM-DD.csv). It also generates trade charts under charts/ (files saved as charts/{SYMBOL}.png).

Key implementation details
--------------------------
- Pattern classification (features/patterns.py):
  - Recognised pattern labels: TIGHT_BASE, BREAKOUT_SETUP, NEAR_52W_HIGH, PULLBACK_CONTINUATION, MOMENTUM.
  - Fake breakout rejection: has_rejection_near_resistance checks recent candles (default lookback=3) for bearish upper-wick rejections and rejects a setup when 2+ rejection candles are found.

- Trend check (features/trend.py):
  - in_uptrend requires at least 20 rows and checks short-term EMA alignment: latest close must be above ema_10 and ema_15, and ema_10 must not be below ema_15.

- Chart plotting (charts/plot.py):
  - plot_trade_chart saves a PNG at charts/{symbol}.png and draws ema_10, ema_15, volume, resistance (30-day high) and trade plan horizontal lines (tp1, tp2, tp3, sl).

Other notes
-----------
- Trained model: ml/model.pkl is used by the prediction pipeline (see ml/predict.py).
- Processed data is expected in data/processed/master_dataset.csv and the universe list is under universe/.

If you need more examples (module-level usage or API descriptions), add a request or open issues/PRs to expand this README.