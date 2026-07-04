from dataclasses import dataclass
from enum import Enum


class EvidenceType(Enum):
    VALIDATION = "validation"

    QUALITY = "quality"

    CONFIRMATION = "confirmation"


@dataclass(slots=True)
class Evidence:
    name: str

    score: float

    reason: str

    type: EvidenceType
