"""Shopping routes: optimize list, saved lists."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import OptimizeRequest, OptimizeResponse, ShoppingListResponse

router = APIRouter(prefix="/shopping", tags=["shopping"])


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_shopping(body: OptimizeRequest, user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — proxy to ClipArtist for optimization
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/lists", response_model=list[ShoppingListResponse])
async def list_shopping_lists(user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — user's saved shopping lists
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
