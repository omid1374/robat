"""
risk_manager.py

مدیریت ریسک ربات BloFin
"""

import logging
from datetime import datetime, timedelta

from exchange import client
from config import (
    SYMBOL,
    MAX_INVENTORY,
    MAX_ALLOWED_LOSS,
    COOLDOWN_MINUTES,
)

logger = logging.getLogger(__name__)


class RiskManager:
    def __init__(self):

        self.cooldown_until = datetime.min

    # -------------------------
    # Cooldown
    # -------------------------

    @property
    def in_cooldown(self):

        return datetime.utcnow() < self.cooldown_until

    def start_cooldown(self):

        self.cooldown_until = datetime.utcnow() + timedelta(minutes=COOLDOWN_MINUTES)

        logger.warning(f"Cooldown started until {self.cooldown_until}")

    # -------------------------
    # دریافت پوزیشن
    # -------------------------

    async def get_position(self):

        positions = await client.fetch_positions(SYMBOL)

        if not positions:
            return None

        for pos in positions:
            contracts = pos.get("contracts")

            if contracts is None:
                continue

            if float(contracts) == 0:
                continue

            return pos

        return None

    # -------------------------
    # موجودی پوزیشن
    # -------------------------

    async def inventory(self):

        pos = await self.get_position()

        if pos is None:
            return 0.0

        size = float(pos["contracts"])

        side = pos["side"].lower()

        if side == "long":
            return size

        return -size

    # -------------------------
    # سود و زیان
    # -------------------------

    async def unrealized_pnl(self):

        pos = await self.get_position()

        if pos is None:
            return 0.0

        pnl = pos.get("unrealizedPnl", 0)

        return float(pnl)

    # -------------------------
    # بررسی حد ضرر
    # -------------------------

    async def stop_loss_hit(self):

        pnl = await self.unrealized_pnl()

        return pnl <= -MAX_ALLOWED_LOSS

    # -------------------------
    # هج اضطراری
    # -------------------------

    async def hedge_position(self):

        pos = await self.get_position()

        if pos is None:
            return

        size = float(pos["contracts"])

        if size == 0:
            return

        side = pos["side"].lower()

        hedge_side = "sell" if side == "long" else "buy"

        logger.warning(f"Hedge -> {hedge_side} {size}")

        await client.create_market_order(
            symbol=SYMBOL,
            side=hedge_side,
            amount=size,
        )

    # -------------------------
    # کنترل حجم
    # -------------------------

    async def inventory_limit_hit(self):

        inv = abs(await self.inventory())

        return inv >= MAX_INVENTORY

    # -------------------------
    # مدیریت ریسک
    # -------------------------

    async def evaluate(self):

        if self.in_cooldown:
            return False

        if await self.stop_loss_hit():
            logger.error("Emergency Stop Loss Triggered")

            await self.hedge_position()

            self.start_cooldown()

            return False

        if await self.inventory_limit_hit():
            logger.warning("Inventory Limit Exceeded")

            await self.hedge_position()

        return True


risk_manager = RiskManager()
