from market_features import MarketFeatures

from feature_models.measurement import Measurement


class MeasurementPipeline:
    """
    Collect measurements from one FeatureModel.

    This pipeline knows nothing about Evidence.

    It only gathers objective market observations.
    """

    def collect(
        self,
        feature_model,
        features: MarketFeatures,
    ) -> list[Measurement]:

        measurements: list[Measurement] = []

        for factor in feature_model.FACTORS:
            measurements.extend(
                factor.measure(
                    features,
                )
            )

        return measurements
