from feature_models.context.market_context import (
    MarketContext,
)

from feature_models.feature_result import (
    FeatureResult,
)

from feature_models.feature_type import (
    FeatureType,
)


class ContextBuilder:

    def build(
        self,
        results: dict[
            str,
            FeatureResult,
        ],
    ) -> MarketContext:

        return MarketContext(

            trend_score=results[
                FeatureType.TREND.value
            ].score,

            momentum_score=results[
                FeatureType.MOMENTUM.value
            ].score,

            volume_score=results[
                FeatureType.VOLUME.value
            ].score,

            volatility_score=results[
                FeatureType.VOLATILITY.value
            ].score,

        )