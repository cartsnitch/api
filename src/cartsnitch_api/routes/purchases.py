"""Purchase routes: list, detail, stats."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import PurchaseDetailResponse, PurchaseResponse, PurchaseStatsResponse

router = APIRouter(prefix="/purchases", tags=["purchases"])


@router.get("", response_model=list[PurchaseResponse])
async def list_purchases(
    user_id: UUID = Depends(get_current_user),
    store_id: UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    # TODO: call service layer — paginated purchase list
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/stats", response_model=PurchaseStatsResponse)
async def purchase_stats(user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — spending summary
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{purchase_id}", response_model=PurchaseDetailResponse)
async def get_purchase(purchase_id: UUID, user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — purchase detail with line items
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
