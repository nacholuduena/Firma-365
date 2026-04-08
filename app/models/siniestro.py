from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from .database import Base


class GravedadSiniestro(str, enum.Enum):
    LEVE = "leve"
    MODERADO = "moderado"
    GRAVE = "grave"


class Siniestro(Base):
    __tablename__ = "siniestros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    conductor_id = Column(Integer, ForeignKey("conductores.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    descripcion = Column(Text, nullable=False)
    gravedad = Column(SAEnum(GravedadSiniestro), nullable=False)
    costo_estimado = Column(Float, default=0)
    ubicacion = Column(String(200))
    tiene_seguro = Column(Integer, default=1)
    numero_poliza = Column(String(50))

    vehiculo = relationship("Vehiculo", back_populates="siniestros")
