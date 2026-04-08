from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from .database import Base


class EstadoViaje(str, enum.Enum):
    PROGRAMADO = "programado"
    EN_CURSO = "en_curso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class Viaje(Base):
    __tablename__ = "viajes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    conductor_id = Column(Integer, ForeignKey("conductores.id"), nullable=False)
    fecha_salida = Column(Date, nullable=False)
    fecha_llegada = Column(Date)
    origen = Column(String(200), nullable=False)
    destino = Column(String(200), nullable=False)
    km_recorridos = Column(Float, default=0)
    estado = Column(SAEnum(EstadoViaje), default=EstadoViaje.PROGRAMADO)
    carga_descripcion = Column(Text)
    notas = Column(Text)

    vehiculo = relationship("Vehiculo", back_populates="viajes")
