from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.measurement import Measurement


class HistogramBuilder(
    BaseMeasurementBuilder,
):

    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        histogram = measurement.value

        score = min(

            abs(histogram),

            1.0,

        )

        if histogram > 0:

            reason = "Bullish histogram"

        elif histogram < 0:

            reason = "Bearish histogram"

        else:

            reason = "Flat histogram"

        return Evidence(

            name="macd_histogram",

            score=score,

            reason=reason,

            type=EvidenceType.CONFIRMATION,

        )