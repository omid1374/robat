"""
telegram/callbacks.py
"""

from telegram import Update
from telegram.ext import ContextTypes
from core.balance_service import BalanceService
from core.exchange import exchange
from core.bot_controller import BotController
from telegram.keyboard import main_menu


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    balance_service = BalanceService(exchange)
    query = update.callback_query
    await query.answer()

    controller = BotController.instance()

    data = query.data

    # ===========================
    # Start
    # ===========================

    if data == "bot_start":
        if controller.is_running:
            await query.edit_message_text(
                "🟢 ربات در حال اجراست.",
                reply_markup=main_menu(),
            )

            return

        await controller.start()

        await query.edit_message_text(
            "🚀 ربات با موفقیت شروع شد.",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Stop
    # ===========================

    if data == "bot_stop":
        if not controller.is_running:
            await query.edit_message_text(
                "🔴 ربات متوقف است.",
                reply_markup=main_menu(),
            )

            return

        await controller.stop()

        await query.edit_message_text(
            "🛑 ربات متوقف شد.",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Restart
    # ===========================

    if data == "bot_restart":
        await controller.restart()

        await query.edit_message_text(
            "♻️ ربات ریستارت شد.",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Status
    # ===========================

    if data == "bot_status":
        status = "🟢 فعال" if controller.is_running else "🔴 متوقف"

        await query.edit_message_text(
            f"وضعیت ربات\n\n{status}",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Balance
    # ===========================

    if data == "balance":

        balance = await balance_service.get_balance()

        text = f"""
    💰 Wallet Balance : {balance['wallet_balance']:.2f}

    💵 Available Balance : {balance['available_balance']:.2f}

    📈 Equity : {balance['equity']:.2f}

    📊 Unrealized PNL : {balance['unrealized_pnl']:.2f}

    🕒 {balance['timestamp']}
    """

        await query.edit_message_text(
            text,
            reply_markup=main_menu(),
        )

        return
    # ===========================
    # Positions
    # ===========================

    if data == "positions":
        await query.edit_message_text(
            "📈 بخش پوزیشن‌ها هنوز متصل نشده است.",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Orders
    # ===========================

    if data == "orders":
        await query.edit_message_text(
            "📑 بخش سفارش‌ها هنوز متصل نشده است.",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # PNL
    # ===========================

    if data == "pnl":
        await query.edit_message_text(
            "💵 بخش سود و زیان هنوز متصل نشده است.",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Settings
    # ===========================

    if data == "settings":
        await query.edit_message_text(
            "⚙️ پنل تنظیمات در نسخه بعدی اضافه می‌شود.",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Logs
    # ===========================

    if data == "logs":
        await query.edit_message_text(
            "📋 نمایش لاگ‌ها هنوز متصل نشده است.",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Refresh
    # ===========================

    if data == "refresh":
        status = "🟢 فعال" if controller.is_running else "🔴 متوقف"

        await query.edit_message_text(
            f"🔄 بروزرسانی شد.\n\nوضعیت: {status}",
            reply_markup=main_menu(),
        )

        return

    # ===========================
    # Main Menu
    # ===========================

    if data == "main_menu":
        await query.edit_message_text(
            "پنل مدیریت ربات",
            reply_markup=main_menu(),
        )
