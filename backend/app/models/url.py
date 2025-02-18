from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.types import timestamp


class UrlOrm(Base):
    __tablename__ = "url"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_url_key: Mapped[str] = mapped_column(String(25), unique=True, index=True, nullable=False)
    target_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    secret_key: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    admin_url: Mapped[str] = mapped_column(String(100), nullable=False)
    clicks: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[timestamp] = map

    def __repr__(self):
        return f"<URL(short_url_key='{self.short_url_key}', target_url='{self.target_url}')>"
