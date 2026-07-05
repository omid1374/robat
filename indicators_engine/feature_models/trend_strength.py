from .base_feature import BaseFeature
from .feature_type import FeatureType
from .trend.persistence import TrendPersistence
from .trend.structure import TrendStructure
from .trend.extension import TrendExtension


class TrendStrength(
    BaseFeature,
):
    NAME = FeatureType.TREND

    FACTOR_TYPES = (
        TrendPersistence,
        TrendStructure,
        TrendExtension,
    )

    def calculate(
        self,
        features,
    ):

        return self.pipeline.execute(
            self,
            features,
        )
