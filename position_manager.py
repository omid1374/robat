"""
position_manager.py

Professional position management (Prop-Firm style)
"""

import asyncio


class PositionManager:
    def __init__(self, client, risk_manager):

        self.client = client

        self.risk_manager = risk_manager

        # -------------------------
        # Settings
        # -------------------------

        self.be_trigger = 0.01  # 1% profit → break even

        self.trailing_start = 0.02  # 2% profit → trailing start

        self.trailing_step = 0.005  # trailing step

        self.partial_close_trigger = 0.03  # 3% profit

        self.partial_close_ratio = 0.5  # 50% close

    # -----------------------------------------------------
    # MAIN UPDATE LOOP
    # -----------------------------------------------------

    async def manage(self, symbol: str):

        try:
            position = await self.client.fetch_position(symbol)

            if not position:
                return

            entry = float(position.get("entryPrice", 0))

            current = float(position.get("markPrice", 0))

            size = float(position.get("size", 0))

            side = position.get("side")

            if size == 0:
                return

            pnl_percent = (
                (current - entry) / entry
                if side == "long"
                else (entry - current) / entry
            )

            # -----------------------------------------
            # 1. BREAK EVEN
            # -----------------------------------------

            if pnl_percent >= self.be_trigger:
                await self.set_break_even(
                    symbol,
                    position,
                )

            # -----------------------------------------
            # 2. TRAILING STOP
            # -----------------------------------------

            if pnl_percent >= self.trailing_start:
                await self.apply_trailing_stop(
                    symbol,
                    position,
                    current,
                )

            # -----------------------------------------
            # 3. PARTIAL CLOSE
            # -----------------------------------------

            if pnl_percent >= self.partial_close_trigger:
                await self.partial_close(
                    symbol,
                    position,
                )

        except Exception as e:
            print(f"Position manager error: {e}")

    # -----------------------------------------------------
    # BREAK EVEN
    # -----------------------------------------------------

    async def set_break_even(self, symbol, position):

        entry = float(position["entryPrice"])

        await self.client.modify_stop_loss(
            symbol=symbol,
            stop_loss=entry,
        )

    # -----------------------------------------------------
    # TRAILING STOP
    # -----------------------------------------------------

    async def apply_trailing_stop(
        self,
        symbol,
        position,
        current_price,
    ):

        new_sl = current_price * (1 - self.trailing_step)

        await self.client.modify_stop_loss(
            symbol=symbol,
            stop_loss=new_sl,
        )

    # -----------------------------------------------------
    # PARTIAL CLOSE
    # -----------------------------------------------------

    async def partial_close(self, symbol, position):

        size = float(position["size"])

        close_size = size * self.partial_close_ratio

        await self.client.close_position_partial(
            symbol=symbol,
            size=close_size,
        )
