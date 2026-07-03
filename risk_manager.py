"""
risk_manager.py

Professional Risk Management System (Prop-Firm Style)
"""

from datetime import datetime, timedelta


class RiskManager:
    def __init__(self):

        # -------------------------
        # Account Limits
        # -------------------------

        self.max_daily_loss_percent = 3.0

        self.max_drawdown_percent = 10.0

        self.max_trades_per_day = 20

        self.max_consecutive_losses = 3

        self.cooldown_after_loss_sec = 300

        # -------------------------
        # Runtime State
        # -------------------------

        self.daily_start_balance = None

        self.current_balance = None

        self.daily_loss = 0.0

        self.trades_today = 0

        self.consecutive_losses = 0

        self.last_loss_time = None

    # -----------------------------------------------------
    # UPDATE BALANCE
    # -----------------------------------------------------

    def update_balance(self, balance: float):

        if self.daily_start_balance is None:
            self.daily_start_balance = balance
        if self.daily_start_balance <= 0:
            self.daily_loss = 0.0
            self.current_balance = balance
            return
        self.current_balance = balance

        self.daily_loss = (
            (self.daily_start_balance - self.current_balance) / self.daily_start_balance
        ) * 100

    # -----------------------------------------------------
    # CHECK IF CAN TRADE
    # -----------------------------------------------------

    def can_open_trade(self) -> bool:
        # 0. Balance must be initialized
        if self.current_balance is None:
            return False

        # 1. Daily loss check
        if self.daily_loss >= self.max_daily_loss_percent:
            return False

        # 2. Max trades per day
        if self.trades_today >= self.max_trades_per_day:
            return False

        # 3. Consecutive losses
        if self.consecutive_losses >= self.max_consecutive_losses:
            return False

        # 4. Cooldown after loss
        if self.last_loss_time:
            if datetime.utcnow() - self.last_loss_time < timedelta(
                seconds=self.cooldown_after_loss_sec
            ):
                return False

        return True

    # -----------------------------------------------------
    # ON TRADE RESULT
    # -----------------------------------------------------

    def on_trade_result(self, pnl: float):

        self.trades_today += 1

        if pnl < 0:
            self.consecutive_losses += 1

            self.last_loss_time = datetime.utcnow()

        else:
            self.consecutive_losses = 0

    # -----------------------------------------------------
    # RESET DAILY
    # -----------------------------------------------------

    def reset_daily(self):

        self.daily_start_balance = self.current_balance

        self.daily_loss = 0.0

        self.trades_today = 0

        self.consecutive_losses = 0

        self.last_loss_time = None

    # -----------------------------------------------------
    # POSITION SIZE
    # -----------------------------------------------------

    # -----------------------------------------------------
    # POSITION SIZE
    # -----------------------------------------------------

    def calculate_position_size(
        self,
        entry_price: float,
        stop_loss: float,
        risk_percent: float = 1.0,
    ) -> float:
        """
        Calculate position size using the latest account balance.
        """

        try:
            if self.current_balance is None:
                return 0.0

            account_balance = float(self.current_balance)

            if account_balance <= 0:
                return 0.0

            stop_distance = abs(entry_price - stop_loss)

            if stop_distance <= 0:
                return 0.0

            risk_amount = account_balance * (risk_percent / 100)

            position_size = risk_amount / stop_distance

            return max(position_size, 0.0)

        except Exception:
            return 0.0
