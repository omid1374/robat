from market_state import MarketState


class ConflictEngine:
    """
    Detect conflicts between FeatureModels.

    This engine does NOT decide.

    It only measures agreement
    between feature opinions.
    """

    def analyze(
        self,
        state: MarketState,
    ):
        raise NotImplementedError
