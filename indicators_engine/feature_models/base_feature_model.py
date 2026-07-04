class BaseFeatureModel:

    @staticmethod
    def normalize(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:

        if maximum <= minimum:
            return 0.0

        score = (
            value - minimum
        ) / (
            maximum - minimum
        )

        return max(
            0.0,
            min(score, 1.0),
        )

    @staticmethod
    def aggregate(
        *scores: float,
    ) -> float:

        if not scores:
            return 0.0

        return sum(scores) / len(scores)