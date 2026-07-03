"""
signal_scoring.py

Professional weighted signal scoring engine.
"""

from __future__ import annotations

from typing import Dict, List

from .weights import *


def _clamp(score: int) -> int:
    """Limit score to valid range."""
    return max(0, min(MAX_SCORE, score))


def score_signal(market: Dict) -> Dict:
    """
    Generate BUY / SELL scores from analyzed market data.
    """

    buy_score = 0
    sell_score = 0

    buy_reasons: List[str] = []
    sell_reasons: List[str] = []

    # =====================================================
    # TREND
    # =====================================================

    if market["trend"] == "bullish":
        buy_score += BULLISH_TREND

        buy_reasons.append("Bullish Trend")

    elif market["trend"] == "bearish":
        sell_score += BEARISH_TREND

        sell_reasons.append("Bearish Trend")

    else:
        buy_score += RANGING_MARKET_PENALTY
        sell_score += RANGING_MARKET_PENALTY

    # =====================================================
    # TREND STRENGTH
    # =====================================================

    strength = market["trend_strength"]

    if strength == "very_strong":
        buy_score += VERY_STRONG_TREND
        sell_score += VERY_STRONG_TREND

        buy_reasons.append("Very Strong Trend")
        sell_reasons.append("Very Strong Trend")

    elif strength == "strong":
        buy_score += STRONG_TREND
        sell_score += STRONG_TREND

    elif strength == "medium":
        buy_score += MEDIUM_TREND
        sell_score += MEDIUM_TREND

    else:
        buy_score += WEAK_TREND
        sell_score += WEAK_TREND

    # =====================================================
    # MOMENTUM
    # =====================================================

    if market["momentum"] == "bullish":
        buy_score += BULLISH_MOMENTUM

        buy_reasons.append("Bullish Momentum")

    elif market["momentum"] == "bearish":
        sell_score += BEARISH_MOMENTUM

        sell_reasons.append("Bearish Momentum")

    # =====================================================
    # RSI
    # =====================================================

    rsi = market["rsi"]

    if RSI_BULL_MIN <= rsi <= RSI_BULL_MAX:
        buy_score += HEALTHY_RSI

        buy_reasons.append(f"RSI {rsi}")

    elif RSI_BEAR_MIN <= rsi <= RSI_BEAR_MAX:
        sell_score += WEAK_RSI

        sell_reasons.append(f"RSI {rsi}")

    elif rsi >= RSI_OVERBOUGHT:
        sell_score += OVERBOUGHT

        sell_reasons.append("Overbought")

    elif rsi <= RSI_OVERSOLD:
        buy_score += OVERSOLD

        buy_reasons.append("Oversold")

    # =====================================================
    # BREAKOUT
    # =====================================================

    if market["breakout"]:
        if market["trend"] == "bullish":
            buy_score += BREAKOUT_SCORE

            buy_reasons.append("Bullish Breakout")

        elif market["trend"] == "bearish":
            sell_score += BREAKOUT_SCORE

            sell_reasons.append("Bearish Breakout")

    # =====================================================
    # VOLUME
    # =====================================================

    if market["volume"] == "high":
        buy_score += HIGH_VOLUME
        sell_score += HIGH_VOLUME

        buy_score += HIGH_VOLUME_BONUS
        sell_score += HIGH_VOLUME_BONUS

        buy_reasons.append("High Volume")
        sell_reasons.append("High Volume")

    elif market["volume"] == "low":
        buy_score += LOW_VOLUME
        sell_score += LOW_VOLUME

        buy_score += LOW_VOLUME_PENALTY
        sell_score += LOW_VOLUME_PENALTY

    # =====================================================
    # VOLATILITY
    # =====================================================

    if market["volatility"] == "high":
        buy_score += HIGH_VOLATILITY
        sell_score += HIGH_VOLATILITY

        buy_score += EXTREME_VOLATILITY_PENALTY
        sell_score += EXTREME_VOLATILITY_PENALTY

    elif market["volatility"] == "low":
        buy_score += LOW_VOLATILITY
        sell_score += LOW_VOLATILITY

    # =====================================================
    # EMA ALIGNMENT BONUS
    # =====================================================

    if market["trend"] in ("bullish", "bearish"):
        buy_score += EMA_ALIGNMENT_BONUS
        sell_score += EMA_ALIGNMENT_BONUS

    # =====================================================
    # ADX BONUS
    # =====================================================

    if market["adx"] >= ADX_STRONG:
        buy_score += STRONG_ADX_BONUS
        sell_score += STRONG_ADX_BONUS

    # =====================================================
    # CONFIDENCE
    # =====================================================

    buy_score = _clamp(buy_score)
    sell_score = _clamp(sell_score)

    buy_signal = buy_score >= BUY_THRESHOLD and buy_score > sell_score

    sell_signal = sell_score >= SELL_THRESHOLD and sell_score > buy_score

    confidence = max(
        buy_score,
        sell_score,
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {
        "buy": buy_signal,
        "sell": sell_signal,
        "buy_score": buy_score,
        "sell_score": sell_score,
        "confidence": confidence,
        "buy_reasons": buy_reasons,
        "sell_reasons": sell_reasons,
    }
