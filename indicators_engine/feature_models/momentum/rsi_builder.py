from feature_models.builders.base_builder import (
    BaseMeasurementBuilder,
)

from feature_models.evidence import (
    Evidence,
    EvidenceType,
)

from feature_models.measurement import Measurement


class RSIBuilder(
    BaseMeasurementBuilder,
):

    def build(
        self,
        measurement: Measurement,
    ) -> Evidence:

        rsi = measurement.value

        if rsi >= 70:

            score = 0.30
            reason = "RSI is overbought"

        elif rsi >= 60:

            score = 1.00
            reason = "Strong bullish momentum"

        elif rsi >= 50:

            score = 0.80
            reason = "Bullish momentum"

        elif rsi >= 40:

            score = 0.60
            reason = "Neutral momentum"

        elif rsi >= 30:

            score = 0.80
            reason = "Bearish momentum"

        else:

            score = 0.30
            reason = "RSI is oversold"

        return Evidence(

            name="rsi",

            score=score,

            reason=reason,

            type=EvidenceType.CONFIRMATION,

        )