"""
telegram/messages.py
"""

from telegram import Update
from telegram.ext import ContextTypes

from telegram.keyboard import main_menu


WELCOME_MESSAGE = """
🤖 ربات ترید آماده است.

از منوی زیر می‌توانید ربات را مدیریت کنید.

━━━━━━━━━━━━━━━

🚀 Start Bot
🛑 Stop Bot
📊 Status
💰 Balance
📈 Positions
📑 Orders
💵 PNL
⚙️ Settings
📋 Logs

━━━━━━━━━━━━━━━
"""


async def send_main_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    await update.message.reply_text(
        text=WELCOME_MESSAGE,
        reply_markup=main_menu(),
    )


async def send_error(
    update: Update,
    text: str,
):

    await update.message.reply_text(f"❌ {text}")


async def send_success(
    update: Update,
    text: str,
):

    await update.message.reply_text(f"✅ {text}")


async def send_info(
    update: Update,
    text: str,
):

    await update.message.reply_text(f"ℹ️ {text}")
