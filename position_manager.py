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
        self.break_even_done = {}

        # آخرین Stop Loss ثبت‌شده برای هر نماد
        self.trailing_stop_price = {}

        self.partial_closed = {}

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

            if pnl_percent >= self.be_trigger and not self.break_even_done.get(
                symbol, False
            ):
                await self.set_break_even(
                    symbol,
                    position,
                )

                self.break_even_done[symbol] = True

            # -----------------------------------------
            # 2. TRAILING STOP
            # -----------------------------------------

            if pnl_percent >= self.trailing_start and not self.trailing_active.get(
                symbol, False
            ):
                await self.apply_trailing_stop(
                    symbol,
                    position,
                    current,
                )

                self.trailing_active[symbol] = True

            # -----------------------------------------
            # 3. PARTIAL CLOSE
            # -----------------------------------------

            if (
                pnl_percent >= self.partial_close_trigger
                and not self.partial_closed.get(symbol, False)
            ):
                await self.partial_close(
                    symbol,
                    position,
                )

                self.partial_closed[symbol] = True

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
        """
        Move Stop Loss only if it improves the current trailing stop.
        """

        try:
            side = position.get("side")

            if side == "long":
                new_sl = current_price * (1 - self.trailing_step)

                previous_sl = self.trailing_stop_price.get(symbol)

                if previous_sl is not None and new_sl <= previous_sl:
                    return

            else:
                new_sl = current_price * (1 + self.trailing_step)

                previous_sl = self.trailing_stop_price.get(symbol)

                if previous_sl is not None and new_sl >= previous_sl:
                    return

            new_sl = await self.client.price_to_precision(
                symbol,
                new_sl,
            )

            await self.client.modify_stop_loss(
                symbol=symbol,
                stop_loss=new_sl,
            )

            self.trailing_stop_price[symbol] = new_sl

        except Exception:
            raise

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

    def reset_symbol_state(
        self,
        symbol: str,
    ):
        """
        Reset all runtime state for a closed position.
        """

        self.break_even_done.pop(
            symbol,
            None,
        )

        self.partial_closed.pop(
            symbol,
            None,
        )

        self.trailing_stop_price.pop(
            symbol,
            None,
        )
