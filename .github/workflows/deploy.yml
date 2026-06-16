import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


# ── Health check ──────────────────────────────────────────────
@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── Assets ────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_list_assets_returns_list(client):
    with patch("app.api.routers.assets.get_db") as mock_db:
        mock_session = AsyncMock()
        mock_session.execute.return_value.scalars.return_value.all.return_value = []
        mock_db.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_db.return_value.__aexit__ = AsyncMock(return_value=False)

        response = await client.get("/api/v1/assets/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# ── Employees ─────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_list_employees_returns_list(client):
    with patch("app.api.routers.employees.get_db") as mock_db:
        mock_session = AsyncMock()
        mock_session.execute.return_value.scalars.return_value.all.return_value = []
        mock_db.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_db.return_value.__aexit__ = AsyncMock(return_value=False)

        response = await client.get("/api/v1/employees/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# ── Departments ───────────────────────────────────────────────
@pytest.mark.asyncio
async def test_list_departments_returns_list(client):
    with patch("app.api.routers.other.get_db") as mock_db:
        mock_session = AsyncMock()
        mock_session.execute.return_value.scalars.return_value.all.return_value = []
        mock_db.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_db.return_value.__aexit__ = AsyncMock(return_value=False)

        response = await client.get("/api/v1/departments/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)