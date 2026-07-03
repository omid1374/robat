"""
settings.py

تنظیمات و متغیرهای سراسری ربات Market Maker
"""

import logging
from datetime import datetime

from mt5_utils import SYMBOL, VOLUME

# -------------------------------------------------
# Logging
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            "market_maker.log",
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

# -------------------------------------------------
# Market Maker Settings
# -------------------------------------------------

# فاصله زمانی اجرای حلقه اصلی
LOOP_INTERVAL = 1

# حداکثر اسپرد مجاز
MAX_SPREAD_ALLOWED = 30.0

# حداقل اسپرد پایه
MIN_SPREAD_FLOOR = 30.0

# حداکثر ضرر مجاز هر معامله
MAX_ALLOWED_LOSS_DOLLARS = 20.0

# مدت توقف ربات پس از استاپ اضطراری
COOLDOWN_MINUTES = 60

# ضریب ATR برای تعیین فاصله سفارش
ATR_MULTIPLIER = 1.2

# ضریب حد سود
TAKE_PROFIT_MULTIPLIER = 1.5

# تلورانس جابه‌جایی سفارش
ORDER_REFRESH_THRESHOLD = 0.10

# -------------------------------------------------
# Runtime Variables
# -------------------------------------------------

cooldown_end_time = datetime.now()

buy_entry_offset = None

sell_entry_offset = None

# -------------------------------------------------
# Shared Exports
# -------------------------------------------------

__all__ = [
    "logger",
    "SYMBOL",
    "VOLUME",
    "LOOP_INTERVAL",
    "MAX_SPREAD_ALLOWED",
    "MIN_SPREAD_FLOOR",
    "MAX_ALLOWED_LOSS_DOLLARS",
    "COOLDOWN_MINUTES",
    "ATR_MULTIPLIER",
    "TAKE_PROFIT_MULTIPLIER",
    "ORDER_REFRESH_THRESHOLD",
    "cooldown_end_time",
    "buy_entry_offset",
    "sell_entry_offset",
]
