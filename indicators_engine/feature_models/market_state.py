from dataclasses import dataclass
from .feature_result import FeatureResult
from .feature_type import FeatureType
from .consensus import ConsensusReport



@dataclass(slots=True)
class MarketState:
    """
    Unified snapshot of the market.

    Produced after evaluating all FeatureModels.
    """

    features: dict[FeatureType, FeatureResult]
    consensus: ConsensusReport | None = None