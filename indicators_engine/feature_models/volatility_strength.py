from market_features import MarketFeatures

from .base_feature import BaseFeature
from .base_feature_model import BaseFeatureModel
from .feature_model import FeatureModel
from .feature_type import FeatureType
from .evidence import Evidence

from .volatility.atr import ATRQuality
from .volatility.bollinger import BollingerQuality
from .volatility.compression import CompressionQuality


class VolatilityStrength(
    BaseFeature,
    BaseFeatureModel,
    FeatureModel,
):
    NAME = FeatureType.VOLATILITY

    FACTORS = (
        ATRQuality(),
        BollingerQuality(),
        CompressionQuality(),
    )

    def build_evidences(
        self,
        features: MarketFeatures,
    ) -> list[Evidence]:

        return [
            factor.evaluate(
                features,
            )
            for factor in self.FACTORS
        ]
