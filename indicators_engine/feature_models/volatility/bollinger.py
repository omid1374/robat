from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import VolatilityFactor


class BollingerQuality(
    VolatilityFactor,
):

    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        width = (
            features.bb_upper -
            features.bb_lower
        )

        score = self._normalize(
            width /
            features.close,
            0.01,
            0.15,
        )

        return Evidence(
            name="bollinger_width",
            score=score,
            reason=f"Width={width:.2f}",
            type=EvidenceType.CONFIRMATION,
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