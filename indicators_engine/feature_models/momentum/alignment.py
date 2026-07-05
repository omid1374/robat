from market_features import MarketFeatures

from feature_models.measurement import Measurement
from feature_models.measurement_type import MeasurementType

from .base_factor import MomentumFactor


class MomentumAlignment(
    MomentumFactor,
):

    def measure(
        self,
        features: MarketFeatures,
    ) -> list[Measurement]:

        bullish = (

            features.ema20 >
            features.ema50 >
            features.ema200

        )

        bearish = (

            features.ema20 <
            features.ema50 <
            features.ema200

        )

        if bullish:

            aligned = (

                features.macd > 0

                and

                features.rsi > 50

            )

        elif bearish:

            aligned = (

                features.macd < 0

                and

                features.rsi < 50

            )

        else:

            aligned = False

        return [

            Measurement(

                type=MeasurementType.MOMENTUM_ALIGNMENT,

                value=1.0 if aligned else 0.0,

                unit="bool",

            )

        ]