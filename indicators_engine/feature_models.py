from market_context import MarketContext


def calculate_trend_strength(
    context: MarketContext,
) -> float:
    raise NotImplementedError


def calculate_momentum_strength(
    context: MarketContext,
) -> float:
    raise NotImplementedError


def calculate_volume_strength(
    context: MarketContext,
) -> float:
    raise NotImplementedError