from dataclasses import dataclass

from feature_models.evidence import Evidence


@dataclass(slots=True)
class FeatureResult:

    name: str

    evidences: list[Evidence]