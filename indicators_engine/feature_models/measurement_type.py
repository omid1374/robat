from enum import Enum


class MeasurementType(str, Enum):
    # ===== Trend =====

    ADX = "adx"

    EMA_ALIGNMENT = "ema_alignment"

    EMA_DISTANCE = "ema_distance"

    PRICE_POSITION = "price_position"

    TREND_EXTENSION = "trend_extension"

    # ===== Momentum =====

    RSI = "rsi"

    MACD = "macd"

    MACD_HISTOGRAM = "macd_histogram"

    MOMENTUM_ALIGNMENT = "momentum_alignment"

    # ===== Volume =====

    VOLUME_RATIO = "volume_ratio"

    VOLUME_EXPANSION = "volume_expansion"

    VOLUME_CONFIRMATION = "volume_confirmation"

    # ===== Volatility =====

    ATR_PERCENT = "atr_percent"

    BOLLINGER_WIDTH = "bollinger_width"

    COMPRESSION = "compression"
