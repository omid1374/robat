class TradeExecutionUnknown(Exception):
    """
    The exchange did not confirm whether the trade request
    succeeded or failed.

    Caller must verify open orders / positions before retrying.
    """

    pass