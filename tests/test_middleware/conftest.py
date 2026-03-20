"""Conftest for middleware tests — overrides global rate-limit disable."""

import pytest

from cartsnitch_api.config import settings as cartsnitch_settings


@pytest.fixture(autouse=True)
def disable_rate_limiting():
    """Middleware tests need rate limiting active — override the global disable."""
    cartsnitch_settings.rate_limit_enabled = True
    yield
    cartsnitch_settings.rate_limit_enabled = True
