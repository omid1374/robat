from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import VolumeFactor


class VolumeConfirmation(
    VolumeFactor,
):
    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        bullish = features.ema20 > features.ema50 > features.ema200

        bearish = features.ema20 < features.ema50 < features.ema200

        high_volume = features.volume_ratio >= 1.2

        confirmed = (bullish or bearish) and high_volume

        return Evidence(
            name="volume_confirmation",
            score=1.0 if confirmed else 0.0,
            reason="Volume confirms trend" if confirmed else "Weak participation",
            type=EvidenceType.VALIDATION,
        )
