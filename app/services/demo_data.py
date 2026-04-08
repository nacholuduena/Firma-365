import random
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.vehiculo import Vehiculo, EstadoVehiculo, TipoVehiculo
from app.models.conductor import Conductor
from app.models.mantenimiento import Mantenimiento, TipoMantenimiento, EstadoMantenimiento
from app.models.combustible import RegistroCombustible
from app.models.viaje import Viaje, EstadoViaje
from app.models.siniestro import Siniestro, GravedadSiniestro
from app.models.documento import Documento, TipoDocumento, EstadoDocumento
from app.models.costo import CostoOperacion, CategoriaCosto


def seed_demo_data(db: Session):
    """Genera datos de demostración realistas para el dashboard."""

    if db.query(Vehiculo).count() > 0:
        return  # Ya hay datos

    hoy = date.today()
    random.seed(42)

    # ── Vehículos ────────────────────────────────────────────────────
    vehiculos_data = [
        ("ABC-123", "Toyota", "Hilux", 2022, TipoVehiculo.CAMIONETA, EstadoVehiculo.EN_RUTA, 45200),
        ("DEF-456", "Ford", "Ranger", 2021, TipoVehiculo.CAMIONETA, EstadoVehiculo.DISPONIBLE, 62800),
        ("GHI-789", "Mercedes-Benz", "Actros", 2020, TipoVehiculo.CAMION, EstadoVehiculo.EN_RUTA, 128500),
        ("JKL-012", "Volkswagen", "Amarok", 2023, TipoVehiculo.CAMIONETA, EstadoVehiculo.DISPONIBLE, 18300),
        ("MNO-345", "Scania", "R450", 2019, TipoVehiculo.CAMION, EstadoVehiculo.EN_TALLER, 195000),
        ("PQR-678", "Toyota", "Corolla", 2022, TipoVehiculo.SEDAN, EstadoVehiculo.DISPONIBLE, 32100),
        ("STU-901", "Hyundai", "H1", 2021, TipoVehiculo.VAN, EstadoVehiculo.EN_RUTA, 55400),
        ("VWX-234", "Iveco", "Daily", 2020, TipoVehiculo.VAN, EstadoVehiculo.DISPONIBLE, 87600),
        ("YZA-567", "Mercedes-Benz", "Sprinter", 2023, TipoVehiculo.VAN, EstadoVehiculo.EN_RUTA, 22000),
        ("BCD-890", "Volvo", "FH", 2018, TipoVehiculo.CAMION, EstadoVehiculo.FUERA_DE_SERVICIO, 320000),
        ("EFG-111", "Chevrolet", "S10", 2022, TipoVehiculo.CAMIONETA, EstadoVehiculo.DISPONIBLE, 41000),
        ("HIJ-222", "Ford", "Transit", 2021, TipoVehiculo.VAN, EstadoVehiculo.EN_RUTA, 68200),
        ("KLM-333", "Toyota", "Hiace", 2023, TipoVehiculo.VAN, EstadoVehiculo.DISPONIBLE, 15600),
        ("NOP-444", "Scania", "G410", 2020, TipoVehiculo.CAMION, EstadoVehiculo.EN_TALLER, 175800),
        ("QRS-555", "Nissan", "Frontier", 2022, TipoVehiculo.CAMIONETA, EstadoVehiculo.EN_RUTA, 38900),
    ]

    vehiculos = []
    for placa, marca, modelo, anio, tipo, estado, km in vehiculos_data:
        v = Vehiculo(
            placa=placa, marca=marca, modelo=modelo, anio=anio,
            tipo=tipo, estado=estado, kilometraje_actual=km,
            capacidad_tanque=random.choice([60, 80, 100, 200]),
            rendimiento_esperado=random.choice([6, 8, 10, 12, 14]),
            fecha_adquisicion=hoy - timedelta(days=random.randint(365, 2000)),
            activo=True,
        )
        db.add(v)
        vehiculos.append(v)

    db.flush()

    # ── Conductores ──────────────────────────────────────────────────
    conductores_data = [
        ("Carlos Rodríguez", "12345678", "LIC-001", "B"),
        ("María López", "23456789", "LIC-002", "C"),
        ("Juan Martínez", "34567890", "LIC-003", "B"),
        ("Ana García", "45678901", "LIC-004", "C"),
        ("Pedro Sánchez", "56789012", "LIC-005", "B"),
        ("Laura Fernández", "67890123", "LIC-006", "B"),
        ("Diego Morales", "78901234", "LIC-007", "C"),
        ("Sofía Herrera", "89012345", "LIC-008", "B"),
        ("Roberto Díaz", "90123456", "LIC-009", "C"),
        ("Valentina Castro", "01234567", "LIC-010", "B"),
    ]

    conductores = []
    for nombre, cedula, lic, cat in conductores_data:
        vence = hoy + timedelta(days=random.randint(-30, 400))
        c = Conductor(
            nombre=nombre, cedula=cedula, licencia=lic,
            categoria_licencia=cat,
            fecha_vencimiento_licencia=vence,
            telefono=f"+54 9 11 {random.randint(1000,9999)}-{random.randint(1000,9999)}",
            email=f"{nombre.split()[0].lower()}@protracking.com",
            fecha_ingreso=hoy - timedelta(days=random.randint(180, 1500)),
            calificacion=round(random.uniform(3.5, 5.0), 1),
            total_viajes=random.randint(20, 200),
            total_km=random.randint(5000, 80000),
            total_siniestros=random.randint(0, 3),
            activo=True,
        )
        db.add(c)
        conductores.append(c)

    db.flush()

    # ── Viajes (últimos 90 días) ─────────────────────────────────────
    for _ in range(250):
        v = random.choice(vehiculos)
        c = random.choice(conductores)
        salida = hoy - timedelta(days=random.randint(0, 90))
        km = random.uniform(50, 1200)
        estado = random.choices(
            [EstadoViaje.COMPLETADO, EstadoViaje.EN_CURSO, EstadoViaje.CANCELADO],
            weights=[80, 10, 10],
        )[0]
        viaje = Viaje(
            vehiculo_id=v.id, conductor_id=c.id,
            fecha_salida=salida,
            fecha_llegada=salida + timedelta(days=random.randint(0, 3)) if estado == EstadoViaje.COMPLETADO else None,
            origen=random.choice(["Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Tucumán", "Mar del Plata"]),
            destino=random.choice(["Santa Fe", "Salta", "Neuquén", "Bahía Blanca", "La Plata", "Paraná"]),
            km_recorridos=round(km, 1) if estado == EstadoViaje.COMPLETADO else 0,
            estado=estado,
        )
        db.add(viaje)

    # ── Registros de Combustible ─────────────────────────────────────
    for _ in range(200):
        v = random.choice(vehiculos)
        litros = random.uniform(30, 200)
        costo_litro = random.uniform(0.9, 1.5)
        reg = RegistroCombustible(
            vehiculo_id=v.id,
            fecha=hoy - timedelta(days=random.randint(0, 90)),
            litros=round(litros, 1),
            costo_total=round(litros * costo_litro, 2),
            costo_por_litro=round(costo_litro, 2),
            kilometraje=v.kilometraje_actual - random.randint(0, 5000),
            tipo_combustible=random.choice(["diesel", "nafta"]),
            estacion=random.choice(["YPF Centro", "Shell Norte", "Axion Sur", "YPF Ruta 9"]),
        )
        db.add(reg)

    # ── Mantenimientos ───────────────────────────────────────────────
    for _ in range(60):
        v = random.choice(vehiculos)
        tipo = random.choices(
            [TipoMantenimiento.PREVENTIVO, TipoMantenimiento.CORRECTIVO],
            weights=[60, 40],
        )[0]
        inicio = hoy - timedelta(days=random.randint(0, 180))
        duracion = random.randint(1, 10)
        estado = random.choices(
            [EstadoMantenimiento.COMPLETADO, EstadoMantenimiento.EN_PROCESO, EstadoMantenimiento.PROGRAMADO],
            weights=[70, 15, 15],
        )[0]

        descripciones_prev = ["Cambio de aceite", "Rotación de neumáticos", "Revisión de frenos",
                              "Alineación y balanceo", "Cambio de filtros", "Revisión general"]
        descripciones_corr = ["Falla en motor", "Rotura de suspensión", "Problema eléctrico",
                              "Fuga de aceite", "Embrague dañado", "Problema de transmisión"]

        mant = Mantenimiento(
            vehiculo_id=v.id,
            tipo=tipo,
            estado=estado,
            descripcion=random.choice(descripciones_prev if tipo == TipoMantenimiento.PREVENTIVO else descripciones_corr),
            fecha_inicio=inicio,
            fecha_fin=inicio + timedelta(days=duracion) if estado == EstadoMantenimiento.COMPLETADO else None,
            costo=round(random.uniform(100, 5000), 2),
            kilometraje_al_ingreso=v.kilometraje_actual - random.randint(0, 3000),
            proveedor=random.choice(["Taller Central", "ServiFast", "MecánicaPro", "AutoService"]),
        )
        db.add(mant)

    # ── Siniestros ───────────────────────────────────────────────────
    for _ in range(12):
        v = random.choice(vehiculos)
        c = random.choice(conductores)
        gravedad = random.choices(
            [GravedadSiniestro.LEVE, GravedadSiniestro.MODERADO, GravedadSiniestro.GRAVE],
            weights=[50, 35, 15],
        )[0]
        sin = Siniestro(
            vehiculo_id=v.id, conductor_id=c.id,
            fecha=hoy - timedelta(days=random.randint(0, 365)),
            descripcion=random.choice([
                "Colisión menor en estacionamiento", "Choque por alcance",
                "Impacto lateral", "Vuelco en ruta", "Daño por granizo",
                "Colisión en intersección",
            ]),
            gravedad=gravedad,
            costo_estimado=round(random.uniform(500, 25000), 2),
            ubicacion=random.choice(["Ruta 9 km 45", "Av. Libertador 1200", "Autopista Sur", "Ruta 5 km 120"]),
            tiene_seguro=1,
        )
        db.add(sin)

    # ── Documentos ───────────────────────────────────────────────────
    for v in vehiculos:
        for tipo in TipoDocumento:
            if tipo == TipoDocumento.LICENCIA_CONDUCIR:
                continue
            emision = hoy - timedelta(days=random.randint(30, 400))
            vencimiento = emision + timedelta(days=random.randint(180, 400))
            doc = Documento(
                vehiculo_id=v.id,
                tipo=tipo,
                numero=f"{tipo.value[:3].upper()}-{random.randint(10000, 99999)}",
                fecha_emision=emision,
                fecha_vencimiento=vencimiento,
                proveedor=random.choice(["Seguros SA", "AseguraTodo", "ProtectPlus", "MunicipalidadX"]),
            )
            db.add(doc)

    # ── Costos de Operación ──────────────────────────────────────────
    for _ in range(300):
        v = random.choice(vehiculos)
        cat = random.choice(list(CategoriaCosto))
        montos = {
            CategoriaCosto.COMBUSTIBLE: (100, 800),
            CategoriaCosto.MANTENIMIENTO: (200, 5000),
            CategoriaCosto.SEGURO: (500, 2000),
            CategoriaCosto.IMPUESTOS: (100, 500),
            CategoriaCosto.PEAJES: (10, 100),
            CategoriaCosto.MULTAS: (50, 1000),
            CategoriaCosto.REPUESTOS: (50, 3000),
            CategoriaCosto.OTROS: (20, 500),
        }
        rango = montos[cat]
        costo = CostoOperacion(
            vehiculo_id=v.id,
            categoria=cat,
            monto=round(random.uniform(*rango), 2),
            fecha=hoy - timedelta(days=random.randint(0, 90)),
            descripcion=f"{cat.value.capitalize()} - {v.placa}",
        )
        db.add(costo)

    db.commit()
    print(f"[DEMO] Datos de demostración generados: {len(vehiculos)} vehículos, "
          f"{len(conductores)} conductores, 250 viajes, 200 cargas de combustible, "
          f"60 mantenimientos, 12 siniestros, {len(vehiculos)*4} documentos, 300 costos")
