"""
calculate_live_indicators.py

Main entry point for signal generation system.
This module connects everything together and returns final trading signal.
"""

from __future__ import annotations

from typing import Dict

from .multi_timeframe import multi_timeframe_analysis


async def calculate_live_indicators(
    client,
    symbol: str,
) -> Dict:
    """
    Main signal generator (ENTRY POINT).

    This function:
    - Runs multi-timeframe analysis
    - Aggregates scores
    - Returns final trading decision
    """

    try:
        # -----------------------------------------
        # Multi-Timeframe Core Analysis
        # -----------------------------------------

        result = await multi_timeframe_analysis(
            client=client,
            symbol=symbol,
        )

        # -----------------------------------------
        # Safety Defaults
        # -----------------------------------------

        if not result:
            return {
                "buy": False,
                "sell": False,
                "confidence": 0,
                "buy_score": 0,
                "sell_score": 0,
                "reason": "No data returned",
            }

        # -----------------------------------------
        # Confidence Filter (Global Safety Layer)
        # -----------------------------------------

        confidence = result.get("confidence", 0)

        # اگر خیلی ضعیف بود، معامله نکن
        if confidence < 50:
            return {
                "buy": False,
                "sell": False,
                "confidence": confidence,
                "buy_score": result.get("buy_score", 0),
                "sell_score": result.get("sell_score", 0),
                "reason": "Low confidence filter",
                "timeframes": result.get("timeframes", []),
            }

        # -----------------------------------------
        # Final Output (Clean Interface)
        # -----------------------------------------

        return {
            "buy": result.get("buy", False),
            "sell": result.get("sell", False),
            "confidence": confidence,
            "buy_score": result.get("buy_score", 0),
            "sell_score": result.get("sell_score", 0),
            "confirmations": result.get("confirmations", 0),
            "timeframes": result.get("timeframes", []),
            "status": "ACTIVE" if confidence >= 70 else "WEAK_SIGNAL",
        }

    except Exception as e:
        return {
            "buy": False,
            "sell": False,
            "confidence": 0,
            "buy_score": 0,
            "sell_score": 0,
            "error": str(e),
            "status": "ERROR",
        }
