from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from .database import Base


class CategoriaCosto(str, enum.Enum):
    COMBUSTIBLE = "combustible"
    MANTENIMIENTO = "mantenimiento"
    SEGURO = "seguro"
    IMPUESTOS = "impuestos"
    PEAJES = "peajes"
    MULTAS = "multas"
    REPUESTOS = "repuestos"
    OTROS = "otros"


class CostoOperacion(Base):
    __tablename__ = "costos_operacion"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    categoria = Column(SAEnum(CategoriaCosto), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(String(200))
    referencia = Column(String(50))

    vehiculo = relationship("Vehiculo", back_populates="costos")
