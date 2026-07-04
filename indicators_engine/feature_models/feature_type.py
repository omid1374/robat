from enum import Enum


class FeatureType(Enum):
    """
    Canonical feature identifiers.

    Every FeatureModel must expose one
    of these identifiers.
    """

    TREND = "trend"

    MOMENTUM = "momentum"

    VOLUME = "volume"

    VOLATILITY = "volatility"

    LIQUIDITY = "liquidity"

    STRUCTURE = "structure"
