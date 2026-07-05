from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.measurement import Measurement


class VolumeExpansionBuilder(
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
                (ratio - 1.0) / (3.0 - 1.0),
                1.0,
            ),
        )

        return Evidence(

            name="volume_expansion",

            score=score,

            reason=f"Expansion={ratio:.2f}",

            type=EvidenceType.CONFIRMATION,

        )