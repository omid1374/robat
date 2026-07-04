from abc import ABC
from abc import abstractmethod

from .evidence import Evidence


class FeaturePolicy(ABC):
    """
    Defines how evidences are combined into a score.
    """

    @abstractmethod
    def score(
        self,
        evidences: list[Evidence],
    ) -> float: ...
