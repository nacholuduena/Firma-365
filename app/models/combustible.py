from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from .database import Base


class RegistroCombustible(Base):
    __tablename__ = "registros_combustible"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    litros = Column(Float, nullable=False)
    costo_total = Column(Float, nullable=False)
    costo_por_litro = Column(Float, nullable=False)
    kilometraje = Column(Float, nullable=False)
    tipo_combustible = Column(String(20), default="diesel")
    estacion = Column(String(100))

    vehiculo = relationship("Vehiculo", back_populates="registros_combustible")
