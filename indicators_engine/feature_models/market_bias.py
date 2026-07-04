from dataclasses import dataclass
from enum import Enum


class BiasDirection(Enum):

    LONG = "long"

    SHORT = "short"

    NEUTRAL = "neutral"


@dataclass(slots=True)
class MarketBias:
    """
    High-level interpretation
    of the current market.
    """

    direction: BiasDirection

    confidence: float

    explanation: str