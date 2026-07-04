from market_features import MarketFeatures

from feature_models.feature_result import FeatureResult

from feature_models.pipeline.measurement_pipeline import (
    MeasurementPipeline,
)

from feature_models.pipeline.builder_pipeline import (
    BuilderPipeline,
)

from feature_models.evidence_aggregator import (
    EvidenceAggregator,
)


class FeaturePipeline:
    """
    Complete Feature execution pipeline.

    Feature

        ↓

    Measurements

        ↓

    Evidences

        ↓

    FeatureResult
    """

    def __init__(self):

        self.measurements = MeasurementPipeline()

        self.builders = BuilderPipeline()

        self.aggregator = EvidenceAggregator()

    def execute(
        self,
        feature_model,
        features: MarketFeatures,
    ) -> FeatureResult:

        measurements = self.measurements.collect(
            feature_model,
            features,
        )

        evidences = self.builders.build(
            measurements,
        )

        return self.aggregator.aggregate(
            feature=feature_model.NAME,
            evidences=evidences,
        )
