"""
CEREBRO OMEGA ∞
MÓDULO: ALIMENTADOR

Obtiene información externa y la prepara
para que CEREBRO OMEGA decida incorporarla
a su memoria.

Este módulo NO modifica el núcleo.
"""

import re
from datetime import datetime
from urllib.parse import quote

import requests


class AlimentadorOmega:

    VERSION = "1.0.0"
    NOMBRE = "ALIMENTADOR OMEGA"
    FUENTE = "Wikipedia"

    def __init__(self):
        self.experiencias = []

    # ========================================================
    # LIMPIAR TEXTO
    # ========================================================

    def limpiar(self, texto):

        if not texto:
            return ""

        texto = re.sub(
            r"\s+",
            " ",
            str(texto)
        )

        return texto.strip()

    # ========================================================
    # BUSCAR EN WIKIPEDIA
    # ========================================================

    def buscar(
        self,
        concepto,
        idioma="es"
    ):

        concepto = self.limpiar(
            concepto
        )

        if not concepto:

            return {
                "ok": False,
                "error":
                    "No se recibió ningún concepto."
            }

        url = (
            f"https://{idioma}.wikipedia.org"
            f"/api/rest_v1/page/summary/"
            f"{quote(concepto)}"
        )

        try:

            respuesta = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent":
                        "CEREBRO-OMEGA/1.0"
                }
            )

            if respuesta.status_code != 200:

                return {
                    "ok": False,
                    "error":
                        f"No se encontró información "
                        f"sobre: {concepto}"
                }

            datos = respuesta.json()

            titulo = datos.get(
                "title",
                concepto
            )

            descripcion = datos.get(
                "description",
                ""
            )

            extracto = datos.get(
                "extract",
                ""
            )

            if not extracto:

                return {
                    "ok": False,
                    "error":
                        "La fuente no devolvió "
                        "información suficiente."
                }

            conocimiento = {

                "concepto":
                    self.limpiar(titulo),

                "descripcion":
                    self.limpiar(descripcion),

                "informacion":
                    self.limpiar(extracto),

                "fuente":
                    self.FUENTE,

                "fecha":
                    datetime.now().isoformat()
            }

            experiencia = {

                "tipo":
                    "alimentacion_externa",

                "concepto":
                    conocimiento["concepto"],

                "fuente":
                    self.FUENTE,

                "fecha":
                    datetime.now().isoformat()
            }

            self.experiencias.append(
                experiencia
            )

            return {

                "ok": True,

                "conocimiento":
                    conocimiento,

                "experiencia":
                    experiencia
            }

        except requests.RequestException as error:

            return {

                "ok": False,

                "error":
                    f"Error de conexión: {error}"
            }

        except Exception as error:

            return {

                "ok": False,

                "error":
                    f"Error procesando información: {error}"
            }

    # ========================================================
    # PREPARAR PARA MEMORIA
    # ========================================================

    def preparar_para_memoria(
        self,
        resultado
    ):

        if not resultado.get("ok"):

            return None

        conocimiento = resultado[
            "conocimiento"
        ]

        return {

            "concepto":
                conocimiento["concepto"].lower(),

            "informacion":
                conocimiento["informacion"],

            "fuente":
                conocimiento["fuente"],

            "fecha":
                conocimiento["fecha"]
        }

    # ========================================================
    # ALIMENTAR
    # ========================================================

    def alimentar(
        self,
        concepto,
        idioma="es"
    ):

        resultado = self.buscar(
            concepto,
            idioma
        )

        if not resultado.get("ok"):

            return resultado

        memoria = (
            self.preparar_para_memoria(
                resultado
            )
        )

        return {

            "ok": True,

            "accion":
                "conocimiento_preparado",

            "memoria":
                memoria,

            "experiencia":
                resultado["experiencia"]
        }


# ============================================================
# PUNTO DE ENTRADA DEL MÓDULO
# ============================================================

def crear_modulo():

    return AlimentadorOmega()
