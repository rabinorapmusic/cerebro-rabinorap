"""
CEREBRO OMEGA ∞
MÓDULO: ALIMENTADOR

Consulta conocimiento externo y lo prepara para que
el núcleo de CEREBRO OMEGA pueda incorporarlo.

IMPORTANTE:
Este módulo NO modifica el núcleo.
"""

impor requests
importre
fro datetime importdatetime


clas AlimentadorOmega:

    VERSION = "1.0.0"
    NOMBRE = "ALIMENTADOR OMEGA"

    def__init__(self):
        self.fuente = "Wikipedia"
        self.experiencias = []

    deflimpiar(self, texto):
        """Limpia espacios y caracteres innecesarios."""
        i no texto:
            retur ""

        texto = re.sub(r"\s+", " ", texto)
        retur texto.strip()

    de buscar(self, concepto, idioma="es"):
        """
        Busca información sobre un concepto en Wikipedia.

        Devuelve un paquete de conocimiento.
        """

        concepto = self.limpiar(concepto)

        i no concepto:
            retur {
                "ok": False,
                "error": "No se recibió ningún concepto."
            }

        url = f"https://{idioma}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(concepto)}"

        tr:
            respuesta = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "CEREBRO-OMEGA/1.0"
                }
            )

            ifrespuesta.status_code != 200:
                retur {
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

            retur {
                "ok": True,
                "conocimiento": conocimiento
            }

        exceptrequests.RequestException a e:

            retur {
                "ok": False,
                "error": f"Error de conexión: {str(e)}"
            }

        exceptException ase:

            retur {
                "ok": False,
                "error": f"Error procesando conocimiento: {str(e)}"
            }

    de
preparar_para_memoria(self, resultado):
        """
        Convierte el resultado en un formato sencillo
        que el sistema de memoria puede guardar.
        """

        i notresultado.get("ok"):
            retur Non

        conocimiento = resultado["conocimiento"]

        retur {
            "concepto": conocimiento["concepto"].lower(),
            "informacion": conocimiento["informacion"],
            "fuente": conocimiento["fuente"],
            "fecha": conocimiento["fecha"]
        }

    de alimentar(self, concepto, idioma="es"):
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

        i notresultado["ok"]:
            retur resultado

        memoria = self.preparar_para_memoria(resultado)

        retur {
            "ok": True,
            "accion": "conocimiento_preparado",
            "memoria": memoria,
            "experiencia": self.experiencias[-1]
        }


defcrear_modulo():
    """Punto de entrada estándar del módulo."""
    retur AlimentadorOmega()
