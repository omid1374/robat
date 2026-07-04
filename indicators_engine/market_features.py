from dataclasses import dataclass
import pandas as pd


from enum import Enum


class TrendDirection(Enum):
    BULLISH = "bullish"

    BEARISH = "bearish"

    NEUTRAL = "neutral"


class MomentumDirection(Enum):
    BULLISH = "bullish"

    BEARISH = "bearish"

    NEUTRAL = "neutral"


@dataclass(slots=True)
class MarketFeatures:
    timeframe: str

    # ===== Price =====
    close: float

    # ===== Trend =====
    ema20: float
    ema50: float
    ema200: float

    # ===== Momentum =====
    rsi: float
    macd: float
    macd_signal: float
    macd_hist: float

    # ===== Trend Strength =====
    adx: float

    # ===== Volatility =====
    atr: float
    atr_percent: float

    # ===== Volume =====
    volume: float
    volume_sma: float
    volume_ratio: float

    # ===== Bollinger =====
    bb_upper: float
    bb_middle: float
    bb_lower: float


def extract_market_features(
    df: pd.DataFrame,
    timeframe: str,
) -> MarketFeatures:
    """
    Convert indicator DataFrame into MarketFeatures.
    """

    row = df.iloc[-2]

    return MarketFeatures(
        timeframe=timeframe,
        close=float(row["close"]),
        ema20=float(row["ema20"]),
        ema50=float(row["ema50"]),
        ema200=float(row["ema200"]),
        rsi=float(row["rsi"]),
        macd=float(row["macd"]),
        macd_signal=float(row["macd_signal"]),
        macd_hist=float(row["macd_hist"]),
        adx=float(row["adx"]),
        atr=float(row["atr"]),
        atr_percent=float(row["atr"] / row["close"] * 100),
        volume=float(row["volume"]),
        volume_sma=float(row["volume_sma"]),
        volume_ratio=float(row["volume"] / row["volume_sma"]),
        bb_upper=float(row["bb_upper"]),
        bb_middle=float(row["bb_middle"]),
        bb_lower=float(row["bb_lower"]),
    )
