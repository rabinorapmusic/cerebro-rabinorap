"""
============================================================
CEREBRO OMEGA ∞
ORQUESTADOR OMEGA
VERSIÓN 1.0.0

CENTRO DE COORDINACIÓN DE INTELIGENCIA

Este módulo NO reemplaza:
    - el núcleo
    - la memoria
    - el Alimentador
    - el Investigador

Los coordina.

FLUJO:

ORDEN
  ↓
ANÁLISIS
  ↓
MEMORIA
  ↓
PLAN
  ↓
INVESTIGACIÓN / IA / RAZONAMIENTO
  ↓
EVALUACIÓN
  ↓
RESPUESTA
  ↓
PROPUESTA DE MEMORIA

La IA puede PROPONER conocimiento.
La memoria principal decide cuándo GUARDARLO.

============================================================
"""

import os
import re
import json
import hashlib
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class OrquestadorOmega:

    VERSION = "1.0.0"
    NOMBRE = "ORQUESTADOR OMEGA"

    MODELO = os.getenv(
        "OMEGA_MODEL",
        "gpt-5.6-luna"
    )

    MAX_MEMORIA = 12000
    MAX_INVESTIGACION = 14000
    MAX_RESPUESTA = 12000

    def __init__(
        self,
        memoria=None,
        alimentador=None,
        investigador=None
    ):

        self.memoria = memoria or {}
        self.alimentador = alimentador
        self.investigador = investigador

        self.experiencias = []

        self.cliente = None

        self.api_disponible = False

        self._inicializar_api()

    # ========================================================
    # API
    # ========================================================

    def _inicializar_api(self):

        if OpenAI is None:
            return

        clave = os.getenv(
            "OPENAI_API_KEY"
        )

        if not clave:
            return

        try:

            self.cliente = OpenAI(
                api_key=clave
            )

            self.api_disponible = True

        except Exception:

            self.cliente = None
            self.api_disponible = False

    # ========================================================
    # UTILIDADES
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
    # HUELLA
    # ========================================================

    def huella(self, texto):

        return hashlib.sha256(
            self.limpiar(texto)
            .lower()
            .encode("utf-8")
        ).hexdigest()[:16]

    # ========================================================
    # ANALIZAR ORDEN
    # ========================================================

    def analizar_orden(self, orden):

        texto = self.limpiar(
            orden
        )

        bajo = texto.lower()

        palabras = re.findall(
            r"\b[\wáéíóúüñ]+\b",
            bajo
        )

        intencion = "general"

        if any(
            palabra in bajo
            for palabra in [
                "aprende",
                "enseña",
                "memoriza",
                "recuerda",
                "guarda"
            ]
        ):

            intencion = "aprendizaje"

        elif any(
            palabra in bajo
            for palabra in [
                "investiga",
                "investigar",
                "busca",
                "fuentes",
                "evidencia"
            ]
        ):

            intencion = "investigacion"

        elif any(
            palabra in bajo
            for palabra in [
                "historia",
                "histórico",
                "historico",
                "pasado",
                "antes",
                "origen"
            ]
        ):

            intencion = "historico"

        elif any(
            palabra in bajo
            for palabra in [
                "futuro",
                "futuros",
                "podría",
                "podria",
                "escenario",
                "escenarios",
                "proyección",
                "proyeccion"
            ]
        ):

            intencion = "futuros"

        elif any(
            palabra in bajo
            for palabra in [
                "compara",
                "comparar",
                "diferencias",
                "versus",
                "mejor"
            ]
        ):

            intencion = "comparacion"

        elif any(
            palabra in bajo
            for palabra in [
                "analiza",
                "analizar",
                "razona",
                "razonar",
                "resuelve",
                "explica"
            ]
        ):

            intencion = "razonamiento"

        return {

            "orden": texto,

            "intencion": intencion,

            "palabras":
                palabras,

            "huella":
                self.huella(texto)
        }

    # ========================================================
    # MEMORIA
    # ========================================================

    def contexto_memoria(
        self,
        consulta
    ):

        conocimiento = (
            self.memoria
            .get(
                "conocimiento",
                {}
            )
        )

        if not conocimiento:
            return ""

        consulta = consulta.lower()

        encontrados = []

        for concepto, informacion in (
            conocimiento.items()
        ):

            concepto_limpio = concepto.lower()

            coincide = (
                concepto_limpio in consulta
            )

            if not coincide:

                palabras = (
                    concepto_limpio.split()
                )

                coincide = any(
                    len(p) >= 4
                    and p in consulta
                    for p in palabras
                )

            if coincide:

                encontrados.append(
                    {
                        "concepto":
                            concepto,

                        "informacion":
                            informacion
                    }
                )

        texto = json.dumps(
            encontrados,
            ensure_ascii=False,
            indent=2
        )

        return texto[
            :self.MAX_MEMORIA
        ]

    # ========================================================
    # PLAN DE ACCIÓN
    # ========================================================

    def crear_plan(
        self,
        analisis,
        memoria_disponible
    ):

        intencion = analisis[
            "intencion"
        ]

        acciones = []

        if memoria_disponible:

            acciones.append(
                "usar_memoria"
            )

        if intencion == "investigacion":

            acciones.extend([
                "investigar",
                "evaluar_fuentes"
            ])

        elif intencion == "historico":

            acciones.extend([
                "investigar",
                "analizar_pasado",
                "comparar_fuentes"
            ])

        elif intencion == "futuros":

            acciones.extend([
                "investigar_tendencias",
                "analizar_variables",
                "crear_escenarios"
            ])

        elif intencion == "comparacion":

            acciones.extend([
                "buscar_datos",
                "comparar"
            ])

        elif intencion == "razonamiento":

            acciones.append(
                "razonar"
            )

        elif intencion == "aprendizaje":

            acciones.append(
                "evaluar_para_aprendizaje"
            )

        else:

            acciones.append(
                "razonar"
            )

        if self.api_disponible:

            acciones.append(
                "consultar_modelo"
            )

        return list(
            dict.fromkeys(
                acciones
            )
        )

    # ========================================================
    # INVESTIGACIÓN
    # ========================================================

    def investigar(
        self,
        pregunta
    ):

        if self.investigador is None:

            return None

        try:

            resultado = (
                self.investigador.investigar(
                    pregunta,
                    profundidad=3
                )
            )

            return resultado

        except Exception as error:

            return {
                "ok": False,
                "error":
                    str(error)
            }

    # ========================================================
    # CONTEXTO DE INVESTIGACIÓN
    # ========================================================

    def preparar_investigacion(
        self,
        resultado
    ):

        if not resultado:

            return ""

        datos = {

            "pregunta":
                resultado.get(
                    "pregunta"
                ),

            "confianza":
                resultado.get(
                    "confianza"
                ),

            "nivel_confianza":
                resultado.get(
                    "nivel_confianza"
                ),

            "conclusiones":
                resultado.get(
                    "conclusiones",
                    []
                ),

            "contradicciones":
                resultado.get(
                    "contradicciones",
                    []
                ),

            "resultados":
                resultado.get(
                    "resultados",
                    []
                )
        }

        return json.dumps(
            datos,
            ensure_ascii=False,
            indent=2
        )[
            :self.MAX_INVESTIGACION
        ]

    # ========================================================
    # PROMPT PRINCIPAL
    # ========================================================

    def construir_instrucciones(
        self,
        analisis,
        memoria,
        investigacion
    ):

        return f"""
Eres el motor de inteligencia de CEREBRO OMEGA ∞.

Tu función es ayudar a CEREBRO a:

- analizar
- razonar
- comparar
- investigar
- evaluar evidencia
- relacionar conceptos
- estudiar el pasado
- construir escenarios futuros
- identificar incertidumbres
- proponer conocimiento

REGLAS IMPORTANTES:

1. No inventes hechos.
2. Distingue hechos de inferencias.
3. Si existe incertidumbre, dilo.
4. No presentes futuros potenciales como hechos.
5. No afirmes que una fuente demuestra algo
   si realmente no lo demuestra.
6. La memoria proporcionada puede contener errores.
7. La investigación externa puede contener errores.
8. La propuesta de memoria NO significa que
   el conocimiento ya haya sido guardado.
9. No puedes modificar directamente la memoria.
10. Responde en español salvo que se solicite otro idioma.

TIPO DE ORDEN:

{analisis["intencion"]}

MEMORIA DISPONIBLE:

{memoria if memoria else "No hay conocimiento relevante."}

INVESTIGACIÓN DISPONIBLE:

{investigacion if investigacion else "No se realizó investigación externa."}

Cuando sea apropiado, estructura tu respuesta conceptualmente como:

RESPUESTA
HECHOS
INFERENCIAS
INCERTIDUMBRES
FUENTES
CONCEPTOS RELACIONADOS
PROPUESTA DE APRENDIZAJE

No inventes fuentes.
"""

    # ========================================================
    # LLAMADA A OPENAI
    # ========================================================

    def consultar_modelo(
        self,
        orden,
        instrucciones
    ):

        if not self.api_disponible:

            return {

                "ok": False,

                "error":
                    "API de OpenAI no configurada."
            }

        try:

            response = (
                self.cliente.responses.create(

                    model=self.MODELO,

                    instructions=
                        instrucciones,

                    input=orden
                )
            )

            texto = getattr(
                response,
                "output_text",
                ""
            )

            texto = self.limpiar(
                texto
            )

            if not texto:

                return {

                    "ok": False,

                    "error":
                        "La API no devolvió texto."
                }

            return {

                "ok": True,

                "modelo":
                    self.MODELO,

                "respuesta":
                    texto[
                        :self.MAX_RESPUESTA
                    ]
            }

        except Exception as error:

            return {

                "ok": False,

                "error":
                    f"Error de API: {error}"
            }

    # ========================================================
    # PROPUESTA DE MEMORIA
    # ========================================================

    def crear_propuesta_memoria(
        self,
        orden,
        respuesta,
        investigacion
    ):

        if not respuesta:

            return None

        informacion = self.limpiar(
            respuesta
        )

        fuente = "OpenAI"

        if investigacion:

            fuentes = investigacion.get(
                "resultados",
                []
            )

            if fuentes:

                fuente = (
                    "OpenAI + investigación externa"
                )

        return {

            "concepto":
                self.limpiar(
                    orden
                ).lower(),

            "informacion":
                informacion,

            "fuente":
                fuente,

            "tipo":
                "propuesta_ia",

            "fecha":
                datetime.now().isoformat(),

            "aprobacion_requerida":
                True
        }

    # ========================================================
    # CREAR RESPUESTA LOCAL
    # ========================================================

    def respuesta_local(
        self,
        orden,
        analisis,
        memoria
    ):

        if memoria:

            return (
                "🧠 CEREBRO OMEGA procesó la orden.\n\n"
                f"🎯 Intención: "
                f"{analisis['intencion']}\n\n"
                "💾 Encontré conocimiento relacionado "
                "en la memoria.\n\n"
                f"{memoria}"
            )

        return (
            "🧠 CEREBRO OMEGA procesó la orden.\n\n"
            f"🎯 Intención detectada: "
            f"{analisis['intencion']}\n\n"
            "⚠️ No hay suficiente conocimiento "
            "local para responder con profundidad.\n\n"
            "💡 Puedes activar la investigación "
            "externa o conectar la API de IA."
        )

    # ========================================================
    # EJECUTAR
    # ========================================================

    def ejecutar(
        self,
        orden,
        investigar_automaticamente=True
    ):

        inicio = datetime.now()

        orden = self.limpiar(
            orden
        )

        if not orden:

            return {

                "ok": False,

                "error":
                    "No se recibió ninguna orden."
            }

        analisis = self.analizar_orden(
            orden
        )

        memoria = self.contexto_memoria(
            orden
        )

        plan = self.crear_plan(
            analisis,
            bool(memoria)
        )

        investigacion = None

        necesita_investigacion = (
            "investigar" in plan
            or
            "investigar_tendencias" in plan
        )

        if (
            investigar_automaticamente
            and necesita_investigacion
            and self.investigador is not None
        ):

            investigacion = self.investigar(
                orden
            )

        contexto_investigacion = (
            self.preparar_investigacion(
                investigacion
            )
        )

        instrucciones = (
            self.construir_instrucciones(
                analisis,
                memoria,
                contexto_investigacion
            )
        )

        respuesta_api = None

        if self.api_disponible:

            respuesta_api = (
                self.consultar_modelo(
                    orden,
                    instrucciones
                )
            )

        if (
            respuesta_api
            and respuesta_api.get("ok")
        ):

            respuesta = (
                respuesta_api["respuesta"]
            )

            origen = "api"

        else:

            respuesta = self.respuesta_local(
                orden,
                analisis,
                memoria
            )

            origen = "local"

        propuesta_memoria = (
            self.crear_propuesta_memoria(
                orden,
                respuesta,
                investigacion
            )
        )

        duracion = (
            datetime.now()
            - inicio
        ).total_seconds()

        experiencia = {

            "tipo":
                "orquestacion",

            "orden":
                orden,

            "intencion":
                analisis["intencion"],

            "plan":
                plan,

            "uso_memoria":
                bool(memoria),

            "uso_investigacion":
                investigacion is not None,

            "uso_api":
                origen == "api",

            "modelo":
                self.MODELO
                if origen == "api"
                else None,

            "fecha":
                datetime.now().isoformat(),

            "duracion":
                round(
                    duracion,
                    3
                )
        }

        self.experiencias.append(
            experiencia
        )

        return {

            "ok": True,

            "orquestador":
                self.NOMBRE,

            "version":
                self.VERSION,

            "respuesta":
                respuesta,

            "origen":
                origen,

            "analisis":
                analisis,

            "
