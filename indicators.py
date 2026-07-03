"""
indicators.py
اندیکاتورها و محاسبات آماری ربات
"""

from collections import deque
import numpy as np
import pandas as pd

# -----------------------------
# تاریخچه قیمت و معاملات
# -----------------------------

mid_history = deque(maxlen=500)
trade_history = deque(maxlen=5000)
recent_volumes = deque(maxlen=1000)


# -----------------------------
# Mid Price
# -----------------------------
def get_mid_price(orderbook):

    bid = orderbook["bids"][0][0]
    ask = orderbook["asks"][0][0]

    return (bid + ask) / 2, bid, ask


# -----------------------------
# Volatility
# -----------------------------
def get_volatility(window=50):

    if len(mid_history) < window:
        return 0.0

    prices = list(mid_history)[-window:]

    return float(np.std(prices))


# -----------------------------
# Order Book Imbalance
# -----------------------------
def order_imbalance(orderbook, depth=5):

    bid_volume = sum(x[1] for x in orderbook["bids"][:depth])
    ask_volume = sum(x[1] for x in orderbook["asks"][:depth])

    total = bid_volume + ask_volume

    if total == 0:
        return 0.0

    return (bid_volume - ask_volume) / total


# -----------------------------
# EMA
# -----------------------------
def calculate_ema(closes, period=200):

    if len(closes) < period:
        return None

    s = pd.Series(closes)

    return float(s.ewm(span=period, adjust=False).mean().iloc[-1])


# -----------------------------
# ATR
# -----------------------------
def calculate_atr(df, period=20):

    if len(df) < period + 1:
        return None

    high_low = df["high"] - df["low"]

    high_close = (df["high"] - df["close"].shift()).abs()

    low_close = (df["low"] - df["close"].shift()).abs()

    tr = pd.concat(
        [
            high_low,
            high_close,
            low_close,
        ],
        axis=1,
    ).max(axis=1)

    atr = tr.rolling(period).mean()

    return float(atr.iloc[-1])


# -----------------------------
# EMA + ATR
# -----------------------------
def calculate_market_state(ohlcv):

    df = pd.DataFrame(
        ohlcv,
        columns=[
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
    )

    ema = calculate_ema(df["close"].tolist())

    atr = calculate_atr(df)

    return ema, atr


# -----------------------------
# VPIN
# -----------------------------
def compute_vpin(bucket_size=5000):

    if len(trade_history) == 0:
        return None

    buy_volume = 0.0
    sell_volume = 0.0
    bucket_volume = 0.0

    values = []

    for trade in list(trade_history):
        amount = float(trade.get("amount", 0))

        side = trade.get("side", "buy")

        bucket_volume += amount

        if side == "buy":
            buy_volume += amount
        else:
            sell_volume += amount

        if bucket_volume >= bucket_size:
            values.append(abs(buy_volume - sell_volume) / bucket_size)

            buy_volume = 0.0
            sell_volume = 0.0
            bucket_volume = 0.0

    if len(values) == 0:
        return None

    return float(np.mean(values))


# -----------------------------
# Pricing Model
# -----------------------------
def compute_quotes(
    mid,
    inventory,
    volatility,
    imbalance,
    vpin,
    base_spread,
    k_vol,
    k_inv,
):

    toxicity = 1 + vpin if vpin else 1

    spread = (base_spread + (volatility * k_vol)) * toxicity

    adjusted_mid = mid + imbalance * spread * 0.5

    inventory_skew = inventory * k_inv

    bid = adjusted_mid - spread / 2 - inventory_skew

    ask = adjusted_mid + spread / 2 - inventory_skew

    return bid, ask, spread
