"""HTTP client for ReceiptWitness internal API."""

import httpx

from cartsnitch_api.config import settings


class ReceiptWitnessClient:
    def __init__(self) -> None:
        self.base_url = settings.receiptwitness_url
        self.headers = {"X-Service-Key": settings.service_key}

    async def trigger_sync(self, user_id: str, store_slug: str) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/sync/{store_slug}",
                headers=self.headers,
                json={"user_id": user_id},
            )
            resp.raise_for_status()
            return resp.json()

    async def get_sync_status(self, user_id: str) -> list[dict]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/sync/status",
                headers=self.headers,
                params={"user_id": user_id},
            )
            resp.raise_for_status()
            return resp.json()
