from pydantic import BaseModel


class ShortUrlResponse(BaseModel):
    short_url_key: str
    full_short_url: str
    target_url: str
    secret_key: str
    admin_url: str
    clicks: int = 0
    created_at: str


class RedirectToTargetUrlResponse(BaseModel):
    target_url: str


class SecretKeyRequestBody(BaseModel):
    secret_key: str


class DeleteShortUrlResponse(BaseModel):
    success: bool
