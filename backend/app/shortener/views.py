from app.shortener.models import DeleteShortUrlResponse, SecretKeyRequestBody, ShortUrlResponse
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

url_storage = {}


@router.post("/shorten", response_model=ShortUrlResponse)
async def create_short_url() -> ShortUrlResponse:
    return ShortUrlResponse(
        short_url_key="abc123",
        full_short_url="https://short.ly/abc123",
        target_url="https://example.com",
        secret_key="mysecret",
        admin_url="https://short.ly/admin/abc123",
        clicks=42,
        created_at="2024-02-17T12:00:00Z",
    )


@router.get("/redirect/{url_key}", response_class=RedirectResponse)
async def redirect_to_url(url_key: str) -> RedirectResponse:
    return RedirectResponse(url="https://example.com")


@router.post("/admin/{url_key}", response_model=ShortUrlResponse)
async def get_short_url(url_key: str, secret_key_request: SecretKeyRequestBody) -> ShortUrlResponse:
    return ShortUrlResponse(
        short_url_key="abc123",
        full_short_url="https://short.ly/abc123",
        target_url="https://example.com",
        secret_key="mysecret",
        admin_url="https://short.ly/admin/abc123",
        clicks=42,
        created_at="2024-02-17T12:00:00Z",
    )


@router.delete("/admin/{url_key}", response_model=DeleteShortUrlResponse)
async def delete_short_url(url_key: str, secret_key_request: SecretKeyRequestBody):
    return DeleteShortUrlResponse(success=True)
