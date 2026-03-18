"""Pydantic v2 schemas for data contracts (ORM Create/Read models).

These schemas define the shared data contracts used by the pipeline
and inter-service communication. They complement the API-facing response
schemas in cartsnitch_api.schemas.
"""

from cartsnitch_api.data_schemas.coupon import CouponCreate, CouponRead
from cartsnitch_api.data_schemas.events import EventEnvelope
from cartsnitch_api.data_schemas.price import PriceHistoryCreate, PriceHistoryRead
from cartsnitch_api.data_schemas.product import NormalizedProductCreate, NormalizedProductRead
from cartsnitch_api.data_schemas.purchase import (
    PurchaseCreate,
    PurchaseItemCreate,
    PurchaseItemRead,
    PurchaseRead,
)
from cartsnitch_api.data_schemas.shrinkflation import ShrinkflationEventCreate, ShrinkflationEventRead
from cartsnitch_api.data_schemas.store import (
    StoreCreate,
    StoreLocationCreate,
    StoreLocationRead,
    StoreRead,
)
from cartsnitch_api.data_schemas.user import (
    UserCreate,
    UserRead,
    UserStoreAccountCreate,
    UserStoreAccountRead,
)

__all__ = [
    "StoreCreate",
    "StoreRead",
    "StoreLocationCreate",
    "StoreLocationRead",
    "UserCreate",
    "UserRead",
    "UserStoreAccountCreate",
    "UserStoreAccountRead",
    "PurchaseCreate",
    "PurchaseRead",
    "PurchaseItemCreate",
    "PurchaseItemRead",
    "NormalizedProductCreate",
    "NormalizedProductRead",
    "PriceHistoryCreate",
    "PriceHistoryRead",
    "CouponCreate",
    "CouponRead",
    "ShrinkflationEventCreate",
    "ShrinkflationEventRead",
    "EventEnvelope",
]
