from dataclasses import dataclass

from feature_models.measurement_type import MeasurementType


@dataclass(
    slots=True,
    frozen=True,
)
class Measurement:
    type: MeasurementType

    value: float

    unit: str

    metadata: dict | None = None
