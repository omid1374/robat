from enum import Enum
from dataclasses import dataclass

from market_features import MarketFeatures


class MarketRegime(Enum):
    TRENDING = "trending"

    RANGING = "ranging"


class VolatilityRegime(Enum):
    HIGH = "high"

    NORMAL = "normal"

    LOW = "low"


@dataclass(slots=True)
class MarketContext:
    # Composite Features
    features: MarketFeatures

    # Trend Regime
    trend: MarketRegime | None = None

    # Volatility Regime
    volatility: VolatilityRegime | None = None

    # قدرت روند
    trend_strength: float = 0.0

    # کیفیت مومنتوم
    momentum_strength: float = 0.0

    # کیفیت حجم
    volume_strength: float = 0.0


def detect_market_regime(
    adx: float,
    atr_percent: float,
) -> MarketContext:
    raise NotImplementedError
