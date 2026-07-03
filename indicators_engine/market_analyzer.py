"""
market_analyzer.py

Analyze current market regime.
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


def analyze_market(df: pd.DataFrame) -> Dict:

    last = df.iloc[-1]

    previous = df.iloc[-2]

    trend = "sideways"

    trend_strength = "weak"

    volatility = "normal"

    momentum = "neutral"

    volume_state = "normal"

    breakout = False

    # -------------------------------------
    # Trend Detection
    # -------------------------------------

    if last["ema20"] > last["ema50"] > last["ema200"]:
        trend = "bullish"

    elif last["ema20"] < last["ema50"] < last["ema200"]:
        trend = "bearish"

    # -------------------------------------
    # Trend Strength
    # -------------------------------------

    adx = float(last["adx"])

    if adx >= 35:
        trend_strength = "very_strong"

    elif adx >= 25:
        trend_strength = "strong"

    elif adx >= 18:
        trend_strength = "medium"

    else:
        trend_strength = "weak"

    # -------------------------------------
    # Momentum
    # -------------------------------------

    if last["macd"] > last["macd_signal"]:
        momentum = "bullish"

    elif last["macd"] < last["macd_signal"]:
        momentum = "bearish"

    # -------------------------------------
    # Volatility
    # -------------------------------------

    atr_avg = df["atr"].tail(30).mean()

    if last["atr"] > atr_avg * 1.5:
        volatility = "high"

    elif last["atr"] < atr_avg * 0.7:
        volatility = "low"

    # -------------------------------------
    # Volume
    # -------------------------------------

    if last["volume"] > last["volume_sma"] * 1.5:
        volume_state = "high"

    elif last["volume"] < last["volume_sma"] * 0.7:
        volume_state = "low"

    # -------------------------------------
    # Breakout
    # -------------------------------------

    if previous["close"] <= previous["bb_upper"] and last["close"] > last["bb_upper"]:
        breakout = True

    if previous["close"] >= previous["bb_lower"] and last["close"] < last["bb_lower"]:
        breakout = True

    return {
        "trend": trend,
        "trend_strength": trend_strength,
        "momentum": momentum,
        "volatility": volatility,
        "volume": volume_state,
        "breakout": breakout,
        "adx": round(float(last["adx"]), 2),
        "atr": round(float(last["atr"]), 4),
        "rsi": round(float(last["rsi"]), 2),
        "close": round(float(last["close"]), 6),
    }
