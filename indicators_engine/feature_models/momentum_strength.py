from market_features import MarketFeatures

from .base_feature import BaseFeature
from .base_feature_model import BaseFeatureModel
from .feature_model import FeatureModel
from .feature_type import FeatureType

from .evidence import Evidence

from .momentum.rsi import RSIStrength
from .momentum.macd import MACDStrength
from .momentum.histogram import HistogramStrength
from .momentum.alignment import MomentumAlignment


class MomentumStrength(
    BaseFeature,
    BaseFeatureModel,
    FeatureModel,
):
    NAME = FeatureType.MOMENTUM

    FACTORS = (
        RSIStrength(),
        MACDStrength(),
        HistogramStrength(),
        MomentumAlignment(),
    )

    def build_evidences(
        self,
        features: MarketFeatures,
    ) -> list[Evidence]:

        evidences = []

        for factor in self.FACTORS:
            measurements = factor.measure(
                features,
            )

            for measurement in measurements:
                builder = self.pipeline.resolve(
                    measurement.type,
                )

                evidences.append(
                    builder.build(
                        measurement,
                    )
                )

        return evidences
