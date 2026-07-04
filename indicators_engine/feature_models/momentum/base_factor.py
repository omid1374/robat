from abc import ABC
from abc import abstractmethod

from market_features import MarketFeatures
from feature_models.measurement import Measurement



class MomentumFactor(ABC):

    @abstractmethod
    def measure(
        self,
        features: MarketFeatures,
    ) -> list[Measurement]:
        ...