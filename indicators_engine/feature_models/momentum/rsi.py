from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import MomentumFactor


class RSIStrength(
    MomentumFactor,
):
    """
    Evaluate RSI quality.

    Healthy bullish trends usually keep RSI
    between 55 and 70.

    Healthy bearish trends usually keep RSI
    between 30 and 45.
    """

    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        bullish = features.ema20 > features.ema50 > features.ema200

        bearish = features.ema20 < features.ema50 < features.ema200

        if bullish:
            score = 1.0 - self._normalize(
                abs(features.rsi - 62),
                0,
                25,
            )

        elif bearish:
            score = 1.0 - self._normalize(
                abs(features.rsi - 38),
                0,
                25,
            )

        else:
            score = 0.50

        return Evidence(
            name="rsi_strength",
            score=score,
            reason=f"RSI={features.rsi:.1f}",
            type=EvidenceType.QUALITY,
        )

    def _normalize(
        self,
        value,
        minimum,
        maximum,
    ):

        score = (value - minimum) / (maximum - minimum)

        return max(
            0.0,
            min(score, 1.0),
        )
