from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings


if settings.DEMO_MODE:
    engine = create_engine("sqlite:///fleet_demo.db", echo=settings.APP_DEBUG)
else:
    engine = create_engine(settings.database_url, echo=settings.APP_DEBUG)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
