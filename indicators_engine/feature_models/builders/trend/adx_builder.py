from feature_models.measurement import Measurement

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)

from feature_models.normalizers.registry import (
    NormalizerRegistry,
)


class ADXBuilder(
    BaseMeasurementBuilder,
):
    def __init__(self):

        self.normalizers = NormalizerRegistry()

    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        normalizer = self.normalizers.resolve(
            measurement.type,
        )

        score = normalizer.normalize(
            measurement,
        )

        return Evidence(
            name="trend_persistence",
            score=score,
            reason=f"ADX={measurement.value:.1f}",
            type=EvidenceType.CONFIRMATION,
        )
