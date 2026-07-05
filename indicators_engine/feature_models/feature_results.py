from dataclasses import dataclass

from feature_models.feature_result import (
    FeatureResult,
)


@dataclass(slots=True)
class FeatureResults:

    results: dict[str, FeatureResult]

    def get(
        self,
        name: str,
    ) -> FeatureResult:

        return self.results[name]