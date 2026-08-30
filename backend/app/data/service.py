from app.config import (
    DEALS_BOARD_ID,
    WORK_ORDERS_BOARD_ID,
)

from app.data.normalizer import (
    normalize_deals,
    normalize_work_orders,
)

class DataService:

    def __init__(self, monday_client):
        self.monday = monday_client

        self._deals = None
        self._work_orders = None

    async def get_deals(self) -> list[dict]:
        if self._deals is None:
            raw_deals = await self.monday.get_all_items(
                DEALS_BOARD_ID
            )

            self._deals = normalize_deals(raw_deals)

        return self._deals

    async def get_work_orders(self) -> list[dict]:
        if self._work_orders is None:
            raw_work_orders = await self.monday.get_all_items(
                WORK_ORDERS_BOARD_ID
            )

            self._work_orders = normalize_work_orders(
                raw_work_orders
            )

        return self._work_orders

    async def refresh(self):
        raw_deals = await self.monday.get_all_items(
            DEALS_BOARD_ID
        )

        raw_work_orders = await self.monday.get_all_items(
            WORK_ORDERS_BOARD_ID
        )

        self._deals = normalize_deals(raw_deals)
        self._work_orders = normalize_work_orders(
            raw_work_orders
        )

    def clear_cache(self):
        self._deals = None
        self._work_orders = None