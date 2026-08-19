"""
CEREBRO OMEGA ∞
MÓDULO: ALIMENTADOR

Consulta conocimiento externo y lo prepara para que
el núcleo de CEREBRO OMEGA pueda incorporarlo.

IMPORTANTE:
Este módulo NO modifica el núcleo.
"""

import requests
import re
from datetime import datetime


class AlimentadorOmega:

    VERSION = "1.0.0"
    NOMBRE = "ALIMENTADOR OMEGA"

    def __init__(self):
        self.fuente = "Wikipedia"
        self.experiencias = []

    def limpiar(self, texto):
        """Limpia espacios y caracteres innecesarios."""
        if not texto:
            return ""

        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()

    def buscar(self, concepto, idioma="es"):
        """
        Busca información sobre un concepto en Wikipedia.

        Devuelve un paquete de conocimiento.
        """

        concepto = self.limpiar(concepto)

        if not concepto:
            return {
                "ok": False,
                "error": "No se recibió ningún concepto."
            }

        url = f"https://{idioma}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(concepto)}"

        try:
            respuesta = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "CEREBRO-OMEGA/1.0"
                }
            )

            if respuesta.status_code != 200:
                return {
                    "ok": False,
                    "error": f"No se encontró información sobre: {concepto}"
                }

            datos = respuesta.json()

            titulo = datos.get("title", concepto)
            descripcion = datos.get("description", "")
            extracto = datos.get("extract", "")

            conocimiento = {
                "concepto": titulo,
                "descripcion": self.limpiar(descripcion),
                "informacion": self.limpiar(extracto),
                "fuente": self.fuente,
                "fecha": datetime.now().isoformat()
            }

            self.experiencias.append({
                "tipo": "alimentacion_externa",
                "concepto": titulo,
                "fuente": self.fuente,
                "fecha": datetime.now().isoformat()
            })

            return {
                "ok": True,
                "conocimiento": conocimiento
            }

        except requests.RequestException as e:

            return {
                "ok": False,
                "error": f"Error de conexión: {str(e)}"
            }

        except Exception as e:

            return {
                "ok": False,
                "error": f"Error procesando conocimiento: {str(e)}"
            }

    def preparar_para_memoria(self, resultado):
        """
        Convierte el resultado en un formato sencillo
        que el sistema de memoria puede guardar.
        """

        if not resultado.get("ok"):
            return None

        conocimiento = resultado["conocimiento"]

        return {
            "concepto": conocimiento["concepto"].lower(),
            "informacion": conocimiento["informacion"],
            "fuente": conocimiento["fuente"],
            "fecha": conocimiento["fecha"]
        }

    def alimentar(self, concepto, idioma="es"):
        """
        Flujo completo:

        BUSCAR
        ↓
        PROCESAR
        ↓
        PREPARAR
        ↓
        ENTREGAR AL SISTEMA
        """

        resultado = self.buscar(concepto, idioma)

        if not resultado["ok"]:
            return resultado

        memoria = self.preparar_para_memoria(resultado)

        return {
            "ok": True,
            "accion": "conocimiento_preparado",
            "memoria": memoria,
            "experiencia": self.experiencias[-1]
        }


def crear_modulo():
    """Punto de entrada estándar del módulo."""
    return AlimentadorOmega()
