import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import settings
from app.models.database import Base, engine, SessionLocal
from app.services.demo_data import seed_demo_data
from app.routes import api_router, pages_router

app = FastAPI(
    title="Firma-365 | Monitoreo de Flota",
    description="Sistema de monitoreo de flota con KPIs - Datos de DQD",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(api_router)
app.include_router(pages_router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    if settings.DEMO_MODE:
        db = SessionLocal()
        try:
            seed_demo_data(db)
        finally:
            db.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
    )
