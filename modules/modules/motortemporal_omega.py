# modules/motor_temporal_omega.py
"""
╔══════════════════════════════════════════════════════════════╗
║                 CEREBRO OMEGA ∞                            ║
║              MOTOR TEMPORAL OMEGA                          ║
╠══════════════════════════════════════════════════════════════╣
║ PASADO → PRESENTE → FUTUROS POTENCIALES                    ║
║                                                              ║
║ Capacidades:                                                 ║
║ • Investigación temporal                                    ║
║ • Línea cronológica                                         ║
║ • Análisis causal                                           ║
║ • Contrafactuales                                           ║
║ • Escenarios futuros                                        ║
║ • Señales de cambio                                         ║
║ • Evaluación de hipótesis                                   ║
║ • Memoria de ciclos                                         ║
║ • Comparación futura vs. realidad                           ║
║                                                              ║
║ El módulo NO modifica el CORE.                              ║
╚══════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import json
import os
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Any


class MotorTemporalOmega:

    NAME = "MOTOR TEMPORAL OMEGA"
    VERSION = "3.0"

    ESTADOS = (
        "HECHO",
        "INFERENCIA",
        "HIPOTESIS",
        "CONTRAFÁCTICO",
        "ESCENARIO",
        "INCERTIDUMBRE",
    )

    def __init__(
        self,
        memoria_path: str = "memoria_temporal.json",
    ):
        self.memoria_path = Path(memoria_path)
        self.memoria = self._cargar_memoria()

    # =========================================================
    # MEMORIA
    # =========================================================

    def _cargar_memoria(self) -> dict:
        if not self.memoria_path.exists():
            return {
                "version": self.VERSION,
                "ciclos": [],
                "hipotesis": [],
                "escenarios": [],
                "aprendizajes": [],
            }

        try:
            with self.memoria_path.open(
                "r",
                encoding="utf-8"
            ) as archivo:
                return json.load(archivo)

        except Exception:
            return {
                "version": self.VERSION,
                "ciclos": [],
                "hipotesis": [],
                "escenarios": [],
                "aprendizajes": [],
            }

    def _guardar_memoria(self):
        temporal = self.memoria_path.with_suffix(".tmp")

        with temporal.open(
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                self.memoria,
                archivo,
                ensure_ascii=False,
                indent=2,
            )

        temporal.replace(self.memoria_path)

    # =========================================================
    # IDENTIDAD DE INVESTIGACIÓN
    # =========================================================

    def _id_investigacion(self, pregunta: str) -> str:
        base = (
            pregunta.strip()
            + "|"
            + datetime.now(timezone.utc).isoformat()
        )

        return hashlib.sha256(
            base.encode("utf-8")
        ).hexdigest()[:16]

    # =========================================================
    # ESTRUCTURA DE INVESTIGACIÓN
    # =========================================================

    def crear_investigacion(
        self,
        pregunta: str,
        inicio: str | None = None,
        fin: str | None = None,
        horizonte: str | None = None,
        escenarios: int = 5,
    ) -> dict[str, Any]:

        if not pregunta.strip():
            raise ValueError(
                "La pregunta de investigación está vacía."
            )

        escenarios = max(
            3,
            min(int(escenarios), 10)
        )

        investigacion = {
            "id": self._id_investigacion(pregunta),
            "fecha": datetime.now(
                timezone.utc
            ).isoformat(),

            "pregunta": pregunta.strip(),

            "periodo": {
                "inicio": inicio,
                "fin": fin,
            },

            "horizonte_futuro": horizonte,

            "parametros": {
                "escenarios": escenarios,
            },

            "pasado": {
                "hechos": [],
                "cronologia": [],
                "causas": [],
                "consecuencias": [],
                "fuentes": [],
            },

            "presente": {
                "estado": [],
                "tendencias": [],
                "señales": [],
                "factores": [],
                "fuentes": [],
            },

            "futuro": {
                "escenarios": [],
                "variables_clave": [],
                "señales_tempranas": [],
            },

            "contrafactuales": [],

            "incertidumbres": [],

            "conclusion": "",

            "estado": "PENDIENTE",
        }

        return investigacion

    # =========================================================
    # REGISTRAR HECHOS
    # =========================================================

    def agregar_hecho(
        self,
        investigacion: dict,
        fecha: str,
        descripcion: str,
        fuente: str | None = None,
        confianza: float = 0.5,
    ):

        confianza = max(
            0.0,
            min(float(confianza), 1.0)
        )

        hecho = {
            "fecha": fecha,
            "descripcion": descripcion,
            "tipo": "HECHO",
            "confianza": confianza,
            "fuente": fuente,
        }

        investigacion["pasado"]["hechos"].append(
            hecho
        )

        investigacion["pasado"]["cronologia"].append(
            {
                "fecha": fecha,
                "evento": descripcion,
            }
        )

    # =========================================================
    # CAUSALIDAD
    # =========================================================

    def agregar_relacion_causal(
        self,
        investigacion: dict,
        causa: str,
        efecto: str,
        mecanismo: str,
        confianza: float = 0.5,
    ):

        investigacion["pasado"]["causas"].append(
            {
                "causa": causa,
                "efecto": efecto,
                "mecanismo": mecanismo,
                "confianza": max(
                    0.0,
                    min(float(confianza), 1.0)
                ),
                "tipo": "INFERENCIA",
            }
        )

    # =========================================================
    # CONTRAFACTUAL
    # =========================================================

    def agregar_contrafactual(
        self,
        investigacion: dict,
        condicion: str,
        escenario: str,
        consecuencias: list[str],
        supuestos: list[str] | None = None,
    ):

        investigacion["contrafactuales"].append(
            {
                "tipo": "CONTRAFÁCTICO",
                "condicion": condicion,
                "escenario": escenario,
                "consecuencias": consecuencias,
                "supuestos": supuestos or [],
            }
        )

    # =========================================================
    # ESCENARIOS FUTUROS
    # =========================================================

    def agregar_escenario(
        self,
        investigacion: dict,
        nombre: str,
        descripcion: str,
        factores: list[str],
        señales: list[str],
        obstaculos: list[str],
        plausibilidad: float,
    ):

        plausibilidad = max(
            0.0,
            min(float(plausibilidad), 1.0)
        )

        escenario = {
            "tipo": "ESCENARIO",
            "nombre": nombre,
            "descripcion": descripcion,
            "factores": factores,
            "señales_tempranas": señales,
            "obstaculos": obstaculos,
            "plausibilidad": plausibilidad,
        }

        investigacion["futuro"]["escenarios"].append(
            escenario
        )

    # =========================================================
    # VARIABLES CLAVE
    # =========================================================

    def agregar_variable(
        self,
        investigacion: dict,
        nombre: str,
        valor_actual: str,
        impacto: str,
        tendencia: str,
    ):

        investigacion["futuro"]["variables_clave"].append(
            {
                "nombre": nombre,
                "valor_actual": valor_actual,
                "impacto": impacto,
                "tendencia": tendencia,
            }
        )

    # =========================================================
    # INCERTIDUMBRE
    # =========================================================

    def agregar_incertidumbre(
        self,
        investigacion: dict,
        descripcion: str,
        impacto: str,
    ):

        investigacion["incertidumbres"].append(
            {
                "tipo": "INCERTIDUMBRE",
                "descripcion": descripcion,
                "impacto": impacto,
            }
        )

    # =========================================================
    # EVALUACIÓN
    # =========================================================

    def evaluar(
        self,
        investigacion: dict,
    ) -> dict:

        hechos = len(
            investigacion["pasado"]["hechos"]
        )

        causas = len(
            investigacion["pasado"]["causas"]
        )

        escenarios = len(
            investigacion["futuro"]["escenarios"]
        )

        contrafactuales = len(
            investigacion["contrafactuales"]
        )

        incertidumbres = len(
            investigacion["incertidumbres"]
        )

        componentes = (
            hechos
            + causas
            + escenarios
            + contrafactuales
        )

        puntuacion = min(
            100,
            componentes * 10
        )

        if incertidumbres:
            puntuacion -= min(
                20,
                incertidumbres * 2
            )

        puntuacion = max(
            0,
            puntuacion
        )

        if puntuacion >= 80:
            estado = "INVESTIGACIÓN FUERTE"
        elif puntuacion >= 50:
            estado = "INVESTIGACIÓN PARCIAL"
        else:
            estado = "INVESTIGACIÓN INCOMPLETA"

        resultado = {
            "puntuacion": puntuacion,
            "estado": estado,
            "hechos": hechos,
            "relaciones_causales": causas,
            "escenarios": escenarios,
            "contrafactuales": contrafactuales,
            "incertidumbres": incertidumbres,
        }

        investigacion["evaluacion"] = resultado

        return resultado

    # =========================================================
    # CERRAR CICLO
    # =========================================================

    def cerrar_ciclo(
        self,
        investigacion: dict,
        aprendizaje: str,
    ):

        evaluacion = self.evaluar(
            investigacion
        )

        investigacion["estado"] = "COMPLETADO"

        investigacion[
            "aprendizaje"
        ] = aprendizaje

        self.memoria["ciclos"].append(
            investigacion
        )

        self.memoria["aprendizajes"].append(
            {
                "fecha": datetime.now(
                    timezone.utc
                ).isoformat(),

                "investigacion_id":
                    investigacion["id"],

                "aprendizaje":
                    aprendizaje,

                "puntuacion":
                    evaluacion["puntuacion"],
            }
        )

        self._guardar_memoria()

        return investigacion

    # =========================================================
    # COMPARAR FUTURO CON REALIDAD
    # =========================================================

    def evaluar_escenario_historico(
        self,
        investigacion_id: str,
        realidad: str,
    ):

        for ciclo in self.memoria["ciclos"]:

            if ciclo["id"] != investigacion_id:
                continue

            registro = {
                "fecha_evaluacion":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                "investigacion_id":
                    investigacion_id,

                "realidad_observada":
                    realidad,

                "tipo":
                    "EVALUACION_POSTERIOR",
            }

            ciclo.setdefault(
                "evaluaciones_posteriores",
                []
            ).append(registro)

            self._guardar_memoria()

            return registro

        return None

    # =========================================================
    # RESUMEN PARA EL CORE
    # =========================================================

    def resumen_para_core(
        self,
        investigacion: dict,
    ) -> dict:

        return {
            "modulo": self.NAME,
            "version": self.VERSION,
            "investigacion_id":
                investigacion["id"],

            "pregunta":
                investigacion["pregunta"],

            "pasado":
                investigacion["pasado"],

            "presente":
                investigacion["presente"],

            "futuro":
                investigacion["futuro"],

            "contrafactuales":
                investigacion["contrafactuales"],

            "incertidumbres":
                investigacion["incertidumbres"],

            "evaluacion":
                investigacion.get(
                    "evaluacion",
                    {}
                ),
        }


# ============================================================
# PRUEBA DEL MOTOR
# ============================================================

if __name__ == "__main__":

    motor = MotorTemporalOmega()

    investigacion = motor.crear_investigacion(
        pregunta=(
            "Analizar la evolución de la inteligencia "
            "artificial y estudiar posibles escenarios "
            "de desarrollo durante los próximos años."
        ),

        inicio="1950",
        fin="2026",
        horizonte="2027-2040",

        escenarios=5,
    )

    motor.agregar_hecho(
        investigacion,
        "1950",
        "Inicio del periodo moderno de investigación "
        "sobre inteligencia artificial.",
        confianza=0.9,
    )

    motor.agregar_relacion_causal(
        investigacion,
        causa="Aumento de capacidad computacional",
        efecto="Mayor capacidad para entrenar modelos",
        mecanismo=(
            "Más recursos computacionales permiten "
            "procesar modelos y conjuntos de datos mayores."
        ),
        confianza=0.85,
    )

    motor.agregar_variable(
        investigacion,
        nombre="Capacidad computacional",
        valor_actual="Alta y creciente",
        impacto="Muy alto",
        tendencia="Creciente",
    )

    motor.agregar_escenario(
        investigacion,

        nombre="Aceleración",

        descripcion=(
            "La capacidad de los sistemas continúa "
            "aumentando rápidamente."
        ),

        factores=[
            "Más computación",
            "Mejores algoritmos",
            "Mayor disponibilidad de datos",
        ],

        señales=[
            "Nuevos saltos de rendimiento",
            "Reducción del coste de inferencia",
        ],

        obstaculos=[
            "Costes",
            "Regulación",
            "Limitaciones técnicas",
        ],

        plausibilidad=0.65,
    )

    motor.agregar_contrafactual(
        investigacion,

        condicion=(
            "¿Qué habría ocurrido si el aumento "
            "de capacidad computacional hubiera "
            "sido mucho más lento?"
        ),

        escenario=(
            "La evolución de los sistemas probablemente "
            "habría ocurrido a un ritmo diferente."
        ),

        consecuencias=[
            "Menor escala de modelos",
            "Menor velocidad de experimentación",
        ],

        supuestos=[
            "Las demás variables permanecen "
            "aproximadamente constantes."
        ],
    )

    motor.agregar_incertidumbre(
        investigacion,

        descripcion=(
            "No es posible conocer con certeza "
            "qué tecnologías futuras aparecerán."
        ),

        impacto="Alto",
    )

    resultado = motor.cerrar_ciclo(
        investigacion,

        aprendizaje=(
            "Las proyecciones futuras deben "
            "tratarse como escenarios condicionados "
            "por variables observables y no como "
            "certezas."
        ),
    )

    print(
        json.dumps(
            resultado,
            ensure_ascii=False,
            indent=2,
        )
    )
