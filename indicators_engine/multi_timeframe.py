"""
multi_timeframe.py

Weighted Multi-Timeframe analysis engine.
"""

from __future__ import annotations

from typing import Dict, List

from .weights import TIMEFRAMES
from .fetch_market_data import fetch_market_data
from .indicator_calculator import calculate_indicators
from .market_analyzer import analyze_market
from .signal_scoring import score_signal


# ------------------------------------------------------------
# Helper
# ------------------------------------------------------------


def _get_tf_weight(tf: str) -> float:
    """
    Get weight of timeframe from weights.py
    """

    tf_map = getattr(
        __import__("indicators_engine.weights", fromlist=["*"]),
        "TIMEFRAME_WEIGHTS",
        None,
    )

    # fallback if not defined as dict
    if isinstance(tf_map, dict):
        return tf_map.get(tf, 1)

    # default equal weight
    return 1.0


# ------------------------------------------------------------
# Main Engine
# ------------------------------------------------------------


async def multi_timeframe_analysis(
    client,
    symbol: str,
) -> Dict:
    """
    Run full analysis across multiple timeframes.
    """

    results: List[Dict] = []

    weighted_buy = 0.0
    weighted_sell = 0.0
    total_weight = 0.0

    tf_details = []

    # --------------------------------------------------------
    # Loop Timeframes
    # --------------------------------------------------------

    for tf in TIMEFRAMES:
        try:
            # 1. Market Data
            df = await fetch_market_data(
                client=client,
                symbol=symbol,
                timeframe=tf,
            )

            # 2. Indicators
            df = calculate_indicators(df)

            # 3. Market Regime
            market = analyze_market(df)

            # 4. Score Signal
            score = score_signal(market)

            weight = _get_tf_weight(tf)

            total_weight += weight

            weighted_buy += score["buy_score"] * weight

            weighted_sell += score["sell_score"] * weight

            tf_details.append(
                {
                    "timeframe": tf,
                    "weight": weight,
                    "buy_score": score["buy_score"],
                    "sell_score": score["sell_score"],
                    "buy": score["buy"],
                    "sell": score["sell"],
                    "market": market,
                }
            )

        except Exception as e:
            tf_details.append(
                {
                    "timeframe": tf,
                    "error": str(e),
                }
            )

    # --------------------------------------------------------
    # Final Score Calculation
    # --------------------------------------------------------

    if total_weight == 0:
        return {
            "buy": False,
            "sell": False,
            "confidence": 0,
            "timeframes": tf_details,
        }

    final_buy = weighted_buy / total_weight
    final_sell = weighted_sell / total_weight

    buy_signal = final_buy > final_sell
    sell_signal = final_sell > final_buy

    confidence = max(final_buy, final_sell)

    # --------------------------------------------------------
    # Confirmation logic
    # --------------------------------------------------------

    confirmations = 0

    for tf in tf_details:
        if tf.get("buy"):
            confirmations += 1

    # --------------------------------------------------------
    # Final Decision Filter
    # --------------------------------------------------------

    if confirmations < 2:
        buy_signal = False
        sell_signal = False

    return {
        "buy": buy_signal,
        "sell": sell_signal,
        "confidence": round(confidence, 2),
        "buy_score": round(final_buy, 2),
        "sell_score": round(final_sell, 2),
        "confirmations": confirmations,
        "timeframes": tf_details,
    }
