from sqlmodel import Field, Relationship, SQLModel


class AdminDetailsBase(SQLModel):
    short_url_id: int = Field(foreign_key="shorturl.id", unique=True)


class AdminDetails(AdminDetailsBase, table=True):
    id: int = Field(primary_key=True)
    admin_key: str = Field(max_length=128, index=True, nullable=False)
    clicks: int = Field(default=0, nullable=False)
    user_agent: str | None = Field(default=None, max_length=256, nullable=True)
    client_host: str | None = Field(default=None, max_length=64, nullable=True)

    short_url: "ShortUrl" = Relationship(back_populates="admin_details")
