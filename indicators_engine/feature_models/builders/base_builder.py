from abc import ABC
from abc import abstractmethod

from feature_models.measurement import Measurement
from feature_models.evidence import Evidence


class BaseMeasurementBuilder(
    ABC,
):
    @abstractmethod
    def build(
        self,
        measurement: Measurement,
    ) -> Evidence: ...
