"""
telegram/keyboard.py
"""

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def main_menu():
    """
    منوی اصلی ربات
    """

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Start Bot",
                callback_data="bot_start",
            ),
            InlineKeyboardButton(
                "🛑 Stop Bot",
                callback_data="bot_stop",
            ),
        ],
        [
            InlineKeyboardButton(
                "♻️ Restart",
                callback_data="bot_restart",
            ),
            InlineKeyboardButton(
                "📊 Status",
                callback_data="bot_status",
            ),
        ],
        [
            InlineKeyboardButton(
                "💰 Balance",
                callback_data="balance",
            ),
            InlineKeyboardButton(
                "📈 Positions",
                callback_data="positions",
            ),
        ],
        [
            InlineKeyboardButton(
                "📑 Orders",
                callback_data="orders",
            ),
            InlineKeyboardButton(
                "💵 PNL",
                callback_data="pnl",
            ),
        ],
        [
            InlineKeyboardButton(
                "⚙️ Settings",
                callback_data="settings",
            ),
            InlineKeyboardButton(
                "📋 Logs",
                callback_data="logs",
            ),
        ],
        [
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data="refresh",
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def back_menu():
    """
    دکمه بازگشت
    """

    keyboard = [
        [
            InlineKeyboardButton(
                "⬅️ بازگشت",
                callback_data="main_menu",
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)
