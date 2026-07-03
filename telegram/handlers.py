"""
telegram handlers - Pro version
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram import Update
from telegram.ext import ContextTypes


# -----------------------------------------------------
# STATUS FULL
# -----------------------------------------------------


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE, engine):

    risk = engine.risk_manager

    message = f"""
📊 ENGINE STATUS

🟢 Running: {engine.running}

📈 Trades Today: {risk.trades_today}

📉 Daily Loss: {risk.daily_loss:.2f}%

❌ Consecutive Losses: {risk.consecutive_losses}

💰 Balance: {risk.current_balance}
"""

    await update.message.reply_text(message)


# -----------------------------------------------------
# PNL REPORT
# -----------------------------------------------------


async def pnl_command(update: Update, context: ContextTypes.DEFAULT_TYPE, engine):

    risk = engine.risk_manager

    pnl = risk.current_balance - risk.daily_start_balance if risk.current_balance else 0

    message = f"""
💰 PNL REPORT

Daily PnL: {pnl:.2f}
Daily Loss %: {risk.daily_loss:.2f}%
"""

    await update.message.reply_text(message)


# -----------------------------------------------------
# RISK STATUS
# -----------------------------------------------------


async def risk_command(update: Update, context: ContextTypes.DEFAULT_TYPE, engine):

    risk = engine.risk_manager

    can_trade = risk.can_open_trade()

    message = f"""
🛡 RISK STATUS

Can Trade: {"YES" if can_trade else "NO"}

Max Daily Loss: {risk.max_daily_loss_percent}%
Max Trades: {risk.max_trades_per_day}

Consecutive Losses: {risk.consecutive_losses}
"""

    await update.message.reply_text(message)




# =====================================================
# SIGNAL VIEWER
# =====================================================


async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE, engine):

    # گرفتن symbol از کاربر
    symbol = context.args[0] if context.args else "BTCUSDT"

    try:
        # گرفتن سیگنال زنده از engine
        signal = await engine.calculate_live_indicators(
            client=engine.client, symbol=symbol
        )

        message = f"""
📡 LIVE SIGNAL

Symbol: {symbol}

🟢 BUY: {signal["buy"]}
🔴 SELL: {signal["sell"]}
🔥 CONFIDENCE: {signal["confidence"]}

📊 BUY SCORE: {signal["buy_score"]}
📉 SELL SCORE: {signal["sell_score"]}

📌 STATUS: {signal.get("status", "UNKNOWN")}
"""

        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"❌ Error getting signal: {str(e)}")
