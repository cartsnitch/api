"""Alert routes: list alerts, manage settings."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import AlertResponse, AlertSettingsRequest, AlertSettingsResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
async def list_alerts(user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — user's price/shrinkflation alerts
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.put("/settings", response_model=AlertSettingsResponse)
async def update_alert_settings(
    body: AlertSettingsRequest,
    user_id: UUID = Depends(get_current_user),
):
    # TODO: call service layer — update alert thresholds
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
