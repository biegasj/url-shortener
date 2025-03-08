from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.admin_details import AdminDetails


class ShortUrlBase(SQLModel):
    target_url: str = Field(max_length=2048, unique=True, nullable=False)


class ShortUrl(ShortUrlBase, table=True):
    id: int = Field(primary_key=True)
    short_path: str = Field(max_length=64, unique=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now())

    admin_details: Optional["AdminDetails"] = Relationship(
        back_populates="short_url", cascade_delete=True, sa_relationship_kwargs={"uselist": False}
    )


class ShortUrlCreate(ShortUrlBase):
    short_path_length: int = Field(default=8, ge=8, le=64)


class ShortUrlResponse(ShortUrlBase):
    short_path: str
    short_url: str
    admin_details: Optional[AdminDetails] = None
