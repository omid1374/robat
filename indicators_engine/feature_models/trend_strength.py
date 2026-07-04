from market_features import MarketFeatures

from .base_feature import BaseFeature
from .base_feature_model import BaseFeatureModel
from .feature_model import FeatureModel
from .feature_type import FeatureType

from .evidence import Evidence

from .trend.persistence import TrendPersistence
from .trend.structure import TrendStructure
from .trend.extension import TrendExtension


class TrendStrength(
    BaseFeature,
    BaseFeatureModel,
    FeatureModel,
):
    NAME = FeatureType.TREND

    FACTORS = (
        TrendPersistence(),
        TrendStructure(),
        TrendExtension(),
    )

    def build_evidences(
        self,
        features: MarketFeatures,
    ) -> list[Evidence]:

        evidences = []

        for factor in self.FACTORS:
            evidences.append(
                factor.evaluate(
                    features,
                )
            )

        return evidences
