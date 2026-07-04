from market_features import MarketFeatures

from feature_models.measurement import Measurement
from feature_models.measurement_type import MeasurementType

from .base_factor import TrendFactor


class TrendExtension(
    TrendFactor,
):
    def measure(
        self,
        features: MarketFeatures,
    ) -> list[Measurement]:

        distance = abs(features.close - features.ema20) / max(
            features.atr,
            1e-8,
        )

        return [
            Measurement(
                type=MeasurementType.TREND_EXTENSION,
                value=distance,
                unit="ATR",
            )
        ]
