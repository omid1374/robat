from feature_models.measurement_type import MeasurementType

from .adx_normalizer import ADXNormalizer


class NormalizerRegistry:

    def __init__(self):

        self._normalizers = {

            MeasurementType.ADX:
                ADXNormalizer(),

        }

    def resolve(
        self,
        measurement_type,
    ):

        return self._normalizers[
            measurement_type
        ]