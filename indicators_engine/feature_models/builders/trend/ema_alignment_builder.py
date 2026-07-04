from feature_models.measurement import Measurement

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)


class EMAAlignmentBuilder(
    BaseMeasurementBuilder,
):
    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        aligned = measurement.value >= 1.0

        return Evidence(
            name="trend_structure",
            score=1.0 if aligned else 0.0,
            reason=("EMA aligned" if aligned else "EMA misaligned"),
            type=EvidenceType.VALIDATION,
        )
