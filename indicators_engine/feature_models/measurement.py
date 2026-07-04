from dataclasses import dataclass
from typing import Any
from feature_models.measurement_type import MeasurementType

@dataclass(slots=True)
class Measurement:
    """
    Raw market measurement.

    Measurements contain observations.

    They DO NOT contain interpretation.

    Example
    -------

    ema_distance = 2.84 ATR

    adx = 31.7

    rsi = 63.2

    volume_ratio = 1.84
    """

    name: str
    type: MeasurementType
    value: float

    unit: str

    metadata: dict[str, Any] | None = None