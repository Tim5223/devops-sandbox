import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
async def client():
    # Override the database dependency before importing the app
    with patch("app.database.create_async_engine") as mock_engine, \
         patch("app.database.async_sessionmaker") as mock_session_maker:

        mock_engine.return_value = MagicMock()
        mock_session = AsyncMock()
        mock_session_maker.return_value = MagicMock()

        from app.main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            yield c


# ── Health check ──────────────────────────────────────────────
@pytest.mark.asyncio
async def test_health():
    with patch("app.database.create_async_engine") as mock_engine, \
         patch("app.database.async_sessionmaker"):
        mock_engine.return_value = MagicMock()

        from app.main import app
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── Assets ────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_list_assets_returns_list():
    with patch("app.database.create_async_engine") as mock_engine, \
         patch("app.database.async_sessionmaker"), \
         patch("app.api.routers.assets.get_db") as mock_get_db:

        mock_engine.return_value = MagicMock()

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute = AsyncMock(return_value=mock_result)

        async def override_get_db():
            yield mock_session

        mock_get_db.side_effect = override_get_db

        from app.main import app
        app.dependency_overrides = {}

        from app.database import get_db
        app.dependency_overrides[get_db] = override_get_db

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/assets/")

        app.dependency_overrides = {}

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── Employees ─────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_list_employees_returns_list():
    with patch("app.database.create_async_engine") as mock_engine, \
         patch("app.database.async_sessionmaker"):

        mock_engine.return_value = MagicMock()

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute = AsyncMock(return_value=mock_result)

        async def override_get_db():
            yield mock_session

        from app.main import app
        from app.database import get_db
        app.dependency_overrides[get_db] = override_get_db

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/employees/")

        app.dependency_overrides = {}

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── Departments ───────────────────────────────────────────────
@pytest.mark.asyncio
async def test_list_departments_returns_list():
    with patch("app.database.create_async_engine") as mock_engine, \
         patch("app.database.async_sessionmaker"):

        mock_engine.return_value = MagicMock()

        mock_session = AsyncMock()
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute = AsyncMock(return_value=mock_result)

        async def override_get_db():
            yield mock_session

        from app.main import app
        from app.database import get_db
        app.dependency_overrides[get_db] = override_get_db

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/api/v1/departments/")

        app.dependency_overrides = {}

    assert response.status_code == 200
    assert isinstance(response.json(), list)