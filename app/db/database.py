"""
Database connection — connects to the shared PostgreSQL instance
that the gateway uses for user/API-key management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Generator

from app.core.config import settings

# SQLAlchemy 2.1 defaults "postgresql://" to psycopg (v3); we ship psycopg2.
_url = settings.DATABASE_URL
for _prefix in ("postgres://", "postgresql://"):
    if _url.startswith(_prefix):
        _url = "postgresql+psycopg2://" + _url[len(_prefix):]
        break

engine = create_engine(
    _url,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
