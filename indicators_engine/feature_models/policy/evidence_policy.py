from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from .base_policy import BaseEvidencePolicy


class DefaultEvidencePolicy(
    BaseEvidencePolicy,
):
    """
    Default weighting policy.

    Later we can have:

    CryptoPolicy

    ForexPolicy

    TrendPolicy

    RangePolicy
    """

    WEIGHTS = {
        EvidenceType.VALIDATION: 0.50,
        EvidenceType.CONFIRMATION: 0.30,
        EvidenceType.QUALITY: 0.20,
    }

    def weight(
        self,
        evidence: Evidence,
    ) -> float:

        return self.WEIGHTS.get(
            evidence.type,
            0.0,
        )

    def confidence(
        self,
        evidences: list[Evidence],
    ) -> float:

        if not evidences:
            return 0.0

        weighted = 0.0

        total = 0.0

        for evidence in evidences:
            w = self.weight(
                evidence,
            )

            weighted += evidence.score * w

            total += w

        if total == 0:
            return 0.0

        return weighted / total
