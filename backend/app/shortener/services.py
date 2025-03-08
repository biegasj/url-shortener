import secrets

import validators
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from sqlmodel import select, update

from app.core.dependencies import SessionDep
from app.shortener.models.admin_details import AdminDetails
from app.shortener.models.responses import DeleteResponse
from app.shortener.models.short_url import ShortUrl, ShortUrlCreate, ShortUrlResponse
from app.shortener.utils import generate_unique_short_path, get_full_short_url


async def create_short_url_entry(
    short_url: ShortUrlCreate,
    user_agent: str | None,
    client_host: str | None,
    session: SessionDep,
    base_url: str,
) -> ShortUrlResponse:
    if not validators.url(short_url.target_url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid target URL")

    existing_short_url = session.exec(select(ShortUrl).where(ShortUrl.target_url == short_url.target_url)).first()

    if existing_short_url:
        return ShortUrlResponse(
            **existing_short_url.model_dump(exclude={"admin_details"}),
            short_url=get_full_short_url(base_url, existing_short_url.short_path),
        )

    short_path = generate_unique_short_path(session, short_url.short_path_length)

    admin_details = AdminDetails(
        admin_key=secrets.token_urlsafe(32),
        user_agent=user_agent,
        client_host=client_host,
    )
    new_short_url = ShortUrl(
        short_path=short_path,
        target_url=short_url.target_url,
        admin_details=admin_details,
    )

    session.add(new_short_url)
    session.commit()
    session.refresh(new_short_url)

    return ShortUrlResponse(
        **new_short_url.model_dump(),
        short_url=get_full_short_url(base_url, new_short_url.short_path),
        admin_details=new_short_url.admin_details,
    )


async def handle_redirect(short_path: str, session: SessionDep) -> RedirectResponse:
    statement = select(ShortUrl).join(AdminDetails).where(ShortUrl.short_path == short_path)

    if not (short_url := session.exec(statement).first()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find short URL")

    session.exec(
        update(AdminDetails).where(AdminDetails.id == short_url.admin_details.id).values(clicks=AdminDetails.clicks + 1)
    )
    session.commit()

    return short_url.target_url


async def get_short_url_with_admin(
    short_path: str, admin_key: str, session: SessionDep, base_url: str
) -> ShortUrlResponse:
    statement = (
        select(ShortUrl)
        .join(AdminDetails)
        .where(
            ShortUrl.short_path == short_path,
            AdminDetails.admin_key == admin_key,
        )
    )

    if not (short_url := session.exec(statement).first()):
        raise HTTPException(status_code=404, detail="Invalid short path or secret key")

    return ShortUrlResponse(
        **short_url.model_dump(),
        short_url=get_full_short_url(base_url, short_url.short_path),
        admin_details=short_url.admin_details,
    )


async def delete_short_url_entry(short_path: str, admin_key: str, session: SessionDep) -> DeleteResponse:
    statement = (
        select(ShortUrl)
        .join(AdminDetails)
        .where(
            ShortUrl.short_path == short_path,
            AdminDetails.admin_key == admin_key,
        )
    )

    if not (short_url := session.exec(statement).first()):
        raise HTTPException(status_code=404, detail="Invalid short path or secret key")

    session.delete(short_url)
    session.commit()

    return DeleteResponse(success=True)
