"""
🧠 CEREBRO OMEGA ∞
SUPRACONSCIENCIA OMEGA — V1

Capa de metacognición:
OBSERVAR → EVALUAR → APRENDER → PROPONER

Este módulo NO modifica el núcleo.
"""

import json
import os
from datetime import datetime


ARCHIVO_EXPERIENCIAS = "experiencias_supraconsciencia.json"


class SupraconscienciaOmega:

    def __init__(self):
        self.estado = "ACTIVA"
        self.ciclos = 0
        self.experiencias = self._cargar_experiencias()

    # =========================================================
    # CARGAR MEMORIA
    # =========================================================

    def _cargar_experiencias(self):
        if not os.path.exists(ARCHIVO_EXPERIENCIAS):
            return []

        try:
            with open(
                ARCHIVO_EXPERIENCIAS,
                "r",
                encoding="utf-8"
            ) as archivo:
                return json.load(archivo)

        except Exception:
            return []

    # =========================================================
    # GUARDAR MEMORIA
    # =========================================================

    def _guardar_experiencias(self):
        with open(
            ARCHIVO_EXPERIENCIAS,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                self.experiencias,
                archivo,
                ensure_ascii=False,
                indent=4
            )

    # =========================================================
    # OBSERVAR
    # =========================================================

    def observar(self, entrada, respuesta=None):

        observacion = {
            "fecha": datetime.now().isoformat(),
            "entrada": str(entrada),
            "respuesta": str(respuesta) if respuesta else "",
        }

        return observacion

    # =========================================================
    # EVALUAR
    # =========================================================

    def evaluar(self, entrada, respuesta=None):

        evaluacion = {
            "claridad": 0.5,
            "coherencia": 0.5,
            "utilidad": 0.5,
            "confianza": 0.5,
        }

        if entrada:
            evaluacion["claridad"] = 0.8

        if respuesta:
            evaluacion["coherencia"] = 0.8
            evaluacion["utilidad"] = 0.8

        evaluacion["confianza"] = (
            evaluacion["claridad"]
            + evaluacion["coherencia"]
            + evaluacion["utilidad"]
        ) / 3

        return evaluacion

    # =========================================================
    # APRENDER
    # =========================================================

    def aprender(self, observacion, evaluacion):

        experiencia = {
            "id": len(self.experiencias) + 1,
            "fecha": datetime.now().isoformat(),
            "observacion": observacion,
            "evaluacion": evaluacion,
        }

        self.experiencias.append(experiencia)
        self._guardar_experiencias()

        return experiencia

    # =========================================================
    # CICLO COMPLETO
    # =========================================================

    def ciclo(self, entrada, respuesta=None):

        self.ciclos += 1

        observacion = self.observar(
            entrada,
            respuesta
        )

        evaluacion = self.evaluar(
            entrada,
            respuesta
        )

        experiencia = self.aprender(
            observacion,
            evaluacion
        )

        return {
            "estado": self.estado,
            "ciclo": self.ciclos,
            "observacion": observacion,
            "evaluacion": evaluacion,
            "experiencia_guardada": experiencia["id"]
        }

    # =========================================================
    # ESTADO
    # =========================================================

    def estado_actual(self):

        return {
            "estado": self.estado,
            "ciclos": self.ciclos,
            "experiencias": len(self.experiencias)
        }
