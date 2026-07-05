from market_features import MarketFeatures

from feature_models.measurement import Measurement
from feature_models.measurement_type import MeasurementType

from .base_factor import VolumeFactor


class VolumeParticipation(
    VolumeFactor,
):

    def measure(
        self,
        features: MarketFeatures,
    ) -> list[Measurement]:

        return [

            Measurement(

                type=MeasurementType.VOLUME_RATIO,

                value=features.volume_ratio,

                unit="ratio",

            )

        ]