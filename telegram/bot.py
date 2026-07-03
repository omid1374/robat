"""
telegram/bot.py
"""

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)
from telegram.notifications import notifications


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
        notifications.bind(self.app.bot)
        self._register_handlers()

    # ----------------------------------

    def _register_handlers(self):

        self.app.add_handler(CommandHandler("start", start_command))
        self.app.add_handler(CommandHandler("stop", stop_command))
        self.app.add_handler(CommandHandler("restart", restart_command))
        self.app.add_handler(CommandHandler("status", status_command))
        self.app.add_handler(CommandHandler("help", help_command))
        self.app.add_handler(CommandHandler("ping", ping_command))

        self.app.add_handler(CallbackQueryHandler(callback_handler))

    # ----------------------------------
    # Async Lifecycle
    # ----------------------------------


    async def start(self):

        await notifications.start()

        await self.app.initialize()

        await self.app.start()

        await self.app.updater.start_polling(
            drop_pending_updates=True
        )

    async def stop(self):
        await notifications.stop()
        await self.app.updater.stop()

        await self.app.stop()

        await self.app.shutdown()

    # ----------------------------------
    # فقط برای تست مستقل
    # ----------------------------------

    def run(self):

        self.app.run_polling(drop_pending_updates=True)
