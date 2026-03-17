"""Product routes: search/list, detail, price history."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import PriceTrendResponse, ProductDetailResponse, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
async def list_products(
    user_id: UUID = Depends(get_current_user),
    q: str | None = Query(None),
    category: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    # TODO: call service layer — product search/list
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product(product_id: UUID, user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — product detail with cross-store prices
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/{product_id}/prices", response_model=PriceTrendResponse)
async def get_product_prices(product_id: UUID, user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — price history across stores
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
