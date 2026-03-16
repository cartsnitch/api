"""HTTP client for ClipArtist internal API."""

import httpx

from cartsnitch_api.config import settings


class ClipArtistClient:
    def __init__(self) -> None:
        self.base_url = settings.clipartist_url
        self.headers = {"X-Service-Key": settings.service_key}

    async def optimize_shopping(self, items: list[dict], preferred_stores: list[str] | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/optimize",
                headers=self.headers,
                json={"items": items, "preferred_stores": preferred_stores},
            )
            resp.raise_for_status()
            return resp.json()

    async def get_relevant_coupons(self, user_id: str) -> list[dict]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/coupons/relevant",
                headers=self.headers,
                params={"user_id": user_id},
            )
            resp.raise_for_status()
            return resp.json()
