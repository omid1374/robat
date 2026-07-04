from market_features import MarketFeatures

from .base_feature import BaseFeature
from .base_feature_model import BaseFeatureModel
from .feature_model import FeatureModel
from .feature_type import FeatureType

from .evidence import Evidence


class MomentumStrength(
    BaseFeature,
    BaseFeatureModel,
    FeatureModel,
):
    NAME = FeatureType.MOMENTUM

    FACTORS = (
        "rsi_strength",
        "macd_strength",
        "momentum_alignment",
    )

    def build_evidences(
        self,
        features: MarketFeatures,
    ) -> list[Evidence]:

        raise NotImplementedError
