"""
weights.py

Central scoring configuration.
Everything related to signal scoring should be configurable here.
"""


TIMEFRAMES = [

    "5m",

    "15m",

    "1h",

]

MULTI_TIMEFRAME_CONFIRMATION = True

REQUIRED_CONFIRMATIONS = 2

MULTI_TIMEFRAME_BONUS = 15



# ============================================================
# SIGNAL SCORE
# ============================================================

BUY_THRESHOLD = 75
SELL_THRESHOLD = 75

MAX_SCORE = 100


# ============================================================
# TREND
# ============================================================

BULLISH_TREND = 25
BEARISH_TREND = 25


# ============================================================
# TREND STRENGTH (ADX)
# ============================================================

VERY_STRONG_TREND = 20
STRONG_TREND = 15
MEDIUM_TREND = 8
WEAK_TREND = 0


# ============================================================
# MOMENTUM (MACD)
# ============================================================

BULLISH_MOMENTUM = 20
BEARISH_MOMENTUM = 20


# ============================================================
# RSI
# ============================================================

HEALTHY_RSI = 10

OVERSOLD = 15

OVERBOUGHT = 15

WEAK_RSI = 10


# ============================================================
# BREAKOUT
# ============================================================

BREAKOUT_SCORE = 15


# ============================================================
# VOLUME
# ============================================================

HIGH_VOLUME = 5

LOW_VOLUME = -5


# ============================================================
# VOLATILITY
# ============================================================

HIGH_VOLATILITY = -5

LOW_VOLATILITY = 0


# ============================================================
# ADX FILTERS
# ============================================================

ADX_VERY_STRONG = 35

ADX_STRONG = 25

ADX_MEDIUM = 18


# ============================================================
# RSI FILTERS
# ============================================================

RSI_OVERBOUGHT = 75

RSI_OVERSOLD = 25

RSI_BULL_MIN = 50

RSI_BULL_MAX = 65

RSI_BEAR_MIN = 35

RSI_BEAR_MAX = 50


# ============================================================
# ATR
# ============================================================

ATR_SL_MULTIPLIER = 1.5

ATR_TP_MULTIPLIER = 3.0

ATR_TRAILING = 1.2


# ============================================================
# RISK REWARD
# ============================================================

MIN_RISK_REWARD = 2.0

DEFAULT_RISK_REWARD = 2.5

MAX_RISK_REWARD = 4.0


# ============================================================
# MARKET FILTERS
# ============================================================

MIN_VOLUME_MULTIPLIER = 1.2

BREAKOUT_VOLUME = 1.5

HIGH_VOLATILITY_MULTIPLIER = 1.5

LOW_VOLATILITY_MULTIPLIER = 0.7


# ============================================================
# ENGINE FILTERS
# ============================================================

MIN_CONFIDENCE = 80

MAX_SPREAD_PERCENT = 0.15

MAX_SLIPPAGE = 0.10


# ============================================================
# POSITION FILTERS
# ============================================================

MAX_OPEN_TRADES = 3

COOLDOWN_AFTER_LOSS = 600

MAX_CONSECUTIVE_LOSS = 3


# ============================================================
# SCORING BONUSES
# ============================================================

EMA_ALIGNMENT_BONUS = 5

MULTI_TIMEFRAME_BONUS = 10

HIGH_VOLUME_BONUS = 5

STRONG_ADX_BONUS = 5

LOW_SPREAD_BONUS = 5

HIGH_LIQUIDITY_BONUS = 5


# ============================================================
# SCORING PENALTIES
# ============================================================

LOW_VOLUME_PENALTY = -5

HIGH_SPREAD_PENALTY = -10

NEWS_TIME_PENALTY = -20

RANGING_MARKET_PENALTY = -10

EXTREME_VOLATILITY_PENALTY = -15
