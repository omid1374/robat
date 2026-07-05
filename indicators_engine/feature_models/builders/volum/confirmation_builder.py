from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.measurement import Measurement


class VolumeConfirmationBuilder(
    BaseMeasurementBuilder,
):

    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        confirmed = bool(
            measurement.value,
        )

        return Evidence(

            name="volume_confirmation",

            score=1.0 if confirmed else 0.0,

            reason=(
                "Volume confirms trend"
                if confirmed
                else
                "Weak participation"
            ),

            type=EvidenceType.VALIDATION,

        )