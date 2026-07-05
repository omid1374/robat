from dataclasses import dataclass


@dataclass(
    slots=True,
    frozen=True,
)
class MarketContext:

    trend_score: float

    momentum_score: float

    volume_score: float

    volatility_score: float