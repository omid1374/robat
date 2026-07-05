from market_features import MarketFeatures

from feature_models.measurement import Measurement
from feature_models.measurement_type import MeasurementType
from .base_factor import TrendFactor


class TrendStructure(
    TrendFactor,
):
    def measure(
        self,
        features: MarketFeatures,
    ) -> list[Measurement]:

        measurements: list[Measurement] = []

        bullish = features.ema20 > features.ema50 > features.ema200

        bearish = features.ema20 < features.ema50 < features.ema200

        alignment = 1.0 if (bullish or bearish) else 0.0

        measurements.append(
            Measurement(
                type=MeasurementType.EMA_ALIGNMENT,
                value=alignment,
                unit="score",
            )
        )

        distance_1 = abs(features.ema20 - features.ema50)

        distance_2 = abs(features.ema50 - features.ema200)

        measurements.append(
            Measurement(
                type=MeasurementType.EMA_DISTANCE,
                value=(distance_1 + distance_2),
                unit="price",
            )
        )

        measurements.append(
            Measurement(
                type=MeasurementType.PRICE_POSITION,
                value=features.close,
                unit="price",
                metadata={
                    "ema20": features.ema20,
                },
            )
        )

        return measurements
