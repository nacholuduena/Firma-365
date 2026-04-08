from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from .database import Base


class TipoDocumento(str, enum.Enum):
    SEGURO = "seguro"
    REVISION_TECNICA = "revision_tecnica"
    PERMISO_CIRCULACION = "permiso_circulacion"
    LICENCIA_CONDUCIR = "licencia_conducir"
    TARJETA_PROPIEDAD = "tarjeta_propiedad"


class EstadoDocumento(str, enum.Enum):
    VIGENTE = "vigente"
    POR_VENCER = "por_vencer"
    VENCIDO = "vencido"


class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    tipo = Column(SAEnum(TipoDocumento), nullable=False)
    numero = Column(String(50))
    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    estado = Column(SAEnum(EstadoDocumento), default=EstadoDocumento.VIGENTE)
    proveedor = Column(String(100))

    vehiculo = relationship("Vehiculo", back_populates="documentos")
