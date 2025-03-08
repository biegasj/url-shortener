from typing import Annotated

from fastapi import APIRouter, Header, Request
from fastapi.responses import RedirectResponse

from app.core.dependencies import SessionDep
from app.settings import Settings
from app.shortener.models.responses import DeleteResponse
from app.shortener.models.short_url import ShortUrlCreate, ShortUrlResponse
from app.shortener.services import (
    create_short_url_entry,
    delete_short_url_entry,
    get_short_url_with_admin,
    handle_redirect,
)

settings = Settings()

router = APIRouter()


@router.post("/shorten", response_model=ShortUrlResponse)
async def create_short_url(
    short_url: ShortUrlCreate, user_agent: Annotated[str | None, Header()], request: Request, session: SessionDep
):
    return await create_short_url_entry(
        short_url=short_url,
        user_agent=user_agent,
        client_host=request.client.host,
        session=session,
        base_url=settings.base_url,
    )


@router.get("/{short_path}", response_class=RedirectResponse)
async def redirect_to_url(short_path: str, session: SessionDep):
    return await handle_redirect(short_path, session)


@router.get("/admin/{short_path}", response_model=ShortUrlResponse)
async def get_short_url_details(short_path: str, admin_key: str, session: SessionDep):
    return await get_short_url_with_admin(
        short_path=short_path, admin_key=admin_key, session=session, base_url=settings.base_url
    )


@router.delete("/admin/{short_path}", response_model=DeleteResponse)
async def delete_short_url(short_path: str, admin_key: str, session: SessionDep):
    return await delete_short_url_entry(short_path=short_path, admin_key=admin_key, session=session)
