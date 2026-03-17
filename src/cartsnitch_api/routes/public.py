"""Public endpoints: price transparency data (no auth required)."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from cartsnitch_api.schemas import (
    PublicInflationResponse,
    PublicStoreComparisonResponse,
    PublicTrendResponse,
)

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/trends/{product_id}", response_model=PublicTrendResponse)
async def public_price_trend(product_id: UUID):
    # TODO: call service layer — public price trend for a product
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/store-comparison", response_model=PublicStoreComparisonResponse)
async def public_store_comparison(
    product_ids: list[UUID] = Query(...),
):
    # TODO: call service layer — public store-vs-store comparison
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/inflation", response_model=PublicInflationResponse)
async def public_inflation():
    # TODO: call service layer — price changes vs CPI baseline
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
