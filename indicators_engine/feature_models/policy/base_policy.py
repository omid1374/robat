from abc import ABC
from abc import abstractmethod

from feature_models.measurement import Measurement
from feature_models.feature_context import FeatureContext


class BasePolicy(
    ABC,
):

    @abstractmethod
    def evaluate(
        self,
        measurement: Measurement,
        normalized_score: float,
        context: FeatureContext,
    ) -> tuple[
        str,
        float,
        str,
        ]:
        """
        Returns

        name

        score

        reason
        """
        ...