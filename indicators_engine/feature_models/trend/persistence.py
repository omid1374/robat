from market_features import MarketFeatures

from feature_models.measurement import Measurement

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
                name="adx",
                value=features.adx,
                unit="index",
            )
        ]
