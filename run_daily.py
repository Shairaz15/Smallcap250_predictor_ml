import os
import pandas as pd
from datetime import datetime

from ranking.rank_today import rank_today

# Output folders
os.makedirs("output", exist_ok=True)

def run_daily():
    today_date = datetime.now()
    print(f"\nRunning daily scan for {today_date.strftime('%Y-%m-%d')}\n")

    # --- HOLIDAY LOGIC START ---
    # User Rule: "dont want it to run if the next day the market is closed"
    import calendar
    from datetime import timedelta
    
    next_day = today_date + timedelta(days=1)
    weekday = next_day.weekday() # 0=Mon, ... 5=Sat, 6=Sun

    # 1. Weekend Check (If next day is Sat or Sun, skip)
    if weekday >= 5:
        print(f"Skipping: Next day ({next_day.strftime('%A')}) is a weekend.")
        # return # TEMPORARY: Commented out for testing notification

    # 2. NSE Holidays 2025 (Hardcoded for reliability)
    # Format: YYYY-MM-DD
    nse_holidays_2025 = [
        "2025-01-26", # Republic Day
        "2025-02-26", # Mahashivratri
        "2025-03-14", # Holi
        "2025-03-31", # Eid-ul-Fitr
        "2025-04-10", # Mahavir Jayanti
        "2025-04-14", # Good Friday / Ambedkar Jayanti
        "2025-05-12", # Buddha Purnima
        "2025-06-07", # Bakri Id
        "2025-08-15", # Independence Day
        "2025-08-27", # Ganesh Chaturthi
        "2025-10-02", # Gandhi Jayanti
        "2025-10-21", # Diwali (Laxmi Pujan)
        "2025-10-22", # Diwali (Balipratipada)
        "2025-11-05", # Guru Nanak Jayanti
        "2025-12-25", # Christmas
    ]
    
    next_day_str = next_day.strftime("%Y-%m-%d")
    if next_day_str in nse_holidays_2025:
        print(f"Skipping: Next day ({next_day_str}) is a Market Holiday.")
        return
    # --- HOLIDAY LOGIC END ---

    df = rank_today("universe/smallcap_250.csv", top_n=5)

    if df.empty:
        print("No valid setups today.")
        from utils.notifications import send_whatsapp_message, format_daily_summary
        send_whatsapp_message(format_daily_summary(df))
        return

    # Save CSV
    csv_path = f"output/top_picks_{today}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Saved CSV: {csv_path}")

    # Console summary
    from utils.helpers import print_colored_df
    print("\nTOP PICKS TODAY:")
    print_colored_df(df[["rank", "symbol", "confidence", "pattern", "rule_score", "financials", "trailing_sl"]])

    # WhatsApp Notification
    from utils.notifications import send_whatsapp_message, format_daily_summary
    print("\n--- Sending Notification ---")
    msg = format_daily_summary(df)
    send_whatsapp_message(msg)


if __name__ == "__main__":
    run_daily()
