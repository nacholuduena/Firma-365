from sqlalchemy import Column, Integer, String, Date, Float, Boolean
from .database import Base


class Conductor(Base):
    __tablename__ = "conductores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    licencia = Column(String(30), nullable=False)
    categoria_licencia = Column(String(10), nullable=False)
    fecha_vencimiento_licencia = Column(Date, nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    fecha_ingreso = Column(Date)
    calificacion = Column(Float, default=5.0)  # 1-5
    total_viajes = Column(Integer, default=0)
    total_km = Column(Float, default=0)
    total_siniestros = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
