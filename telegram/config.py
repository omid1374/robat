"""
Telegram Bot Configuration
"""

# =====================================================
# BOT SETTINGS
# =====================================================

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

CHAT_ID = "YOUR_CHAT_ID_HERE"


# =====================================================
# ALERT SETTINGS
# =====================================================

ALERT_CONFIDENCE_THRESHOLD = 80

ALERT_COOLDOWN_SECONDS = 60

SCAN_INTERVAL_SECONDS = 10


# =====================================================
# COMMAND SETTINGS
# =====================================================

ENABLE_SIGNAL_COMMAND = True

ENABLE_STATUS_COMMAND = True

ENABLE_RISK_COMMAND = True


# =====================================================
# SECURITY (Optional)
# =====================================================

ALLOWED_USERS = [
    123456789,  # your telegram user id
]


# =====================================================
# DISPLAY SETTINGS
# =====================================================

SHOW_DEBUG_INFO = False

SHOW_TIMEFRAMES = True