from dataclasses import dataclass
from enum import Enum

from feature_models.feature_type import FeatureType


class ConsensusLevel(Enum):
    STRONG = "strong"

    MODERATE = "moderate"

    WEAK = "weak"

    CONFLICT = "conflict"


@dataclass(slots=True)
class ConsensusReport:
    """
    Summary of agreement between all FeatureModels.
    """

    level: ConsensusLevel

    agreement: float

    supporters: list[FeatureType]

    opponents: list[FeatureType]

    neutral: list[FeatureType]