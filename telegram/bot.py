"""
telegram/bot.py
"""

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

from telegram.commands import (
    start_command,
    stop_command,
    restart_command,
    status_command,
    help_command,
    ping_command,
)

from telegram.callbacks import callback_handler


class TelegramBot:
    def __init__(self, token: str):
        self.token = token

        self.app = Application.builder().token(token).build()

        self._register_handlers()

    # ----------------------------------
    # Register Handlers
    # ----------------------------------

    def _register_handlers(self):

        # Command Handlers
        self.app.add_handler(CommandHandler("start", start_command))
        self.app.add_handler(CommandHandler("stop", stop_command))
        self.app.add_handler(CommandHandler("restart", restart_command))
        self.app.add_handler(CommandHandler("status", status_command))
        self.app.add_handler(CommandHandler("help", help_command))
        self.app.add_handler(CommandHandler("ping", ping_command))

        # Callback Buttons
        self.app.add_handler(CallbackQueryHandler(callback_handler))

    # ----------------------------------
    # Start Bot
    # ----------------------------------

    def run(self):
        self.app.run_polling(
            drop_pending_updates=True,
            allowed_updates=None,
        )

    # ----------------------------------
    # Stop Bot
    # ----------------------------------

    async def stop(self):
        await self.app.stop()
        await self.app.shutdown()
