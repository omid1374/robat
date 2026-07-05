
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
    def __init__(self):

        self.measurement_pipeline = MeasurementPipeline()

        self.builder_pipeline = BuilderPipeline()

        self.aggregator = EvidenceAggregator()

    def execute(
        self,
        feature_model,
        features,
    ):

        measurements = self.measurement_pipeline.collect(
            feature_model,
            features,
        )

        evidences = self.builder_pipeline.build(
            measurements,
        )

        return self.aggregator.aggregate(
            feature=feature_model.NAME,
            evidences=evidences,
        )
