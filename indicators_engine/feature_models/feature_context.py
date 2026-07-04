from dataclasses import dataclass


@dataclass(slots=True)
class FeatureContext:
    symbol: str

    timeframe: str

    market_regime: str = "unknown"

    session: str = "unknown"

    asset_class: str = "unknown"
