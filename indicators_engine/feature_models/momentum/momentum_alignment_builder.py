from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.measurement import Measurement


class MomentumAlignmentBuilder(
    BaseMeasurementBuilder,
):

    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        aligned = bool(measurement.value)

        return Evidence(

            name="momentum_alignment",

            score=1.0 if aligned else 0.0,

            reason=(
                "Momentum aligned"
                if aligned
                else
                "Momentum conflict"
            ),

            type=EvidenceType.CONFIRMATION,

        )