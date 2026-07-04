from feature_models.feature_result import FeatureResult
from feature_models.feature_type import FeatureType

from feature_models.evidence import Evidence

from .policy.evidence_policy import (
    DefaultEvidencePolicy,
)


class EvidenceAggregator:
    def __init__(self):

        self.policy = DefaultEvidencePolicy()

    def aggregate(
        self,
        feature: FeatureType,
        evidences: list[Evidence],
    ) -> FeatureResult:

        score = self._score(
            evidences,
        )

        confidence = self.policy.confidence(
            evidences,
        )

        return FeatureResult(
            feature=feature,
            score=score,
            confidence=confidence,
            evidences=len(evidences),
            reasons=[e.reason for e in evidences],
        )

    def _score(
        self,
        evidences,
    ):

        weighted = 0.0

        total = 0.0

        for evidence in evidences:
            weight = self.policy.weight(
                evidence,
            )

            weighted += evidence.score * weight

            total += weight

        if total == 0:
            return 0.0

        return weighted / total
