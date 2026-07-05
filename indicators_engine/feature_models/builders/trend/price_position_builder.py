from feature_models.builders.base_builder import BaseBuilder

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.measurement import Measurement


class PricePositionBuilder(BaseBuilder):

    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        score = max(
            0.0,
            min(
                measurement.value,
                1.0,
            ),
        )

        return Evidence(

            name="price_position",

            score=score,

            reason=f"Price position = {measurement.value:.2f}",

            type=EvidenceType.CONFIRMATION,

        )