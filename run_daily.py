import os
import pandas as pd
from datetime import datetime

from ranking.rank_today import rank_today

# Output folders
os.makedirs("output", exist_ok=True)

def run_daily():
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"\nRunning daily scan for {today}\n")

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
