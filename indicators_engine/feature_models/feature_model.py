from abc import ABC
from abc import abstractmethod
from .feature_type import FeatureType
from market_features import MarketFeatures

from .evidence import Evidence


class FeatureModel(ABC):
    """
    Base contract for every feature model.
    """

    NAME: FeatureType

    FACTORS: tuple[str, ...]

    @abstractmethod
    def evaluate(
        self,
        features: MarketFeatures,
    ) -> list[Evidence]:
        """
        Evaluate market features and return evidences.
        """
        ...
