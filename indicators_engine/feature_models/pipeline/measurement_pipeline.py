from market_features import MarketFeatures

from feature_models.measurement import Measurement


class MeasurementPipeline:
    def collect(
        self,
        feature_model,
        features: MarketFeatures,
    ) -> list[Measurement]:

        measurements: list[Measurement] = []

        for factor_type in feature_model.FACTOR_TYPES:

            factor = factor_type()

            measurements.extend(

                factor.measure(
                    features,
                )

            )

        return measurements
