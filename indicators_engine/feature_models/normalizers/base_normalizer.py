from abc import ABC
from abc import abstractmethod

from feature_models.measurement import Measurement


class BaseNormalizer(
    ABC,
):

    @abstractmethod
    def normalize(
        self,
        measurement: Measurement,
    ) -> float:
        ...