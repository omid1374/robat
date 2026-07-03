"""
telegram/commands.py
"""

from telegram import Update
from telegram.ext import ContextTypes

from core.bot_controller import BotController


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    controller = BotController.instance()

    if controller.is_running:
        await update.message.reply_text("🟢 ربات هم‌اکنون در حال اجراست.")
        return

    await controller.start()

    await update.message.reply_text("🚀 ربات با موفقیت راه‌اندازی شد.")


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    controller = BotController.instance()

    if not controller.is_running:
        await update.message.reply_text("🔴 ربات از قبل متوقف بوده است.")
        return

    await controller.stop()

    await update.message.reply_text("🛑 ربات متوقف شد.")


async def restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    controller = BotController.instance()

    await controller.restart()

    await update.message.reply_text("♻️ ربات مجدداً راه‌اندازی شد.")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    controller = BotController.instance()

    status = "🟢 فعال" if controller.is_running else "🔴 متوقف"

    msg = f"وضعیت ربات: {status}\nTask فعال: {controller.task_count}\n"

    await update.message.reply_text(msg)
