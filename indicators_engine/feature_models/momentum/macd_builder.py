from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.measurement import Measurement


class MACDBuilder(
    BaseMeasurementBuilder,
):

    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        macd = measurement.value

        score = min(

            abs(macd),

            1.0,

        )

        if macd > 0:

            reason = "MACD is bullish"

        elif macd < 0:

            reason = "MACD is bearish"

        else:

            reason = "MACD is neutral"

        return Evidence(

            name="macd",

            score=score,

            reason=reason,

            type=EvidenceType.CONFIRMATION,

        )