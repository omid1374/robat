from market_features import MarketFeatures

from feature_models.measurement import Measurement
from feature_models.measurement_type import MeasurementType
from .base_factor import TrendFactor


class TrendPersistence(
    TrendFactor,
):
    """
    Measure trend persistence.

    This class contains NO interpretation.

    Only objective observations.
    """

    def measure(
        self,
        features: MarketFeatures,
    ) -> list[Measurement]:

        return [
            Measurement(
                type=MeasurementType.ADX,
                value=features.adx,
                unit="index",
            )
        ]
