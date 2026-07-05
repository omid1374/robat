from market_features import MarketFeatures

from feature_models.measurement import Measurement
from feature_models.measurement_type import MeasurementType

from .base_factor import VolumeFactor


class VolumeConfirmation(
    VolumeFactor,
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

        confirmed = (

            bullish or bearish

        ) and (

            features.volume_ratio >= 1.2

        )

        return [

            Measurement(

                type=MeasurementType.VOLUME_CONFIRMATION,

                value=1.0 if confirmed else 0.0,

                unit="bool",

            )

        ]