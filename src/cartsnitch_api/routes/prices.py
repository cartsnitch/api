"""Price routes: trends, increases, comparison."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import PriceComparisonResponse, PriceIncreaseResponse, PriceTrendResponse

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/trends", response_model=list[PriceTrendResponse])
async def price_trends(
    user_id: UUID = Depends(get_current_user),
    category: str | None = Query(None),
):
    # TODO: call service layer — aggregate price trends
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/increases", response_model=list[PriceIncreaseResponse])
async def price_increases(user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — recent significant price increases
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/comparison", response_model=list[PriceComparisonResponse])
async def price_comparison(
    product_ids: list[UUID] = Query(...),
    user_id: UUID = Depends(get_current_user),
):
    # TODO: call service layer — compare items across stores
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
