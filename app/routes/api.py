from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.services.kpi_service import KPIService

router = APIRouter(prefix="/api", tags=["KPIs"])


def get_kpi_service(db: Session = Depends(get_db)) -> KPIService:
    return KPIService(db)


@router.get("/dashboard")
def dashboard_completo(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.dashboard_completo()


@router.get("/resumen")
def resumen(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.resumen_flota()


@router.get("/disponibilidad")
def disponibilidad(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.disponibilidad_flota()


@router.get("/utilizacion")
def utilizacion(dias: int = 30, kpi: KPIService = Depends(get_kpi_service)):
    return kpi.utilizacion_vehiculos(dias)


@router.get("/kilometraje")
def kilometraje(dias: int = 30, kpi: KPIService = Depends(get_kpi_service)):
    return kpi.kilometraje(dias)


@router.get("/combustible")
def combustible(dias: int = 30, kpi: KPIService = Depends(get_kpi_service)):
    return kpi.consumo_combustible(dias)


@router.get("/costo-por-km")
def costo_por_km(dias: int = 30, kpi: KPIService = Depends(get_kpi_service)):
    return kpi.costo_por_kilometro(dias)


@router.get("/mantenimientos")
def mantenimientos(dias: int = 90, kpi: KPIService = Depends(get_kpi_service)):
    return kpi.mantenimientos_ratio(dias)


@router.get("/mtbf")
def mtbf(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.mtbf()


@router.get("/mttr")
def mttr(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.mttr()


@router.get("/vehiculos-taller")
def vehiculos_taller(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.vehiculos_en_taller()


@router.get("/alertas")
def alertas(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.alertas_vencimiento()


@router.get("/siniestralidad")
def siniestralidad(dias: int = 365, kpi: KPIService = Depends(get_kpi_service)):
    return kpi.indice_siniestralidad(dias)


@router.get("/conductores")
def conductores(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.rendimiento_conductores()


@router.get("/documentacion")
def documentacion(kpi: KPIService = Depends(get_kpi_service)):
    return kpi.estado_documentacion()


@router.get("/costos")
def costos(dias: int = 30, kpi: KPIService = Depends(get_kpi_service)):
    return kpi.costos_operacion(dias)
