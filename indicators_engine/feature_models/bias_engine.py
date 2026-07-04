from market_state import MarketState

from .market_bias import (
    MarketBias,
    BiasDirection,
)

from .consensus import (
    ConsensusLevel,
)


class BiasEngine:
    """
    Convert MarketState into
    a high-level market bias.
    """

    def evaluate(
        self,
        state: MarketState,
    ) -> MarketBias:

        trend = state.features.get(state.features.keys().__iter__().__next__())

        if trend is None:
            return MarketBias(
                direction=BiasDirection.NEUTRAL,
                confidence=0.0,
                explanation="No trend feature.",
            )

        score = trend.score

        consensus = state.consensus

        if score >= 0.65 and consensus.level == ConsensusLevel.STRONG:
            return MarketBias(
                direction=BiasDirection.LONG,
                confidence=score,
                explanation="Strong bullish consensus.",
            )

        if score <= 0.35 and consensus.level == ConsensusLevel.STRONG:
            return MarketBias(
                direction=BiasDirection.SHORT,
                confidence=1.0 - score,
                explanation="Strong bearish consensus.",
            )

        return MarketBias(
            direction=BiasDirection.NEUTRAL,
            confidence=0.50,
            explanation="No clear bias.",
        )
