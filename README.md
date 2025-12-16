# 🚀 Smallcap-250 Smart Trade Scanner (India)

A **rule-driven + ML-assisted stock scanner** for the **NIFTY Smallcap 250**, designed for **short-term swing trades (1–5 days)** with strict risk management.

---

## 🔍 What This Project Does

Every trading day **after market close**, the system:

- 📥 Fetches daily price & volume data (Yahoo Finance)
- 🚫 Filters illiquid and choppy charts
- 📐 Calculates EMA, ATR & volume metrics
- 🧩 Detects clean bullish price-action setups
- 🤖 Predicts **5-day upside probability** using ML
- 🏆 Ranks the **Top 5 Smallcap stocks**
- 🎯 Generates **Entry, SL, TP1–TP3**
- 📊 Logs daily picks for performance tracking

---

## 📊 Trade Style

| Parameter | Value |
|--------|------|
| Market | NSE 🇮🇳 |
| Universe | NIFTY Smallcap 250 |
| Timeframe | Daily |
| Holding Period | 1–5 days |
| Target Range | 5% – 20% |

---

## 🧠 Patterns Detected

- 🔵 **TIGHT_BASE**
- 🚀 **BREAKOUT_SETUP**
- 🔁 **PULLBACK_CONTINUATION**
- 📈 **NEAR_52W_HIGH**
- ⚡ **MOMENTUM**

❌ Stocks with **long wick rejection** or **choppy structure** are automatically rejected.

---

## 🤖 Machine Learning (Used Carefully)

- Model: **Calibrated Logistic Regression** (stored under ml/model.pkl)
- Label: *Did the stock move X% within 5 trading days?*
- Handles class imbalance ✔
- ML **confirms** trades — rules come first

**Final confidence = Rule strength + ML probability**

---

## 📈 Sample Output

| Rank | Symbol        | Confidence | Pattern               |
|------|---------------|------------|-----------------------|
| 1    | IIFL.NS       | 0.58       | BREAKOUT_SETUP        |
| 2    | GRANULES.NS   | 0.55       | BREAKOUT_SETUP        |
| 3    | MANAPPURAM.NS | 0.51       | PULLBACK_CONTINUATION |
| 4    | PNBHOUSING.NS | 0.49       | PULLBACK_CONTINUATION |
| 5    | BSOFT.NS      | 0.47       | BREAKOUT_SETUP        |

---

## 📂 Project Structure

This README reflects the actual repository layout used by the scripts:

```text
├── charts/               # Chart generation and saved PNGs
├── data/                 # Historical stock data storage (processed CSVs)
├── features/             # Price-action rules, indicators, filters
├── ml/                   # Trained ML model and prediction wrappers (model.pkl)
├── output/               # Daily CSV outputs (top_picks_YYYY-MM-DD.csv)
├── ranking/              # Ranking & trade plan computation
├── universe/             # Universe CSV (smallcap_250.csv)
├── utils/                # Helper functions (data loaders, helpers)
├── run_daily.py          # Main execution script
└── README.md             # Project documentation
```

Notes:
- The trained model is under `ml/model.pkl`.
- Daily CSVs are saved as `output/top_picks_YYYY-MM-DD.csv` (see run_daily.py).
- Charts for ranked picks are generated and saved to the `charts/` folder.

---

# NIFTY Smallcap Trade Scanner

## ▶️ How To Run

Execute the scanner **after market close** to ensure data completeness.

1. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

2. **Run the Scanner:**

```bash
python run_daily.py
```

What happens when you run it:
- The script scans the universe in `universe/smallcap_250.csv`.
- It applies liquidity, indicator, trend and pattern filters.
- It computes ML probability and an overall confidence score.
- Top N picks (default 5) are written to `output/top_picks_<YYYY-MM-DD>.csv`.
- Charts for the ranked picks are generated and saved to `charts/`.

---

## 📊 Performance Tracking

This project logs daily picks to CSV files in `output/` for forward testing and tracking. The repository does not automatically maintain an Excel trade log; if you want an aggregated Excel file or a separate tracking sheet, export or aggregate the daily CSVs yourself.

**Tracking Methodology:**
- Picks are saved daily; outcomes and performance tracking must be handled separately or via custom tooling.

---

## 🧱 Project Philosophy

This scanner is built on specific core principles to ensure longevity and capital preservation:

- 📉 **Avoid Choppiness:** We filter out low-quality, sideways charts.
- 📈 **Trend + Structure:** We only trade when Price Action aligns with the dominant trend.
- 🧠 **ML Confirmation:** Machine Learning is used to confirm a setup, never to force a trade.
- 🎯 **Probability > Prediction:** We don't guess; we play the statistical edge.
- 🛑 **Risk First:** Risk management protocols are calculated before return targets.

---

## 🚀 Future Improvements

- [ ] Telegram Integration: Automated alerts for the Top 5 picks.
- [ ] Backtesting Engine: To simulate strategy performance over the last 5 years.
- [ ] Sector Heatmap: Filtering stocks based on sector rotation.
- [ ] Dashboard: A simple web UI (Streamlit) to visualize the daily picks.

---

## ⚠️ Disclaimer

This project is built for **educational and research purposes only**.  
It is **not financial advice**. Trading in the stock market involves significant risk. Please consult a **SEBI-registered financial advisor** before making any investment decisions. The developers of this tool are not responsible for any financial losses.

**Built with ❤️ using price action, discipline, and data.**
