from abc import ABC
from abc import abstractmethod

from feature_models.pipeline.feature_pipeline import (
    FeaturePipeline,
)


class BaseFeature(ABC):
    def __init__(
        self,
        pipeline: FeaturePipeline,
    ):

        self.pipeline = pipeline

    @abstractmethod
    def calculate(
        self,
        features,
    ): ...
