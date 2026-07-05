from feature_models.measurement_type import MeasurementType

from feature_models.builders.trend.adx_builder import ADXBuilder
from feature_models.builders.trend.ema_alignment_builder import (
    EMAAlignmentBuilder,
)
from feature_models.builders.trend.ema_distance_builder import (
    EMADistanceBuilder,
)
from feature_models.builders.trend.price_position_builder import (
    PricePositionBuilder,
)
from feature_models.builders.trend.trend_extension_builder import (
    TrendExtensionBuilder,
)
from feature_models.builders.volume.participation_builder import (
    VolumeParticipationBuilder,
)

from feature_models.builders.volume.expansion_builder import (
    VolumeExpansionBuilder,
)

from feature_models.builders.volume.confirmation_builder import (
    VolumeConfirmationBuilder,
)


class BuilderRegistry:
    def __init__(self):

        self._builders = {
            MeasurementType.ADX: ADXBuilder(),
            MeasurementType.EMA_ALIGNMENT: EMAAlignmentBuilder(),
            MeasurementType.EMA_DISTANCE: EMADistanceBuilder(),
            MeasurementType.PRICE_POSITION: PricePositionBuilder(),
            MeasurementType.TREND_EXTENSION: TrendExtensionBuilder(),
            MeasurementType.VOLUME_RATIO: VolumeParticipationBuilder(),
            MeasurementType.VOLUME_EXPANSION: VolumeExpansionBuilder(),
            MeasurementType.VOLUME_CONFIRMATION: VolumeConfirmationBuilder(),
        }

        self.validate()

    def resolve(
        self,
        measurement_type: MeasurementType,
    ):

        builder = self._builders.get(
            measurement_type,
        )

        if builder is None:
            raise ValueError(f"No builder registered for {measurement_type}")

        return builder

    def validate(
        self,
    ):

        missing = []

        for measurement_type in MeasurementType:
            if measurement_type not in self._builders:
                missing.append(
                    measurement_type.name,
                )

        if missing:
            raise RuntimeError("Missing builders:\n" + "\n".join(missing))
