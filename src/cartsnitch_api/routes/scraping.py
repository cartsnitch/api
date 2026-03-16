"""Scraping routes: trigger sync, check status (proxy to ReceiptWitness)."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import SyncStatusResponse, SyncTriggerResponse

router = APIRouter(prefix="/scraping", tags=["scraping"])


@router.post("/{store_slug}/sync", response_model=SyncTriggerResponse)
async def trigger_sync(store_slug: str, user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — proxy to ReceiptWitness
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/status", response_model=list[SyncStatusResponse])
async def sync_status(user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — sync status across all stores
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
