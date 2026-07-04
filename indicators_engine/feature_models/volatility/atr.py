from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import VolatilityFactor


class ATRQuality(
    VolatilityFactor,
):

    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        score = 1.0 - self._normalize(
            features.atr_percent,
            0.5,
            5.0,
        )

        return Evidence(
            name="atr_quality",
            score=score,
            reason=f"ATR={features.atr_percent:.2%}",
            type=EvidenceType.QUALITY,
        )

    def _normalize(
        self,
        value,
        minimum,
        maximum,
    ):

        score = (
            value - minimum
        ) / (
            maximum - minimum
        )

        return max(
            0,
            min(
                score,
                1,
            ),
        )