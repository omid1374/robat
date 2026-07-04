from market_features import MarketFeatures

from .feature_model import FeatureModel
from .feature_result import FeatureResult
from .evidence_aggregator import EvidenceAggregator
from market_state import MarketState
from .consensus_engine import ConsensusEngine
from .evidence_aggregator import (
    EvidenceAggregator,
)

class FeatureEngine:
    """
    Execute every FeatureModel and
    convert evidences into FeatureResults.
    """

    def __init__(
        self,
        models: list[FeatureModel],
    ):

        self.models = models
        self.aggregator = EvidenceAggregator()
        self.aggregator = EvidenceAggregator()
        self.consensus_engine = ConsensusEngine()

    def evaluate(
        self,
        features: MarketFeatures,
    ) -> MarketState:

        results = []

        for model in self.models:

            evidences = model.evaluate(
                features,
            )

            result = self.aggregator.aggregate(
                feature=model.NAME,
                evidences=evidences,
            )

            results.append(
                result,
            )

        feature_map = {result.feature: result for result in results}

        state = MarketState(
            features=feature_map,
        )

        state.consensus = self.consensus_engine.evaluate(
            state,
        )

        return state
