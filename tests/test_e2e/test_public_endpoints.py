"""E2E: Public price transparency endpoints (no auth required)."""

import pytest


@pytest.mark.asyncio
class TestPublicTrends:
    """Public price trend endpoint — no auth, real data."""

    async def test_public_trend_returns_data(self, client, seed_data):
        cheerios_id = str(seed_data["products"]["cheerios"].id)
        resp = await client.get(f"/public/trends/{cheerios_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["product_name"] == "Cheerios 18oz"
        assert len(data["data_points"]) >= 3

    async def test_public_trend_no_auth_needed(self, client, seed_data):
        """Confirm no Authorization header is required."""
        cheerios_id = str(seed_data["products"]["cheerios"].id)
        resp = await client.get(f"/public/trends/{cheerios_id}")
        assert resp.status_code == 200


@pytest.mark.asyncio
class TestPublicStoreComparison:
    """Public store comparison endpoint."""

    async def test_store_comparison(self, client, seed_data):
        cheerios_id = str(seed_data["products"]["cheerios"].id)
        resp = await client.get(
            "/public/store-comparison",
            params=[("product_ids", cheerios_id)],
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "products" in data
        assert len(data["products"]) >= 1


@pytest.mark.asyncio
class TestPublicInflation:
    """Public inflation index endpoint."""

    async def test_inflation_returns_index(self, client, seed_data):
        resp = await client.get("/public/inflation")
        assert resp.status_code == 200
        data = resp.json()
        assert "cartsnitch_index" in data
        assert "cpi_baseline" in data
        assert "categories" in data
