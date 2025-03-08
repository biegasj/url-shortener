import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from app.core.postgres import get_db_session
from app.main import app
from app.shortener.models import ShortUrl
from app.shortener.models.admin_details import AdminDetails


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_db_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_db_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_duplicate_target_url_returns_existing(client: TestClient, session: Session):
    target_url = "https://example.com"
    data = {"target_url": target_url}

    response1 = client.post("/shorten", json=data)
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["admin_details"] is not None

    response2 = client.post("/shorten", json=data)
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["admin_details"] is None

    assert data1["target_url"] == data2["target_url"] == target_url
    assert data1["short_path"] == data2["short_path"]

    short_urls = session.exec(select(ShortUrl)).all()
    assert len(short_urls) == 1


def test_redirect_valid_short_path(client: TestClient, session: Session):
    short_url = ShortUrl(
        short_path="abc123",
        target_url="https://example.com",
        admin_details=AdminDetails(admin_key="test", user_agent="test", client_host="test"),
    )
    session.add(short_url)
    session.commit()

    response = client.get("/abc123", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com"
    admin_details = session.get(AdminDetails, short_url.admin_details.id)
    assert admin_details.clicks == 1


def test_redirect_invalid_short_path_404(client: TestClient):
    response = client.get("/invalid")
    assert response.status_code == 404
    assert response.json()["detail"] == "Could not find short URL"


def test_redirect_increments_clicks(client, session):
    short_url = ShortUrl(
        short_path="test",
        target_url="https://example.com",
        admin_details=AdminDetails(admin_key="test", user_agent="test", client_host="test"),
    )
    session.add(short_url)
    session.commit()

    for i in range(3):
        client.get("/test")

    admin_details = session.get(AdminDetails, short_url.admin_details.id)

    assert admin_details.clicks == 3


def test_get_details_with_valid_admin_key(client: TestClient, session: Session):
    admin_key = "admin_key"
    short_url = ShortUrl(
        short_path="valid",
        target_url="https://example.com",
        admin_details=AdminDetails(admin_key=admin_key, user_agent="test", client_host="test"),
    )
    session.add(short_url)
    session.commit()

    response = client.get(f"/admin/valid?admin_key={admin_key}")

    assert response.status_code == 200
    data = response.json()
    assert data["short_path"] == "valid"
    assert data["admin_details"]["admin_key"] == admin_key


def test_get_details_with_invalid_admin_key_404(client, session):
    short_url = ShortUrl(
        short_path="valid",
        target_url="https://example.com",
        admin_details=AdminDetails(admin_key="secret123", user_agent="test", client_host="test"),
    )
    session.add(short_url)
    session.commit()

    response = client.get("/admin/valid?admin_key=wrong")

    assert response.status_code == 404
    assert response.json()["detail"] == "Invalid short path or secret key"


def test_delete_with_valid_admin_key(client: TestClient, session: Session):
    admin_key = "admin_key"
    short_url = ShortUrl(
        short_path="delete",
        target_url="https://example.com",
        admin_details=AdminDetails(admin_key=admin_key, user_agent="test", client_host="test"),
    )
    session.add(short_url)
    session.commit()

    response = client.delete(f"/admin/delete?admin_key={admin_key}")

    assert response.status_code == 200
    assert response.json() == {"success": True, "message": None}
    deleted = session.get(ShortUrl, short_url.id)
    assert deleted is None


def test_delete_with_invalid_admin_key_404(client: TestClient, session: Session):
    short_url = ShortUrl(
        short_path="delete",
        target_url="https://example.com",
        admin_details=AdminDetails(admin_key="valid", user_agent="test", client_host="test"),
    )
    session.add(short_url)
    session.commit()

    response = client.delete("/admin/delete?admin_key=invalid")

    assert response.status_code == 404


def test_deleted_url_no_longer_accessible(client: TestClient, session: Session):
    admin_key = "admin_key"
    short_url = ShortUrl(
        short_path="gone",
        target_url="https://example.com",
        admin_details=AdminDetails(admin_key=admin_key, user_agent="test", client_host="test"),
    )
    session.add(short_url)
    session.commit()

    client.delete(f"/admin/gone?admin_key={admin_key}")

    response = client.get("/gone")
    assert response.status_code == 404
