from market_features import MarketFeatures

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_factor import MomentumFactor


class MomentumAlignment(
    MomentumFactor,
):
    def evaluate(
        self,
        features: MarketFeatures,
    ) -> Evidence:

        bullish = features.ema20 > features.ema50 > features.ema200

        bearish = features.ema20 < features.ema50 < features.ema200

        if bullish:
            aligned = features.macd > 0 and features.rsi > 50

        elif bearish:
            aligned = features.macd < 0 and features.rsi < 50

        else:
            aligned = False

        return Evidence(
            name="momentum_alignment",
            score=1.0 if aligned else 0.0,
            reason="Momentum aligned" if aligned else "Momentum conflict",
            type=EvidenceType.VALIDATION,
        )
