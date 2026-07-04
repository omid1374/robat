from feature_models.measurement import Measurement
from feature_models.evidence import Evidence

from feature_models.builders.registry import BuilderRegistry


class BuilderPipeline:
    """
    Convert Measurements into Evidences.
    """

    def __init__(self):

        self.registry = BuilderRegistry()

    def build(
        self,
        measurements: list[Measurement],
    ) -> list[Evidence]:

        evidences: list[Evidence] = []

        for measurement in measurements:
            builder = self.registry.resolve(
                measurement.type,
            )

            evidences.append(
                builder.build(
                    measurement,
                )
            )

        return evidences
