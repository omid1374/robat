"""
Real-time Telegram Alert System
"""

import asyncio
from datetime import datetime


class AlertSystem:
    def __init__(self, engine, bot):

        self.engine = engine

        self.bot = bot

        self.last_signal_state = {}

        self.cooldown = 60  # seconds between alerts per symbol

        self.last_alert_time = {}

    # -----------------------------------------------------
    # MAIN LOOP
    # -----------------------------------------------------

    async def run(self):

        while True:
            try:
                await self.scan_market()

                await asyncio.sleep(10)  # هر 10 ثانیه

            except Exception as e:
                print(f"Alert error: {e}")

                await asyncio.sleep(5)

    # -----------------------------------------------------
    # SCAN MARKET
    # -----------------------------------------------------

    async def scan_market(self):

        for symbol in self.engine.symbols:
            signal = await self.engine.calculate_live_indicators(
                client=self.engine.client, symbol=symbol
            )

            await self.handle_signal(symbol, signal)

    # -----------------------------------------------------
    # HANDLE SIGNAL
    # -----------------------------------------------------

    async def handle_signal(self, symbol, signal):

        if not signal:
            return

        confidence = signal.get("confidence", 0)

        if confidence < 80:
            return  # فیلتر سیگنال ضعیف

        now = datetime.utcnow()

        # cooldown per symbol
        if symbol in self.last_alert_time:
            diff = (now - self.last_alert_time[symbol]).seconds

            if diff < self.cooldown:
                return

        previous = self.last_signal_state.get(symbol)

        current_state = "BUY" if signal["buy"] else "SELL" if signal["sell"] else "NONE"

        # اگر تغییر نکرده، پیام نده
        if previous == current_state:
            return

        self.last_signal_state[symbol] = current_state

        self.last_alert_time[symbol] = now

        # -------------------------------------------------
        # SEND ALERT
        # -------------------------------------------------

        message = f"""
🚨 NEW SIGNAL ALERT

📊 Symbol: {symbol}

🟢 BUY: {signal["buy"]}
🔴 SELL: {signal["sell"]}

🔥 Confidence: {confidence}

📈 BUY SCORE: {signal["buy_score"]}
📉 SELL SCORE: {signal["sell_score"]}

⏰ {now.strftime("%Y-%m-%d %H:%M:%S")}
"""

        await self.bot.send_message(chat_id=self.bot.chat_id, text=message)
