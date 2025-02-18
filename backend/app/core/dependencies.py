from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.core.postgres import get_db_session

SessionDep = Annotated[Session, Depends(get_db_session)]
