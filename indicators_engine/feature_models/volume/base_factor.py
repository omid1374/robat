from abc import ABC
from abc import abstractmethod
from feature_models.measurement import Measurement
from market_features import MarketFeatures



class VolumeFactor(ABC):
    @abstractmethod
    def measure(
        self,
        features: MarketFeatures,
    ) -> list[Measurement]:
        ...
