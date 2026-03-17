"""Store routes: list stores, manage user store connections."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import ConnectStoreRequest, StoreAccountResponse, StoreResponse

router = APIRouter(tags=["stores"])


@router.get("/stores", response_model=list[StoreResponse])
async def list_stores():
    # TODO: call service layer — list supported stores
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/me/stores", response_model=list[StoreAccountResponse])
async def list_user_stores(user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — list user's connected store accounts
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post(
    "/me/stores/{store_slug}/connect",
    response_model=StoreAccountResponse,
    status_code=status.HTTP_201_CREATED,
)
async def connect_store(
    store_slug: str,
    body: ConnectStoreRequest,
    user_id: UUID = Depends(get_current_user),
):
    # TODO: call service layer — initiate store connection
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.delete("/me/stores/{store_slug}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_store(store_slug: str, user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — disconnect store account
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
