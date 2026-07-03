"""
core/balance_service.py
"""

from datetime import datetime
from typing import Dict, Any

# این import را با کلاس صرافی پروژه خودت جایگزین کن
# مثال:
# from exchange.exchange import ExchangeClient


class BalanceService:
    def __init__(self, exchange):
        self.exchange = exchange

        self._cache: Dict[str, Any] = {}
        self._last_update = None

    async def get_balance(self):

        balance = await self.exchange.fetch_balance()

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "wallet_balance": float(balance.get("totalWalletBalance", 0)),
            "available_balance": float(balance.get("availableBalance", 0)),
            "equity": float(balance.get("equity", 0)),
            "unrealized_pnl": float(balance.get("unrealizedProfit", 0)),
            "margin_balance": float(balance.get("marginBalance", 0)),
        }

        self._cache = result
        self._last_update = datetime.utcnow()

        return result

    async def cached_balance(self):

        if not self._cache:
            return await self.get_balance()

        return self._cache
