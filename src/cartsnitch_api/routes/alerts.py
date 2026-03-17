"""Alert routes: list alerts, manage settings."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.database import get_db
from cartsnitch_api.schemas import AlertResponse, AlertSettingsRequest, AlertSettingsResponse
from cartsnitch_api.services.alerts import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
async def list_alerts(
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AlertService(db)
    return await svc.list_alerts(user_id)


@router.put("/settings", response_model=AlertSettingsResponse)
async def update_alert_settings(
    body: AlertSettingsRequest,
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AlertService(db)
    return await svc.update_settings(
        user_id,
        price_increase_threshold_pct=body.price_increase_threshold_pct,
        shrinkflation_enabled=body.shrinkflation_enabled,
        email_notifications=body.email_notifications,
    )
