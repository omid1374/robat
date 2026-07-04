from feature_models.feature_context import FeatureContext
from feature_models.measurement import Measurement

from feature_models.policies.base_policy import BasePolicy


class ADXPolicy(
    BasePolicy,
):
    def evaluate(
        self,
        measurement: Measurement,
        normalized_score: float,
        context: FeatureContext,
    ):

        reason = f"ADX={measurement.value:.1f}"

        return (
            "trend_persistence",
            normalized_score,
            reason,
        )
