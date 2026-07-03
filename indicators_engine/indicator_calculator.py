"""
Indicator Calculator
"""

import pandas as pd

from indicators import (
    ema,
    rsi,
    macd,
    atr,
    adx,
    bollinger_bands,
)


def calculate_indicators(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df["ema20"] = ema(df.close, 20)

    df["ema50"] = ema(df.close, 50)

    df["ema200"] = ema(df.close, 200)

    df["rsi"] = rsi(df.close)

    macd_line, signal_line, hist = macd(df.close)

    df["macd"] = macd_line

    df["macd_signal"] = signal_line

    df["macd_hist"] = hist

    df["atr"] = atr(
        df.high,
        df.low,
        df.close,
    )

    df["adx"] = adx(
        df.high,
        df.low,
        df.close,
    )

    upper, middle, lower = bollinger_bands(df.close)

    df["bb_upper"] = upper

    df["bb_middle"] = middle

    df["bb_lower"] = lower

    df["volume_sma"] = df.volume.rolling(20).mean()

    return df
