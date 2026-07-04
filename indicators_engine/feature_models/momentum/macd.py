from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import MomentumFactor


class MACDStrength(
    MomentumFactor,
):
    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        diff = abs(features.macd - features.macd_signal)

        score = self._normalize(
            diff,
            0,
            2,
        )

        if features.macd_hist < 0:
            score *= 0.60

        return Evidence(
            name="macd_strength",
            score=score,
            reason=f"Hist={features.macd_hist:.2f}",
            type=EvidenceType.CONFIRMATION,
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
