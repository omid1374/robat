from feature_models.measurement_type import MeasurementType

from feature_models.builders.trend.adx_builder import ADXBuilder
from feature_models.builders.trend.ema_alignment_builder import (
    EMAAlignmentBuilder,
)


class BuilderRegistry:

    def __init__(self):

        self._builders = {

            MeasurementType.ADX:
                ADXBuilder(),

            MeasurementType.EMA_ALIGNMENT:
                EMAAlignmentBuilder(),

        }

    def resolve(
        self,
        measurement_type: MeasurementType,
    ):

        return self._builders[
            measurement_type
        ]