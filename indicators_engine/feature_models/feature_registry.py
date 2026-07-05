from feature_models.trend_strength import (
    TrendStrength,
)
from feature_models.momentum_strength import (
    MomentumStrength,
)


from feature_models.volume_strength import VolumeStrength


class FeatureRegistry:

    def __init__(
        self,
        pipeline,
    ):
        self.pipeline = pipeline

    def get_features(
        self,
    ):
        return [
            TrendStrength(),

            MomentumStrength(),

            VolumeStrength(),
        ]