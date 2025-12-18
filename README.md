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
- 📊 Logs results for **30-day performance tracking**

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

- Model: **Calibrated Logistic Regression**
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

## 📂 Project Structure

```text
├── data/                  # Historical stock data storage
├── models/                # Trained ML models for trend confirmation
├── output/                # Daily Excel logs and performance tracking
├── strategies/            # Price action logic and trend definitions
├── utils/                 # Helper functions (indicators, math)
├── run_daily.py           # Main execution script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
# NIFTY Smallcap Trade Scanner
```
# NIFTY Smallcap Trade Scanner

## ▶️ How To Run

Execute the scanner **after market close** to ensure data completeness.

1. **Install Dependencies:**
pip install -r requirements.txt
2. **Run the Scanner:**
run run_daily.py


**Output:** The script scans all 250 NIFTY Smallcap stocks and outputs the **Top 5 high-probability trade setups** based on the algorithm.

## 📊 Performance Tracking

We believe in radical transparency. Trades are logged daily into a local Excel sheet (`/output/trade_log.xlsx`) for forward testing.

**Tracking Methodology:**
- Trades are logged automatically after the scan.
- Holding Days are auto-calculated based on entry date.
- Outcomes are manually updated for validation.

**Visual Status:**
- ✅ **HIT:** Full row turns Green (Target Achieved).
- ❌ **FAIL:** Full row turns Red (Stop Loss Hit).

**Purpose:** Used for real 30-day forward performance validation to ensure the model adapts to changing market conditions.

## 🧱 Project Philosophy

This scanner is built on specific core principles to ensure longevity and capital preservation:

- 📉 **Avoid Choppiness:** We filter out low-quality, sideways charts.
- 📈 **Trend + Structure:** We only trade when Price Action aligns with the dominant trend.
- 🧠 **ML Confirmation:** Machine Learning is used to confirm a setup, never to force a trade.
- 🎯 **Probability > Prediction:** We don't guess; we play the statistical edge.
- 🛑 **Risk First:** Risk management protocols are calculated before return targets.

## 🚀 Future Improvements

- [ ] Telegram Integration: Automated alerts for the Top 5 picks.
- [ ] Backtesting Engine: To simulate strategy performance over the last 5 years.
- [ ] Sector Heatmap: Filtering stocks based on sector rotation.
- [ ] Dashboard: A simple web UI (Streamlit) to visualize the daily picks.

## ⚠️ Disclaimer

This project is built for **educational and research purposes only**.  
It is **not financial advice**. Trading in the stock market involves significant risk. Please consult a **SEBI-registered financial advisor** before making any investment decisions. The developers of this tool are not responsible for any financial losses.

**Built with ❤️ using price action, discipline, and data.**
  



