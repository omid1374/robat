from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.measurement import Measurement


class VolumeParticipationBuilder(
    BaseMeasurementBuilder,
):

    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        ratio = measurement.value

        score = max(
            0.0,
            min(
                (ratio - 0.7) / (2.0 - 0.7),
                1.0,
            ),
        )

        return Evidence(

            name="volume_participation",

            score=score,

            reason=f"Volume Ratio={ratio:.2f}",

            type=EvidenceType.QUALITY,

        )