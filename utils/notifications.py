import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def send_whatsapp_message(message):
    """
    Sends a WhatsApp message using GreenAPI (Free Developer Tier).
    Requires 'GREENAPI_INSTANCE_ID' and 'GREENAPI_API_TOKEN' environment variables.
    And 'GREENAPI_TARGET_PHONE' (the number to send TO).
    """
    instance_id = os.environ.get("GREENAPI_INSTANCE_ID")
    api_token = os.environ.get("GREENAPI_API_TOKEN")
    target_phone = os.environ.get("GREENAPI_TARGET_PHONE")

    if not instance_id or not api_token or not target_phone:
        print("Warning: GreenAPI credentials (INSTANCE_ID, API_TOKEN, TARGET_PHONE) not found. Skipping.")
        return

    print(f"Sending WhatsApp message to {target_phone} via GreenAPI...")

    # Use the specific host provided by the user (or default to api.green-api.com)
    # Ideally this should be an env var too, but we'll default to the one they have or generic.
    host = os.environ.get("GREENAPI_HOST", "7105.api.greenapi.com") 
    url = f"https://{host}/waInstance{instance_id}/SendMessage/{api_token}"

    payload = {
        "chatId": f"{target_phone}@c.us",
        "message": message
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if response.status_code == 200:
            print("WhatsApp message sent successfully!")
        else:
            print(f"Failed to send WhatsApp message. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

def format_daily_summary(df):
    """
    Formats the daily top picks DataFrame into a string for WhatsApp.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    if df.empty:
        return f"Stock Analyser ({today}):\nNo valid setups found today."

    msg = f"*Stock Analyser - Top Picks ({today})*\n\n"
    
    # Iterate over top 5
    for index, row in df.head(5).iterrows():
        symbol = row.get('symbol', 'N/A')
        rank = row.get('rank', index + 1)
        conf = row.get('confidence', 0.0)
        
        # Format: 
        # 1. SYMBOL (95%)
        #    TP1: 100 | SL: 90 | Fin: Good
        tp1 = row.get('tp1', 0)
        sl = row.get('sl', 0)
        fin = row.get('financials', 'N/A')
        
        msg += f"{rank}. *{symbol}* ({conf:.0%})\n"
        msg += f"   TP1: {tp1} | SL: {sl} | Fin: {fin}\n"
    
    msg += "\n_Check email/logs for details._"
    return msg
