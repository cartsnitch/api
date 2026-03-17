from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "CARTSNITCH_"}

    database_url: str = "postgresql+asyncpg://cartsnitch:cartsnitch@localhost:5432/cartsnitch"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    service_key: str = "change-me-in-production"
    fernet_key: str = "change-me-in-production-generate-with-Fernet.generate_key"

    cors_origins: list[str] = ["http://localhost:3000", "https://cartsnitch.com"]

    receiptwitness_url: str = "http://receiptwitness:8001"
    stickershock_url: str = "http://stickershock:8002"
    clipartist_url: str = "http://clipartist:8003"
    shrinkray_url: str = "http://shrinkray:8004"

    rate_limit_requests: int = 60
    rate_limit_window_seconds: int = 60


settings = Settings()
