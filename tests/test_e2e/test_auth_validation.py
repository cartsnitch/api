"""E2E: Auth and token validation flows."""

import pytest


@pytest.mark.asyncio
class TestAuthRegistrationLogin:
    """Full registration → login → token refresh → profile flow."""

    async def test_full_auth_lifecycle(self, client, db_engine):
        """Register → login → get profile → refresh → get profile again."""
        # Register
        reg = await client.post(
            "/auth/register",
            json={
                "email": "lifecycle@example.com",
                "password": "securepass123",
                "display_name": "Lifecycle User",
            },
        )
        assert reg.status_code == 201
        tokens = reg.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"
        assert tokens["expires_in"] > 0

        headers = {"Authorization": f"Bearer {tokens['access_token']}"}

        # Get profile with access token
        me = await client.get("/auth/me", headers=headers)
        assert me.status_code == 200
        assert me.json()["email"] == "lifecycle@example.com"
        assert me.json()["display_name"] == "Lifecycle User"

        # Login with same credentials
        login = await client.post(
            "/auth/login",
            json={"email": "lifecycle@example.com", "password": "securepass123"},
        )
        assert login.status_code == 200
        login_tokens = login.json()
        assert login_tokens["access_token"] != tokens["access_token"]

        # Refresh token
        refresh = await client.post(
            "/auth/refresh",
            json={"refresh_token": tokens["refresh_token"]},
        )
        assert refresh.status_code == 200
        new_tokens = refresh.json()
        assert new_tokens["access_token"] != tokens["access_token"]

        # Use refreshed token to access profile
        new_headers = {"Authorization": f"Bearer {new_tokens['access_token']}"}
        me2 = await client.get("/auth/me", headers=new_headers)
        assert me2.status_code == 200
        assert me2.json()["email"] == "lifecycle@example.com"


@pytest.mark.asyncio
class TestTokenValidation:
    """Token edge cases and error responses."""

    async def test_expired_token_rejected(self, client, db_engine):
        """Manually craft an expired token and verify rejection."""
        import uuid
        from datetime import UTC, datetime, timedelta

        from jose import jwt

        from cartsnitch_api.config import settings

        payload = {
            "sub": str(uuid.uuid4()),
            "exp": datetime.now(UTC) - timedelta(minutes=5),
            "type": "access",
        }
        token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        resp = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 401

    async def test_invalid_token_rejected(self, client, db_engine):
        resp = await client.get(
            "/auth/me", headers={"Authorization": "Bearer not-a-real-token"}
        )
        assert resp.status_code == 401

    async def test_missing_auth_header(self, client, db_engine):
        resp = await client.get("/auth/me")
        assert resp.status_code in (401, 403)

    async def test_refresh_token_cannot_access_endpoints(self, client, db_engine):
        """A refresh token should not work as an access token."""
        reg = await client.post(
            "/auth/register",
            json={
                "email": "refresh-test@example.com",
                "password": "securepass123",
                "display_name": "Refresh Test",
            },
        )
        refresh_token = reg.json()["refresh_token"]
        resp = await client.get(
            "/auth/me", headers={"Authorization": f"Bearer {refresh_token}"}
        )
        assert resp.status_code == 401

    async def test_deleted_user_token_invalid(self, client, db_engine):
        """After deleting an account, tokens should no longer work."""
        reg = await client.post(
            "/auth/register",
            json={
                "email": "delete-me@example.com",
                "password": "securepass123",
                "display_name": "Delete Me",
            },
        )
        tokens = reg.json()
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}

        # Delete account
        delete_resp = await client.delete("/auth/me", headers=headers)
        assert delete_resp.status_code == 204

        # Profile should fail
        me = await client.get("/auth/me", headers=headers)
        assert me.status_code in (401, 404)


@pytest.mark.asyncio
class TestAuthProtectedEndpoints:
    """Verify auth is enforced on all user-specific endpoints."""

    @pytest.mark.parametrize(
        "method,path",
        [
            ("GET", "/purchases"),
            ("GET", "/products"),
            ("GET", "/prices/trends"),
            ("GET", "/prices/increases"),
            ("GET", "/coupons"),
            ("GET", "/alerts"),
            ("GET", "/me/stores"),
        ],
    )
    async def test_endpoints_require_auth(self, client, db_engine, method, path):
        resp = await client.request(method, path)
        assert resp.status_code in (401, 403), f"{method} {path} should require auth"
