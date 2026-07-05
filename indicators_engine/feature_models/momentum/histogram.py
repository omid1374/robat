from market_features import MarketFeatures

from feature_models.measurement import Measurement
from feature_models.measurement_type import MeasurementType

from .base_factor import MomentumFactor


class HistogramStrength(
    MomentumFactor,
):

    def measure(
        self,
        features: MarketFeatures,
    ) -> list[Measurement]:

        return [

            Measurement(

                type=MeasurementType.MACD_HISTOGRAM,

                value=features.macd_hist,

                unit="index",

            )

        ]