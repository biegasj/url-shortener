from datetime import datetime

from sqlmodel import Field, SQLModel


class ShortUrlBase(SQLModel):
    target_url: str = Field(max_length=2048, unique=True, nullable=False)


class ShortUrl(ShortUrlBase, table=True):
    id: int = Field(primary_key=True)
    short_path: str = Field(max_length=64, unique=True, index=True, nullable=False)
    admin_key: str = Field(max_length=128, index=True, nullable=False)
    clicks: int = Field(default=0, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class ShortUrlCreate(ShortUrlBase):
    short_path_length: int = Field(default=8, ge=8, le=64)


class ShortUrlUpdate(ShortUrlBase):
    short_path: str
    clicks: int


class ShortUrlResponse(ShortUrl):
    short_url: str = Field(max_length=2048)
    admin_key: str | None


class DeleteResponse(SQLModel):
    success: bool = Field(default=True)
    message: str | None = Field(default=None, max_length=256, nullable=True)
