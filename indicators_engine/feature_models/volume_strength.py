from market_features import MarketFeatures

from .base_feature import BaseFeature
from .base_feature_model import BaseFeatureModel
from .feature_model import FeatureModel
from .feature_type import FeatureType
from .evidence import Evidence

from .volume.participation import VolumeParticipation
from .volume.expansion import VolumeExpansion
from .volume.confirmation import VolumeConfirmation


class VolumeStrength(
    BaseFeature,
    BaseFeatureModel,
    FeatureModel,
):
    NAME = FeatureType.VOLUME

    FACTORS = (
        VolumeParticipation(),
        VolumeExpansion(),
        VolumeConfirmation(),
    )

    def build_evidences(
        self,
        features: MarketFeatures,
    ) -> list[Evidence]:

        return [factor.evaluate(features) for factor in self.FACTORS]
