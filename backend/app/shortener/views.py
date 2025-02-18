import secrets
from logging import getLogger

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel import select

from app.core.dependencies import SessionDep
from app.models import DeleteResponse, ShortUrl, ShortUrlCreate, ShortUrlResponse
from app.settings import Settings
from app.shortener.utils import generate_unique_short_path

logger = getLogger(__name__)
settings = Settings()

router = APIRouter()


@router.post("/shorten", response_model=ShortUrlResponse)
async def create_short_url(short_url: ShortUrlCreate, session: SessionDep):
    base_url = settings.base_url

    existing_short_url = session.exec(select(ShortUrl).where(ShortUrl.target_url == short_url.target_url)).first()
    if existing_short_url:
        return ShortUrlResponse(
            **short_url.model_dump(),
            short_url=f"{base_url}/{existing_short_url.short_path}",
        )

    short_path = generate_unique_short_path(session, short_url.short_path_length)
    new_url = ShortUrl(
        short_path=short_path,
        target_url=short_url.target_url,
        admin_key=secrets.token_urlsafe(32),
    )

    session.add(new_url)
    session.commit()
    session.refresh(new_url)

    return ShortUrlResponse(
        **new_url.model_dump(),
        short_url=f"{base_url}/{new_url.short_path}",
    )


@router.get("/{short_path}", response_class=RedirectResponse)
async def redirect_to_url(short_path: str, session: SessionDep):
    statement = select(ShortUrl).where(ShortUrl.short_path == short_path)
    short_url = session.exec(statement).scalars().first()

    if not short_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find short URL")

    short_url.clicks += 1
    session.add(short_url)
    session.commit()

    return short_url.target_url


@router.get("/admin/{short_path}", response_model=ShortUrl)
async def get_short_url_details(short_path: str, admin_key: str, session: SessionDep):
    statement = select(ShortUrl).where(ShortUrl.short_path == short_path, ShortUrl.admin_key == admin_key)
    short_url = session.exec(statement).scalars().first()

    if not short_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid short path or secret key")

    return short_url


@router.delete("/admin/{short_path}", response_model=DeleteResponse)
async def delete_short_url(short_path: str, admin_key: str, session: SessionDep):
    statement = select(ShortUrl).where(ShortUrl.short_path == short_path, ShortUrl.admin_key == admin_key)
    short_url = session.exec(statement).first()

    if not short_url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid short path or secret key")

    session.delete(short_url)
    session.commit()

    return DeleteResponse(success=True)
