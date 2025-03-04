import secrets
import string

from fastapi import HTTPException, status
from sqlmodel import select

from app.models.short_url import ShortUrl


def get_full_short_url(base_url: str, short_path: str) -> str:
    """Generate the full short URL from the base URL and short path."""
    return f"{base_url}/{short_path}"


def generate_random_string(length: int, alphabet: str = string.ascii_lowercase + string.digits) -> str:
    """Generate a random string of the given length using the given alphabet."""
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_unique_short_path(session, length, max_attempts: int = 10) -> str:
    """Generate a unique short path within the given number of attempts."""
    for _ in range(max_attempts):
        short_path = generate_random_string(length)
        if not session.exec(select(ShortUrl).where(ShortUrl.short_path == short_path)).first():
            return short_path
    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to generate unique short key")
