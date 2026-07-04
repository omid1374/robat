from dataclasses import dataclass

from .feature_type import FeatureType


@dataclass(slots=True)
class FeatureResult:
    """
    Final output of one FeatureModel.
    """

    feature: FeatureType

    score: float

    confidence: float

    evidences: int

    reasons: list[str]
