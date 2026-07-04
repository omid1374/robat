from feature_models.evidence import (
    Evidence,
    EvidenceType,
)


class EvidenceFactory:
    """
    Central place for creating Evidence objects.

    Keeps Builders lightweight.
    """

    def create(
        self,
        *,
        name: str,
        score: float,
        reason: str,
        evidence_type: EvidenceType,
    ) -> Evidence:

        return Evidence(
            name=name,
            score=score,
            reason=reason,
            type=evidence_type,
        )
