
from market_state import MarketState

from .consensus import (
    ConsensusLevel,
    ConsensusReport,
)


class ConsensusEngine:
    """
    Measure agreement between FeatureModels.

    No trading decisions are made here.
    """

    POSITIVE_THRESHOLD = 0.65

    NEGATIVE_THRESHOLD = 0.35

    def evaluate(
        self,
        state: MarketState,
    ) -> ConsensusReport:

        supporters = []

        opponents = []

        neutral = []

        scores = []

        for feature, result in state.features.items():
            scores.append(result.score)

            if result.score >= self.POSITIVE_THRESHOLD:
                supporters.append(feature)

            elif result.score <= self.NEGATIVE_THRESHOLD:
                opponents.append(feature)

            else:
                neutral.append(feature)

        agreement = self._agreement_score(
            supporters,
            opponents,
            neutral,
        )

        level = self._consensus_level(
            agreement,
            supporters,
            opponents,
        )

        return ConsensusReport(
            level=level,
            agreement=agreement,
            supporters=supporters,
            opponents=opponents,
            neutral=neutral,
        )

    def _agreement_score(
        self,
        supporters,
        opponents,
        neutral,
    ) -> float:

        total = len(supporters) + len(opponents) + len(neutral)

        if total == 0:
            return 0.0

        dominant = max(
            len(supporters),
            len(opponents),
        )

        return dominant / total

    def _consensus_level(
        self,
        agreement: float,
        supporters,
        opponents,
    ) -> ConsensusLevel:

        if supporters and opponents:
            return ConsensusLevel.CONFLICT

        if agreement >= 0.85:
            return ConsensusLevel.STRONG

        if agreement >= 0.60:
            return ConsensusLevel.MODERATE

        return ConsensusLevel.WEAK
