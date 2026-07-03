"""
Fetch market data from exchange.
"""

from typing import Dict

import pandas as pd


async def fetch_market_data(
    client,
    symbol: str,
    timeframe: str = "5m",
    limit: int = 300,
) -> pd.DataFrame:
    """
    Download OHLCV data and convert to DataFrame.
    """

    candles = await client.fetch_ohlcv(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit,
    )

    df = pd.DataFrame(
        candles,
        columns=[
            "timestamp",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ],
    )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        unit="ms",
    )

    df = df.astype(
        {
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": float,
        }
    )

    return df
