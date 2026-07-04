from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import VolumeFactor


class VolumeParticipation(
    VolumeFactor,
):
    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        ratio = features.volume_ratio

        score = self._normalize(
            ratio,
            0.7,
            2.0,
        )

        return Evidence(
            name="volume_participation",
            score=score,
            reason=f"Volume Ratio={ratio:.2f}",
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
