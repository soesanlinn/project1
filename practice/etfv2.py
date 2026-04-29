import requests
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

# =========================
# CONFIG
# =========================
TWELVE_DATA_API_KEY = "f34faf118ba747e8bc60ae0e766f975d"
API_NINJAS_KEY = "1VWATDcQTEmCKH8nwGLMWhR64oVewuAgO3kPC6AB"

MAX_ETFS = 500   # increase gradually (API limits!)
SLEEP = 0.5      # avoid rate limits

# =========================
# STEP 1 — GET ETF LIST
# =========================
def get_etf_list():
    url = f"https://api.twelvedata.com/etfs?apikey={TWELVE_DATA_API_KEY}"
    r = requests.get(url)
    data = r.json()

    if "data" not in data:
        raise Exception("Failed to fetch ETF list")

    symbols = [etf["symbol"] for etf in data["data"]]
    return symbols[:MAX_ETFS]

# =========================
# STEP 2 — FUNDAMENTALS
# =========================
def get_fundamentals(symbol):
    url = f"https://api.api-ninjas.com/v1/etf?ticker={symbol}"
    headers = {"X-Api-Key": API_NINJAS_KEY}

    try:
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            return None

        data = r.json()
        if not data:
            return None

        d = data[0]

        return {
            "expense_ratio": d.get("expense_ratio"),
            "dividend_yield": d.get("dividend_yield"),
            "sector": d.get("category", "Unknown")
        }
    except:
        return None

# =========================
# STEP 3 — PRICE HISTORY
# =========================
def get_price_history(symbol):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "1month",
        "outputsize": 5000,
        "apikey": TWELVE_DATA_API_KEY
    }

    try:
        r = requests.get(url, params=params)
        data = r.json()

        if "values" not in data:
            return None

        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["close"] = df["close"].astype(float)

        df = df.sort_values("datetime")
        df.set_index("datetime", inplace=True)

        return df
    except:
        return None

# =========================
# STEP 4 — RETURNS
# =========================
def annualized_return(df, years):
    months = years * 12
    if len(df) < months:
        return None

    start_price = df["close"].iloc[-months]
    end_price = df["close"].iloc[-1]

    if start_price <= 0:
        return None

    return (end_price / start_price) ** (1 / years) - 1


def compute_returns(df):
    return {
        "1y_return": annualized_return(df, 1),
        "5y_return": annualized_return(df, 5),
        "10y_return": annualized_return(df, 10),
    }

# =========================
# MAIN PIPELINE
# =========================
def main():
    symbols = get_etf_list()

    results = []

    for symbol in tqdm(symbols):
        try:
            fundamentals = get_fundamentals(symbol)
            if not fundamentals:
                continue

            prices = get_price_history(symbol)
            if prices is None or len(prices) < 120:
                continue

            returns = compute_returns(prices)

            results.append({
                "symbol": symbol,
                "expense_ratio": fundamentals["expense_ratio"],
                "dividend_yield": fundamentals["dividend_yield"],
                "sector": fundamentals["sector"],
                "1y_return": returns["1y_return"],
                "5y_return": returns["5y_return"],
                "10y_return": returns["10y_return"],
            })

            time.sleep(SLEEP)

        except Exception as e:
            print(f"Error with {symbol}: {e}")
            continue

    df = pd.DataFrame(results)

    # Save full dataset
    df.to_csv("all_etfs.csv", index=False)

    # =========================
    # BEST ETFs BY SECTOR
    # =========================
    best_by_sector = (
        df.dropna(subset=["10y_return"])
          .sort_values("10y_return", ascending=False)
          .groupby("sector")
          .head(5)
    )

    best_by_sector.to_csv("/Users/ssl/Dropbox/best_etfs_by_sector.csv", index=False)

    print("\nTop ETFs by sector (10Y returns):")
    print(best_by_sector.head(20))


if __name__ == "__main__":
    main()