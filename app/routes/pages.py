from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.services.kpi_service import KPIService

router = APIRouter(tags=["Pages"])
templates = Jinja2Templates(directory="app/templates")


def get_kpi_service(db: Session = Depends(get_db)) -> KPIService:
    return KPIService(db)


@router.get("/")
def dashboard(request: Request, kpi: KPIService = Depends(get_kpi_service)):
    data = kpi.dashboard_completo()
    return templates.TemplateResponse("pages/dashboard.html", {
        "request": request,
        "data": data,
        "page": "dashboard",
    })


@router.get("/vehiculos")
def vehiculos(request: Request, kpi: KPIService = Depends(get_kpi_service)):
    data = {
        "utilizacion": kpi.utilizacion_vehiculos(),
        "kilometraje": kpi.kilometraje(),
        "taller": kpi.vehiculos_en_taller(),
    }
    return templates.TemplateResponse("pages/vehiculos.html", {
        "request": request,
        "data": data,
        "page": "vehiculos",
    })


@router.get("/mantenimiento")
def mantenimiento(request: Request, kpi: KPIService = Depends(get_kpi_service)):
    data = {
        "mantenimientos": kpi.mantenimientos_ratio(),
        "mtbf": kpi.mtbf(),
        "mttr": kpi.mttr(),
        "taller": kpi.vehiculos_en_taller(),
    }
    return templates.TemplateResponse("pages/mantenimiento.html", {
        "request": request,
        "data": data,
        "page": "mantenimiento",
    })


@router.get("/costos-page")
def costos_page(request: Request, kpi: KPIService = Depends(get_kpi_service)):
    data = {
        "costos": kpi.costos_operacion(),
        "combustible": kpi.consumo_combustible(),
        "costo_km": kpi.costo_por_kilometro(),
    }
    return templates.TemplateResponse("pages/costos.html", {
        "request": request,
        "data": data,
        "page": "costos",
    })


@router.get("/seguridad")
def seguridad(request: Request, kpi: KPIService = Depends(get_kpi_service)):
    data = {
        "siniestralidad": kpi.indice_siniestralidad(),
        "conductores": kpi.rendimiento_conductores(),
        "alertas": kpi.alertas_vencimiento(),
        "documentacion": kpi.estado_documentacion(),
    }
    return templates.TemplateResponse("pages/seguridad.html", {
        "request": request,
        "data": data,
        "page": "seguridad",
    })
