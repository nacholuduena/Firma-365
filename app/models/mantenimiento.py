from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from .database import Base


class TipoMantenimiento(str, enum.Enum):
    PREVENTIVO = "preventivo"
    CORRECTIVO = "correctivo"


class EstadoMantenimiento(str, enum.Enum):
    PROGRAMADO = "programado"
    EN_PROCESO = "en_proceso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class Mantenimiento(Base):
    __tablename__ = "mantenimientos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    tipo = Column(SAEnum(TipoMantenimiento), nullable=False)
    estado = Column(SAEnum(EstadoMantenimiento), default=EstadoMantenimiento.PROGRAMADO)
    descripcion = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    costo = Column(Float, default=0)
    kilometraje_al_ingreso = Column(Float)
    proveedor = Column(String(100))
    notas = Column(Text)

    vehiculo = relationship("Vehiculo", back_populates="mantenimientos")
