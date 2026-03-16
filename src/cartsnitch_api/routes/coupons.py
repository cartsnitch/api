"""Coupon routes: browse, relevant matches."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import CouponResponse

router = APIRouter(prefix="/coupons", tags=["coupons"])


@router.get("", response_model=list[CouponResponse])
async def list_coupons(
    store_id: UUID | None = Query(None),
    user_id: UUID = Depends(get_current_user),
):
    # TODO: call service layer — active coupons/deals
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/relevant", response_model=list[CouponResponse])
async def relevant_coupons(user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — coupons relevant to user's purchase history
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
