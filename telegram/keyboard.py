"""
Telegram Inline Keyboards
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# =====================================================
# MAIN CONTROL PANEL
# =====================================================


def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📊 Status", callback_data="status"),
            InlineKeyboardButton("💰 PnL", callback_data="pnl"),
        ],
        [
            InlineKeyboardButton("📡 Signal BTC", callback_data="signal_BTCUSDT"),
            InlineKeyboardButton("📡 Signal ETH", callback_data="signal_ETHUSDT"),
        ],
        [
            InlineKeyboardButton("🛑 Stop Bot", callback_data="stop"),
            InlineKeyboardButton("🚀 Start Bot", callback_data="start"),
        ],
        [
            InlineKeyboardButton("🛡 Risk", callback_data="risk"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =====================================================
# SIGNAL KEYBOARD
# =====================================================


def signal_keyboard(symbol: str):

    keyboard = [
        [
            InlineKeyboardButton(
                f"📡 Refresh {symbol}", callback_data=f"signal_{symbol}"
            )
        ],
        [
            InlineKeyboardButton("📊 Status", callback_data="status"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)
