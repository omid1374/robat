from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import VolumeFactor


class VolumeExpansion(
    VolumeFactor,
):
    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        score = self._normalize(
            features.volume_ratio,
            1.0,
            3.0,
        )

        return Evidence(
            name="volume_expansion",
            score=score,
            reason=f"Expansion={features.volume_ratio:.2f}",
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
