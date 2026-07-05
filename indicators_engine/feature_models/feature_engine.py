from market_features import MarketFeatures

from feature_models.builders.registry import (
    BuilderRegistry,
)

from feature_models.feature_registry import (
    FeatureRegistry,
)

from feature_models.feature_result import (
    FeatureResult,
)

from feature_models.feature_results import (
    FeatureResults,
)


class FeatureEngine:

    def __init__(self):

        self.features = FeatureRegistry()

        self.builders = BuilderRegistry()

    def execute(

        self,

        market: MarketFeatures,

    ) -> FeatureResults:

        results = {}

        for feature in self.features.get_features():

            measurements = feature.measure(
                market,
            )

            evidences = []

            for measurement in measurements:

                builder = self.builders.resolve(
                    measurement.type,
                )

                evidences.append(

                    builder.build(
                        measurement,
                    )

                )

            results[feature.NAME.value] = FeatureResult(

                name=feature.NAME.value,

                evidences=evidences,

            )

        return FeatureResults(

            results=results,

        )