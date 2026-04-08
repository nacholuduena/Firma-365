from sqlalchemy import Column, Integer, String, Float, Date, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from .database import Base


class EstadoVehiculo(str, enum.Enum):
    DISPONIBLE = "disponible"
    EN_RUTA = "en_ruta"
    EN_TALLER = "en_taller"
    FUERA_DE_SERVICIO = "fuera_de_servicio"


class TipoVehiculo(str, enum.Enum):
    CAMION = "camion"
    CAMIONETA = "camioneta"
    SEDAN = "sedan"
    SUV = "suv"
    VAN = "van"
    MOTO = "moto"


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    placa = Column(String(20), unique=True, nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)
    tipo = Column(SAEnum(TipoVehiculo), nullable=False)
    estado = Column(SAEnum(EstadoVehiculo), default=EstadoVehiculo.DISPONIBLE)
    kilometraje_actual = Column(Float, default=0)
    capacidad_tanque = Column(Float, default=60)  # litros
    rendimiento_esperado = Column(Float, default=10)  # km/l
    fecha_adquisicion = Column(Date)
    activo = Column(Boolean, default=True)
    conductor_asignado_id = Column(Integer, nullable=True)

    mantenimientos = relationship("Mantenimiento", back_populates="vehiculo")
    registros_combustible = relationship("RegistroCombustible", back_populates="vehiculo")
    viajes = relationship("Viaje", back_populates="vehiculo")
    siniestros = relationship("Siniestro", back_populates="vehiculo")
    documentos = relationship("Documento", back_populates="vehiculo")
    costos = relationship("CostoOperacion", back_populates="vehiculo")
