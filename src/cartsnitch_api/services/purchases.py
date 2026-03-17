"""Purchase service — list, detail, stats."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class PurchaseService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_purchases(
        self,
        user_id: UUID,
        store_id: UUID | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[dict]:
        from cartsnitch_common.models import Purchase, PurchaseItem

        query = (
            select(Purchase)
            .where(Purchase.user_id == user_id)
            .options(selectinload(Purchase.store))
        )
        if store_id:
            query = query.where(Purchase.store_id == store_id)

        query = query.order_by(Purchase.purchase_date.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        purchases = result.scalars().all()

        out = []
        for p in purchases:
            item_count_result = await self.db.execute(
                select(func.count()).where(PurchaseItem.purchase_id == p.id)
            )
            item_count = item_count_result.scalar()
            out.append({
                "id": p.id,
                "store_id": p.store_id,
                "store_name": p.store.name,
                "purchased_at": p.purchase_date,
                "total": float(p.total),
                "item_count": item_count,
            })
        return out

    async def get_purchase(self, purchase_id: UUID, user_id: UUID) -> dict:
        from cartsnitch_common.models import Purchase

        result = await self.db.execute(
            select(Purchase)
            .where(Purchase.id == purchase_id, Purchase.user_id == user_id)
            .options(selectinload(Purchase.store), selectinload(Purchase.items))
        )
        purchase = result.scalar_one_or_none()
        if not purchase:
            raise LookupError("Purchase not found")

        return {
            "id": purchase.id,
            "store_id": purchase.store_id,
            "store_name": purchase.store.name,
            "purchased_at": purchase.purchase_date,
            "total": float(purchase.total),
            "item_count": len(purchase.items),
            "line_items": [
                {
                    "id": item.id,
                    "product_id": item.normalized_product_id,
                    "name": item.product_name_raw,
                    "quantity": float(item.quantity),
                    "unit_price": float(item.unit_price),
                    "total_price": float(item.extended_price),
                }
                for item in purchase.items
            ],
        }

    async def get_stats(self, user_id: UUID) -> dict:
        from cartsnitch_common.models import Purchase

        result = await self.db.execute(
            select(Purchase)
            .where(Purchase.user_id == user_id)
            .options(selectinload(Purchase.store))
        )
        purchases = result.scalars().all()

        total_spent = sum(float(p.total) for p in purchases)
        by_store: dict[str, float] = {}
        by_period: dict[str, float] = {}

        for p in purchases:
            store_name = p.store.name
            by_store[store_name] = by_store.get(store_name, 0) + float(p.total)
            period = p.purchase_date.strftime("%Y-%m")
            by_period[period] = by_period.get(period, 0) + float(p.total)

        return {
            "total_spent": total_spent,
            "purchase_count": len(purchases),
            "by_store": by_store,
            "by_period": by_period,
        }
