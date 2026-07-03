"""
Telegram Bot main entry
"""
from telegram.commands import (
    start_command,
    stop_command,
    status_command,
    restart_command,
)
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from telegram.commands import start_command, status_command, stop_command

app.add_handler(CommandHandler("restart", restart_command))


class TelegramBot:
    def __init__(self, token: str, engine):

        self.token = token

        self.engine = engine

        self.app = Application.builder().token(token).build()

        self._register_handlers()

    # -----------------------------------------
    # REGISTER COMMANDS
    # -----------------------------------------

    def _register_handlers(self):

        self.app.add_handler(CommandHandler("start", self._start))
        self.app.add_handler(CommandHandler("status", self._status))
        self.app.add_handler(CommandHandler("stop", self._stop))

    
    # -----------------------------------------
    # WRAPPERS
    # -----------------------------------------

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text("Bot started 🚀")

        self.engine.running = True

    async def _stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text("Bot stopped ⛔")

        self.engine.running = False

    async def _status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        status = self.engine.running

        await update.message.reply_text(
            f"Engine status: {'RUNNING' if status else 'STOPPED'}"
        )

    # -----------------------------------------
    # RUN
    # -----------------------------------------

    def run(self):

        self.app.run_polling()
