from abc import ABC
from abc import abstractmethod
from .evidence import (
    EvidenceType,
)
from market_features import MarketFeatures

from .evidence import Evidence


class BaseFeature(ABC):
    """
    Shared execution flow for every FeatureModel.
    """

    def evaluate(
        self,
        features: MarketFeatures,
    ) -> list[Evidence]:

        evidences = self.build_evidences(
            features,
        )

        self.validate_evidences(
            evidences,
        )

        return evidences

    @abstractmethod
    def build_evidences(
        self,
        features: MarketFeatures,
    ) -> list[Evidence]:
        """
        Produce evidences describing one market dimension.
        """

    def validate_evidences(
        self,
        evidences: list[Evidence],
    ) -> None:

        if not evidences:
            raise ValueError(f"{self.__class__.__name__} returned no evidences.")

        for evidence in evidences:
            if not 0.0 <= evidence.score <= 1.0:
                raise ValueError(f"Evidence score out of range: {evidence.name}")

    def _evidence(
        self,
        *,
        name: str,
        score: float,
        reason: str,
        evidence_type: EvidenceType,
    ) -> Evidence:

        return Evidence(
            name=name,
            score=max(
                0.0,
                min(
                    score,
                    1.0,
                ),
            ),
            reason=reason,
            type=evidence_type,
        )
