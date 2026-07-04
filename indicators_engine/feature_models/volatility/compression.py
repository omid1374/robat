from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import VolatilityFactor


class CompressionQuality(
    VolatilityFactor,
):

    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        compressed = (
            features.atr_percent <
            0.015
        )

        return Evidence(
            name="compression",
            score=1.0 if compressed else 0.0,
            reason="Compression"
            if compressed
            else "Normal",
            type=EvidenceType.VALIDATION,
        )