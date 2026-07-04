from feature_models.measurement import Measurement

from .base_normalizer import BaseNormalizer


class ADXNormalizer(
    BaseNormalizer,
):

    def normalize(
        self,
        measurement: Measurement,
    ) -> float:

        value = measurement.value

        score = (value - 15.0) / (45.0 - 15.0)

        return max(
            0.0,
            min(score, 1.0),
        )