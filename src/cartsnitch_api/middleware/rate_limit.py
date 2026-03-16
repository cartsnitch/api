"""Rate limiting middleware stub for public endpoints."""

from fastapi import FastAPI


def add_rate_limit_middleware(app: FastAPI) -> None:
    # TODO: implement rate limiting using Redis sliding window
    # Target: settings.rate_limit_requests per settings.rate_limit_window_seconds
    # Apply only to /public/* routes
    pass
