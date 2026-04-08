from datetime import date, timedelta
from sqlalchemy import func, case, and_
from sqlalchemy.orm import Session

from app.models.vehiculo import Vehiculo, EstadoVehiculo
from app.models.conductor import Conductor
from app.models.mantenimiento import Mantenimiento, TipoMantenimiento, EstadoMantenimiento
from app.models.combustible import RegistroCombustible
from app.models.viaje import Viaje, EstadoViaje
from app.models.siniestro import Siniestro, GravedadSiniestro
from app.models.documento import Documento, EstadoDocumento, TipoDocumento
from app.models.costo import CostoOperacion, CategoriaCosto


class KPIService:
    def __init__(self, db: Session):
        self.db = db

    # ── Resumen General ──────────────────────────────────────────────

    def resumen_flota(self) -> dict:
        total = self.db.query(Vehiculo).filter(Vehiculo.activo == True).count()
        disponibles = self.db.query(Vehiculo).filter(
            Vehiculo.activo == True,
            Vehiculo.estado == EstadoVehiculo.DISPONIBLE,
        ).count()
        en_ruta = self.db.query(Vehiculo).filter(
            Vehiculo.estado == EstadoVehiculo.EN_RUTA
        ).count()
        en_taller = self.db.query(Vehiculo).filter(
            Vehiculo.estado == EstadoVehiculo.EN_TALLER
        ).count()
        fuera_servicio = self.db.query(Vehiculo).filter(
            Vehiculo.estado == EstadoVehiculo.FUERA_DE_SERVICIO
        ).count()

        return {
            "total_vehiculos": total,
            "disponibles": disponibles,
            "en_ruta": en_ruta,
            "en_taller": en_taller,
            "fuera_de_servicio": fuera_servicio,
            "conductores_activos": self.db.query(Conductor).filter(
                Conductor.activo == True
            ).count(),
        }

    # ── KPI 1: Disponibilidad de Flota ───────────────────────────────

    def disponibilidad_flota(self) -> dict:
        total = self.db.query(Vehiculo).filter(Vehiculo.activo == True).count()
        operativos = self.db.query(Vehiculo).filter(
            Vehiculo.activo == True,
            Vehiculo.estado.in_([EstadoVehiculo.DISPONIBLE, EstadoVehiculo.EN_RUTA]),
        ).count()
        porcentaje = (operativos / total * 100) if total > 0 else 0

        return {
            "total": total,
            "operativos": operativos,
            "no_operativos": total - operativos,
            "porcentaje": round(porcentaje, 1),
        }

    # ── KPI 2: Utilización de Vehículos ──────────────────────────────

    def utilizacion_vehiculos(self, dias: int = 30) -> dict:
        fecha_desde = date.today() - timedelta(days=dias)
        vehiculos = self.db.query(Vehiculo).filter(Vehiculo.activo == True).all()
        resultado = []

        for v in vehiculos:
            viajes = self.db.query(Viaje).filter(
                Viaje.vehiculo_id == v.id,
                Viaje.fecha_salida >= fecha_desde,
                Viaje.estado == EstadoViaje.COMPLETADO,
            ).count()
            dias_activo = viajes  # simplificación: 1 viaje = 1 día activo
            tasa = (dias_activo / dias * 100) if dias > 0 else 0
            resultado.append({
                "vehiculo_id": v.id,
                "placa": v.placa,
                "marca": f"{v.marca} {v.modelo}",
                "viajes": viajes,
                "tasa_utilizacion": round(tasa, 1),
            })

        resultado.sort(key=lambda x: x["tasa_utilizacion"], reverse=True)
        promedio = sum(r["tasa_utilizacion"] for r in resultado) / len(resultado) if resultado else 0

        return {
            "promedio_utilizacion": round(promedio, 1),
            "vehiculos": resultado,
        }

    # ── KPI 3: Kilometraje ───────────────────────────────────────────

    def kilometraje(self, dias: int = 30) -> dict:
        fecha_desde = date.today() - timedelta(days=dias)
        viajes = self.db.query(
            Viaje.vehiculo_id,
            func.sum(Viaje.km_recorridos).label("total_km"),
            func.count(Viaje.id).label("total_viajes"),
        ).filter(
            Viaje.fecha_salida >= fecha_desde,
            Viaje.estado == EstadoViaje.COMPLETADO,
        ).group_by(Viaje.vehiculo_id).all()

        total_km = sum(v.total_km or 0 for v in viajes)
        total_viajes = sum(v.total_viajes for v in viajes)

        por_vehiculo = []
        for v in viajes:
            vehiculo = self.db.query(Vehiculo).get(v.vehiculo_id)
            if vehiculo:
                por_vehiculo.append({
                    "placa": vehiculo.placa,
                    "km": round(v.total_km or 0, 1),
                    "viajes": v.total_viajes,
                })

        por_vehiculo.sort(key=lambda x: x["km"], reverse=True)

        return {
            "total_km": round(total_km, 1),
            "promedio_km": round(total_km / len(viajes), 1) if viajes else 0,
            "total_viajes": total_viajes,
            "por_vehiculo": por_vehiculo,
        }

    # ── KPI 4: Consumo de Combustible ────────────────────────────────

    def consumo_combustible(self, dias: int = 30) -> dict:
        fecha_desde = date.today() - timedelta(days=dias)
        registros = self.db.query(
            RegistroCombustible.vehiculo_id,
            func.sum(RegistroCombustible.litros).label("total_litros"),
            func.sum(RegistroCombustible.costo_total).label("total_costo"),
        ).filter(
            RegistroCombustible.fecha >= fecha_desde,
        ).group_by(RegistroCombustible.vehiculo_id).all()

        total_litros = sum(r.total_litros or 0 for r in registros)
        total_costo = sum(r.total_costo or 0 for r in registros)

        por_vehiculo = []
        for r in registros:
            vehiculo = self.db.query(Vehiculo).get(r.vehiculo_id)
            if vehiculo:
                por_vehiculo.append({
                    "placa": vehiculo.placa,
                    "litros": round(r.total_litros or 0, 1),
                    "costo": round(r.total_costo or 0, 2),
                })

        por_vehiculo.sort(key=lambda x: x["litros"], reverse=True)

        return {
            "total_litros": round(total_litros, 1),
            "total_costo": round(total_costo, 2),
            "costo_promedio_litro": round(total_costo / total_litros, 2) if total_litros > 0 else 0,
            "por_vehiculo": por_vehiculo,
        }

    # ── KPI 5: Costo por Kilómetro ──────────────────────────────────

    def costo_por_kilometro(self, dias: int = 30) -> dict:
        fecha_desde = date.today() - timedelta(days=dias)

        costos = self.db.query(func.sum(CostoOperacion.monto)).filter(
            CostoOperacion.fecha >= fecha_desde,
        ).scalar() or 0

        km = self.db.query(func.sum(Viaje.km_recorridos)).filter(
            Viaje.fecha_salida >= fecha_desde,
            Viaje.estado == EstadoViaje.COMPLETADO,
        ).scalar() or 0

        costo_km = (costos / km) if km > 0 else 0

        # Por categoría
        por_categoria = self.db.query(
            CostoOperacion.categoria,
            func.sum(CostoOperacion.monto).label("total"),
        ).filter(
            CostoOperacion.fecha >= fecha_desde,
        ).group_by(CostoOperacion.categoria).all()

        categorias = {str(c.categoria.value): round(c.total, 2) for c in por_categoria}

        return {
            "costo_por_km": round(costo_km, 2),
            "costo_total": round(costos, 2),
            "km_totales": round(km, 1),
            "por_categoria": categorias,
        }

    # ── KPI 6: Mantenimiento Preventivo vs Correctivo ────────────────

    def mantenimientos_ratio(self, dias: int = 90) -> dict:
        fecha_desde = date.today() - timedelta(days=dias)

        preventivos = self.db.query(Mantenimiento).filter(
            Mantenimiento.fecha_inicio >= fecha_desde,
            Mantenimiento.tipo == TipoMantenimiento.PREVENTIVO,
        ).count()

        correctivos = self.db.query(Mantenimiento).filter(
            Mantenimiento.fecha_inicio >= fecha_desde,
            Mantenimiento.tipo == TipoMantenimiento.CORRECTIVO,
        ).count()

        total = preventivos + correctivos
        costo_preventivo = self.db.query(func.sum(Mantenimiento.costo)).filter(
            Mantenimiento.fecha_inicio >= fecha_desde,
            Mantenimiento.tipo == TipoMantenimiento.PREVENTIVO,
        ).scalar() or 0

        costo_correctivo = self.db.query(func.sum(Mantenimiento.costo)).filter(
            Mantenimiento.fecha_inicio >= fecha_desde,
            Mantenimiento.tipo == TipoMantenimiento.CORRECTIVO,
        ).scalar() or 0

        return {
            "preventivos": preventivos,
            "correctivos": correctivos,
            "total": total,
            "ratio_preventivo": round(preventivos / total * 100, 1) if total > 0 else 0,
            "ratio_correctivo": round(correctivos / total * 100, 1) if total > 0 else 0,
            "costo_preventivo": round(costo_preventivo, 2),
            "costo_correctivo": round(costo_correctivo, 2),
        }

    # ── KPI 7: MTBF - Tiempo Medio entre Fallas ─────────────────────

    def mtbf(self) -> dict:
        vehiculos = self.db.query(Vehiculo).filter(Vehiculo.activo == True).all()
        resultados = []

        for v in vehiculos:
            fallas = self.db.query(Mantenimiento).filter(
                Mantenimiento.vehiculo_id == v.id,
                Mantenimiento.tipo == TipoMantenimiento.CORRECTIVO,
            ).order_by(Mantenimiento.fecha_inicio).all()

            if len(fallas) >= 2:
                intervalos = []
                for i in range(1, len(fallas)):
                    diff = (fallas[i].fecha_inicio - fallas[i - 1].fecha_inicio).days
                    intervalos.append(diff)
                mtbf_dias = sum(intervalos) / len(intervalos)
            elif len(fallas) == 1 and v.fecha_adquisicion:
                mtbf_dias = (date.today() - v.fecha_adquisicion).days
            else:
                mtbf_dias = None

            resultados.append({
                "placa": v.placa,
                "marca": f"{v.marca} {v.modelo}",
                "total_fallas": len(fallas),
                "mtbf_dias": round(mtbf_dias, 1) if mtbf_dias else None,
            })

        resultados_con_mtbf = [r for r in resultados if r["mtbf_dias"] is not None]
        promedio = (
            sum(r["mtbf_dias"] for r in resultados_con_mtbf) / len(resultados_con_mtbf)
            if resultados_con_mtbf else 0
        )

        return {
            "promedio_mtbf_dias": round(promedio, 1),
            "vehiculos": resultados,
        }

    # ── KPI 8: MTTR - Tiempo Medio de Reparación ────────────────────

    def mttr(self) -> dict:
        reparaciones = self.db.query(Mantenimiento).filter(
            Mantenimiento.tipo == TipoMantenimiento.CORRECTIVO,
            Mantenimiento.estado == EstadoMantenimiento.COMPLETADO,
            Mantenimiento.fecha_fin.isnot(None),
        ).all()

        tiempos = []
        for r in reparaciones:
            dias = (r.fecha_fin - r.fecha_inicio).days
            tiempos.append(dias)

        promedio = sum(tiempos) / len(tiempos) if tiempos else 0

        return {
            "promedio_mttr_dias": round(promedio, 1),
            "total_reparaciones": len(reparaciones),
            "min_dias": min(tiempos) if tiempos else 0,
            "max_dias": max(tiempos) if tiempos else 0,
        }

    # ── KPI 9: Vehículos en Taller ───────────────────────────────────

    def vehiculos_en_taller(self) -> dict:
        en_taller = self.db.query(Vehiculo).filter(
            Vehiculo.estado == EstadoVehiculo.EN_TALLER,
        ).all()

        detalle = []
        for v in en_taller:
            mant = self.db.query(Mantenimiento).filter(
                Mantenimiento.vehiculo_id == v.id,
                Mantenimiento.estado.in_([
                    EstadoMantenimiento.EN_PROCESO,
                    EstadoMantenimiento.PROGRAMADO,
                ]),
            ).first()

            dias_en_taller = 0
            tipo_mant = None
            if mant:
                dias_en_taller = (date.today() - mant.fecha_inicio).days
                tipo_mant = mant.tipo.value if mant.tipo else None

            detalle.append({
                "placa": v.placa,
                "marca": f"{v.marca} {v.modelo}",
                "dias_en_taller": dias_en_taller,
                "tipo_mantenimiento": tipo_mant,
                "descripcion": mant.descripcion if mant else "",
            })

        return {
            "total_en_taller": len(en_taller),
            "vehiculos": detalle,
        }

    # ── KPI 10: Alertas de Vencimiento ───────────────────────────────

    def alertas_vencimiento(self) -> dict:
        hoy = date.today()
        en_30_dias = hoy + timedelta(days=30)

        vencidos = self.db.query(Documento).filter(
            Documento.fecha_vencimiento < hoy,
        ).all()

        por_vencer = self.db.query(Documento).filter(
            Documento.fecha_vencimiento >= hoy,
            Documento.fecha_vencimiento <= en_30_dias,
        ).all()

        def doc_to_dict(doc):
            vehiculo = self.db.query(Vehiculo).get(doc.vehiculo_id)
            return {
                "vehiculo": vehiculo.placa if vehiculo else "N/A",
                "tipo": doc.tipo.value,
                "numero": doc.numero,
                "vencimiento": doc.fecha_vencimiento.isoformat(),
                "dias_restantes": (doc.fecha_vencimiento - hoy).days,
            }

        # Licencias de conductores
        licencias_por_vencer = self.db.query(Conductor).filter(
            Conductor.activo == True,
            Conductor.fecha_vencimiento_licencia >= hoy,
            Conductor.fecha_vencimiento_licencia <= en_30_dias,
        ).all()

        licencias_vencidas = self.db.query(Conductor).filter(
            Conductor.activo == True,
            Conductor.fecha_vencimiento_licencia < hoy,
        ).all()

        return {
            "documentos_vencidos": [doc_to_dict(d) for d in vencidos],
            "documentos_por_vencer": [doc_to_dict(d) for d in por_vencer],
            "total_vencidos": len(vencidos),
            "total_por_vencer": len(por_vencer),
            "licencias_por_vencer": len(licencias_por_vencer),
            "licencias_vencidas": len(licencias_vencidas),
        }

    # ── KPI 11: Índice de Siniestralidad ─────────────────────────────

    def indice_siniestralidad(self, dias: int = 365) -> dict:
        fecha_desde = date.today() - timedelta(days=dias)
        total_vehiculos = self.db.query(Vehiculo).filter(Vehiculo.activo == True).count()

        siniestros = self.db.query(Siniestro).filter(
            Siniestro.fecha >= fecha_desde,
        ).all()

        por_gravedad = {"leve": 0, "moderado": 0, "grave": 0}
        costo_total = 0
        for s in siniestros:
            por_gravedad[s.gravedad.value] += 1
            costo_total += s.costo_estimado or 0

        indice = (len(siniestros) / total_vehiculos * 100) if total_vehiculos > 0 else 0

        # Tendencia mensual
        meses = []
        for i in range(12):
            mes_inicio = date.today().replace(day=1) - timedelta(days=30 * i)
            mes_fin = (mes_inicio + timedelta(days=32)).replace(day=1)
            count = self.db.query(Siniestro).filter(
                Siniestro.fecha >= mes_inicio,
                Siniestro.fecha < mes_fin,
            ).count()
            meses.append({
                "mes": mes_inicio.strftime("%Y-%m"),
                "siniestros": count,
            })
        meses.reverse()

        return {
            "total_siniestros": len(siniestros),
            "indice": round(indice, 1),
            "por_gravedad": por_gravedad,
            "costo_total": round(costo_total, 2),
            "tendencia_mensual": meses,
        }

    # ── KPI 12: Rendimiento por Conductor ────────────────────────────

    def rendimiento_conductores(self) -> dict:
        conductores = self.db.query(Conductor).filter(Conductor.activo == True).all()
        resultado = []

        for c in conductores:
            viajes = self.db.query(Viaje).filter(
                Viaje.conductor_id == c.id,
                Viaje.estado == EstadoViaje.COMPLETADO,
            ).count()
            km = self.db.query(func.sum(Viaje.km_recorridos)).filter(
                Viaje.conductor_id == c.id,
                Viaje.estado == EstadoViaje.COMPLETADO,
            ).scalar() or 0
            siniestros = self.db.query(Siniestro).filter(
                Siniestro.conductor_id == c.id,
            ).count()

            resultado.append({
                "id": c.id,
                "nombre": c.nombre,
                "calificacion": c.calificacion,
                "viajes": viajes,
                "km": round(km, 1),
                "siniestros": siniestros,
                "licencia_vence": c.fecha_vencimiento_licencia.isoformat(),
            })

        resultado.sort(key=lambda x: x["calificacion"], reverse=True)

        return {"conductores": resultado}

    # ── KPI 13: Estado de Documentación ──────────────────────────────

    def estado_documentacion(self) -> dict:
        hoy = date.today()
        total = self.db.query(Documento).count()
        vigentes = self.db.query(Documento).filter(
            Documento.fecha_vencimiento > hoy + timedelta(days=30),
        ).count()
        por_vencer = self.db.query(Documento).filter(
            Documento.fecha_vencimiento >= hoy,
            Documento.fecha_vencimiento <= hoy + timedelta(days=30),
        ).count()
        vencidos = self.db.query(Documento).filter(
            Documento.fecha_vencimiento < hoy,
        ).count()

        por_tipo = self.db.query(
            Documento.tipo,
            func.count(Documento.id).label("total"),
            func.sum(case(
                (Documento.fecha_vencimiento < hoy, 1), else_=0
            )).label("vencidos"),
        ).group_by(Documento.tipo).all()

        tipos = []
        for t in por_tipo:
            tipos.append({
                "tipo": t.tipo.value,
                "total": t.total,
                "vencidos": int(t.vencidos or 0),
            })

        return {
            "total": total,
            "vigentes": vigentes,
            "por_vencer": por_vencer,
            "vencidos": vencidos,
            "porcentaje_cumplimiento": round(vigentes / total * 100, 1) if total > 0 else 0,
            "por_tipo": tipos,
        }

    # ── KPI 14: Costos Totales de Operación ──────────────────────────

    def costos_operacion(self, dias: int = 30) -> dict:
        fecha_desde = date.today() - timedelta(days=dias)

        por_categoria = self.db.query(
            CostoOperacion.categoria,
            func.sum(CostoOperacion.monto).label("total"),
            func.count(CostoOperacion.id).label("registros"),
        ).filter(
            CostoOperacion.fecha >= fecha_desde,
        ).group_by(CostoOperacion.categoria).all()

        categorias = []
        total_general = 0
        for c in por_categoria:
            monto = round(c.total or 0, 2)
            total_general += monto
            categorias.append({
                "categoria": c.categoria.value,
                "total": monto,
                "registros": c.registros,
            })

        categorias.sort(key=lambda x: x["total"], reverse=True)

        # Tendencia diaria
        tendencia = self.db.query(
            CostoOperacion.fecha,
            func.sum(CostoOperacion.monto).label("total"),
        ).filter(
            CostoOperacion.fecha >= fecha_desde,
        ).group_by(CostoOperacion.fecha).order_by(CostoOperacion.fecha).all()

        tendencia_data = [
            {"fecha": t.fecha.isoformat(), "monto": round(t.total, 2)}
            for t in tendencia
        ]

        return {
            "total_general": round(total_general, 2),
            "por_categoria": categorias,
            "tendencia_diaria": tendencia_data,
        }

    # ── Todos los KPIs ───────────────────────────────────────────────

    def dashboard_completo(self) -> dict:
        return {
            "resumen": self.resumen_flota(),
            "disponibilidad": self.disponibilidad_flota(),
            "utilizacion": self.utilizacion_vehiculos(),
            "kilometraje": self.kilometraje(),
            "combustible": self.consumo_combustible(),
            "costo_por_km": self.costo_por_kilometro(),
            "mantenimientos": self.mantenimientos_ratio(),
            "mtbf": self.mtbf(),
            "mttr": self.mttr(),
            "vehiculos_taller": self.vehiculos_en_taller(),
            "alertas": self.alertas_vencimiento(),
            "siniestralidad": self.indice_siniestralidad(),
            "conductores": self.rendimiento_conductores(),
            "documentacion": self.estado_documentacion(),
            "costos": self.costos_operacion(),
        }
