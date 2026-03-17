"""Price service — trends, increases, comparison."""

from uuid import UUID

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class PriceService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_trends(self, category: str | None = None) -> list[dict]:
        from cartsnitch_common.models import NormalizedProduct, PriceHistory

        query = (
            select(PriceHistory)
            .join(NormalizedProduct)
            .options(
                selectinload(PriceHistory.store),
                selectinload(PriceHistory.normalized_product),
            )
            .order_by(PriceHistory.observed_date)
        )
        if category:
            query = query.where(NormalizedProduct.category == category)

        result = await self.db.execute(query)
        prices = result.scalars().all()

        # Group by product
        by_product: dict[UUID, dict] = {}
        for ph in prices:
            pid = ph.normalized_product_id
            if pid not in by_product:
                by_product[pid] = {
                    "product_id": pid,
                    "product_name": ph.normalized_product.canonical_name,
                    "data_points": [],
                }
            by_product[pid]["data_points"].append({
                "date": ph.observed_date,
                "price": float(ph.regular_price),
                "store_id": ph.store_id,
                "store_name": ph.store.name,
            })
        return list(by_product.values())

    async def get_increases(self) -> list[dict]:
        """Find products with recent significant price increases."""
        from cartsnitch_common.models import PriceHistory

        # Get latest two prices per product+store
        subq = (
            select(
                PriceHistory.normalized_product_id,
                PriceHistory.store_id,
                func.max(PriceHistory.observed_date).label("max_date"),
            )
            .group_by(PriceHistory.normalized_product_id, PriceHistory.store_id)
            .subquery()
        )

        latest_result = await self.db.execute(
            select(PriceHistory)
            .join(
                subq,
                and_(
                    PriceHistory.normalized_product_id == subq.c.normalized_product_id,
                    PriceHistory.store_id == subq.c.store_id,
                    PriceHistory.observed_date == subq.c.max_date,
                ),
            )
            .options(
                selectinload(PriceHistory.normalized_product),
                selectinload(PriceHistory.store),
            )
        )
        latest_prices = latest_result.scalars().all()

        # For each latest price, get the previous price
        increases = []
        for lp in latest_prices:
            prev_result = await self.db.execute(
                select(PriceHistory)
                .where(
                    PriceHistory.normalized_product_id == lp.normalized_product_id,
                    PriceHistory.store_id == lp.store_id,
                    PriceHistory.observed_date < lp.observed_date,
                )
                .order_by(PriceHistory.observed_date.desc())
                .limit(1)
            )
            prev = prev_result.scalar_one_or_none()
            if prev and lp.regular_price > prev.regular_price:
                old = float(prev.regular_price)
                new = float(lp.regular_price)
                increases.append({
                    "product_id": lp.normalized_product_id,
                    "product_name": lp.normalized_product.canonical_name,
                    "store_name": lp.store.name,
                    "old_price": old,
                    "new_price": new,
                    "increase_pct": round((new - old) / old * 100, 2),
                    "detected_at": lp.observed_date,
                })

        increases.sort(key=lambda x: x["increase_pct"], reverse=True)
        return increases

    async def get_comparison(self, product_ids: list[UUID]) -> list[dict]:
        from cartsnitch_common.models import NormalizedProduct, PriceHistory

        comparisons = []
        for pid in product_ids:
            prod_result = await self.db.execute(
                select(NormalizedProduct).where(NormalizedProduct.id == pid)
            )
            product = prod_result.scalar_one_or_none()
            if not product:
                continue

            # Latest price per store
            subq = (
                select(
                    PriceHistory.store_id,
                    func.max(PriceHistory.observed_date).label("max_date"),
                )
                .where(PriceHistory.normalized_product_id == pid)
                .group_by(PriceHistory.store_id)
                .subquery()
            )
            prices_result = await self.db.execute(
                select(PriceHistory)
                .join(
                    subq,
                    and_(
                        PriceHistory.store_id == subq.c.store_id,
                        PriceHistory.observed_date == subq.c.max_date,
                        PriceHistory.normalized_product_id == pid,
                    ),
                )
                .options(selectinload(PriceHistory.store))
            )
            prices = prices_result.scalars().all()

            comparisons.append({
                "product_id": pid,
                "product_name": product.canonical_name,
                "prices": [
                    {
                        "store_id": ph.store_id,
                        "store_name": ph.store.name,
                        "current_price": float(ph.regular_price),
                        "last_seen_at": ph.observed_date,
                    }
                    for ph in prices
                ],
            })
        return comparisons
