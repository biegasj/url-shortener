from pydantic import BaseModel, Field


class DeleteResponse(BaseModel):
    success: bool = Field(default=True)
    message: str | None = Field(default=None, max_length=256)
