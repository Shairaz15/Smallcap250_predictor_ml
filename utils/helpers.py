import numpy as np


# -----------------------------
# CANDLE QUALITY
# -----------------------------
def has_bullish_candles(df, lookback=3):
    """
    Checks if majority of recent candles are bullish.
    """
    recent = df.tail(lookback)
    bullish = (recent["close"] > recent["open"]).sum()
    return bullish >= (lookback // 2 + 1)


# -----------------------------
# CONSOLIDATION
# -----------------------------
def is_consolidating(df, lookback=10, threshold=0.03):
    """
    Checks if price is consolidating (tight range).
    """
    recent = df.tail(lookback)
    high = recent["high"].max()
    low = recent["low"].min()

    if low == 0:
        return False

    return (high - low) / low <= threshold


# -----------------------------
# VOLUME SUPPORT
# -----------------------------
def is_volume_supporting(df, short=5, long=20, min_ratio=1.2):
    """
    Checks if recent volume is higher than baseline volume.
    """
    if len(df) < long:
        return False

    recent_vol = df["volume"].tail(short).mean()
    base_vol = df["volume"].tail(long).mean()

    if base_vol == 0:
        return False

    return recent_vol / base_vol >= min_ratio


# -----------------------------
# RESISTANCE LOGIC
# -----------------------------
def get_recent_high(df, lookback=50):
    """
    Returns recent swing high.
    """
    return df["high"].tail(lookback).max()


def is_near_resistance(df, resistance, threshold=0.03):
    """
    Checks if price is near resistance.
    """
    if resistance == 0:
        return False

    close = df["close"].iloc[-1]
    return abs(resistance - close) / resistance <= threshold
def volume_supports_breakout(df, lookback=5, threshold=1.2):
    """
    Checks if recent volume supports a breakout.
    Returns 1 if average recent volume > threshold × past average, else 0.
    """

    if len(df) < lookback * 2:
        return 0

    recent_vol = df["volume"].tail(lookback).mean()
    past_vol = df["volume"].iloc[-(lookback * 2):-lookback].mean()

    if past_vol == 0:
        return 0

    return int((recent_vol / past_vol) >= threshold)
def compute_resistance(df, lookback=50):
    """
    Computes recent resistance as the max high over a lookback window.
    """

    if len(df) < lookback:
        return None

    return df["high"].tail(lookback).max()


# -----------------------------
# COLORED CONSOLE OUTPUT
# -----------------------------
def print_colored_df(df):
    """
    Prints the DataFrame with color-coded columns using colorama.
    """
    try:
        from colorama import init, Fore, Style
        init(autoreset=True)
        
        # Define headers
        headers = ["rank", "symbol", "confidence", "pattern", "rule_score", "financials", "trailing_sl"]
        # Filter for existing headers only
        headers = [h for h in headers if h in df.columns]
        
        # Print Header
        header_str = " | ".join([f"{h.upper():<12}" for h in headers])
        print("\n" + Style.BRIGHT + header_str)
        print("-" * len(header_str))

        for _, row in df.iterrows():
            line = []
            for col in headers:
                val = row[col]
                text = f"{str(val):<12}"
                
                # Apply Color Logic
                if col == "confidence":
                    if val >= 0.7:
                        text = Fore.GREEN + text + Fore.RESET
                    elif val >= 0.5:
                        text = Fore.YELLOW + text + Fore.RESET
                    else:
                        text = Fore.RED + text + Fore.RESET
                
                elif col == "financials":
                    try:
                        f_score = float(val)
                        if f_score >= 0.7:
                             text = Fore.GREEN + text + Fore.RESET
                        elif f_score <= 0.3:
                             text = Fore.RED + text + Fore.RESET
                        else:
                             text = Fore.CYAN + text + Fore.RESET
                    except:
                        text = Fore.CYAN + text + Fore.RESET

                elif col == "rule_score":
                    if val >= 7:
                        text = Fore.GREEN + text + Fore.RESET
                    elif val >= 5:
                        text = Fore.YELLOW + text + Fore.RESET
                    else:
                        text = Fore.RED + text + Fore.RESET
                
                line.append(text)
            
            print(" | ".join(line))
        print("\n")

    except ImportError:
        # Fallback if colorama not installed
        print(df)
