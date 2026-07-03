"""
telegram/commands.py
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.messages import send_main_menu
from core.bot_controller import BotController


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    controller = BotController.instance()

    if controller.is_running:
        await update.message.reply_text("🟢 ربات در حال اجراست.")
        return

    await controller.start()

    await send_main_menu(update, context)


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    controller = BotController.instance()

    if not controller.is_running:
        await update.message.reply_text("🔴 ربات متوقف است.")
        return

    await controller.stop()

    await update.message.reply_text("🛑 ربات متوقف شد.")


async def restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    controller = BotController.instance()

    await controller.restart()

    await update.message.reply_text("♻️ ربات مجدداً راه‌اندازی شد.")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    controller = BotController.instance()

    text = "🟢 وضعیت: فعال\n" if controller.is_running else "🔴 وضعیت: متوقف\n"

    text += f"Task فعال: {controller.task_count}"

    await update.message.reply_text(text)


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
دستورات ربات

/start
راه‌اندازی ربات

/stop
توقف ربات

/restart
راه‌اندازی مجدد

/status
نمایش وضعیت

/ping
تست اتصال

/help
راهنما
"""

    await update.message.reply_text(text)
