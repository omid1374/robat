"""
config.py
تنظیمات پروژه ربات مارکت میکر BloFin
"""

import os
from dotenv import load_dotenv

# بارگذاری فایل .env
load_dotenv()

# =========================
# Exchange
# =========================

EXCHANGE_NAME = "blofin"

SYMBOL = "DOGE/USDT:USDT"

DEFAULT_TYPE = "swap"

TESTNET = False

# =========================
# API
# =========================

API_KEY = os.getenv("BLOFIN_API_KEY")

API_SECRET = os.getenv("BLOFIN_SECRET")

API_PASSWORD = os.getenv("BLOFIN_PASSWORD")

# =========================
# Trading
# =========================

BASE_ORDER_SIZE = 0.02

MAX_INVENTORY = 0.20

LEVERAGE = 5

POST_ONLY = True

# =========================
# Pricing Model
# =========================

BASE_SPREAD = 0.00030

K_VOL = 0.25

K_INV = 0.002

# =========================
# Indicators
# =========================

EMA_PERIOD = 200

ATR_PERIOD = 20

VPIN_BUCKET_MIN = 5000

VPIN_BUCKET_MULTIPLIER = 20

# =========================
# Risk Management
# =========================

MAX_ALLOWED_LOSS = 20.0

COOLDOWN_MINUTES = 60

MAX_SPREAD_ALLOWED = 30.0

# =========================
# Strategy
# =========================

ORDER_REFRESH_SECONDS = 1

POSITION_REFRESH_SECONDS = 5

ORDERBOOK_DEPTH = 5

# =========================
# Telegram
# =========================

TELEGRAM_ENABLED = False

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# =========================
# Logging
# =========================

LOG_LEVEL = "INFO"

LOG_FILE = "market_maker.log"

# =========================
# Network
# =========================

USE_IPV4 = True

ENABLE_RATE_LIMIT = True

VERIFY_SSL = True