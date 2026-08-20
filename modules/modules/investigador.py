"""
============================================================
CEREBRO OMEGA ∞
MÓDULO: INVESTIGADOR OMEGA
VERSIÓN: 2.0.0

Motor de investigación externa.

OBJETIVO
--------
Transformar una pregunta en una investigación estructurada:

    PREGUNTA
       ↓
    DESCOMPOSICIÓN
       ↓
    CONSULTAS
       ↓
    BÚSQUEDA DE FUENTES
       ↓
    EXTRACCIÓN
       ↓
    LIMPIEZA
       ↓
    DEDUPLICACIÓN
       ↓
    EVALUACIÓN
       ↓
    COMPARACIÓN
       ↓
    CONTRADICCIONES
       ↓
    SÍNTESIS
       ↓
    CONCLUSIONES
       ↓
    CONOCIMIENTO PROPUESTO

IMPORTANTE
----------
Este módulo NO modifica directamente la memoria principal.
Devuelve resultados para que CEREBRO OMEGA decida qué guardar.

Fuentes principales:
- Wikipedia / MediaWiki
- Wikidata
- Crossref

Diseñado para funcionar como módulo independiente.
============================================================
"""

import re
import time
import hashlib
from datetime import datetime
from urllib.parse import quote, urlparse

import requests


class InvestigadorOmega:

    VERSION = "2.0.0"
    NOMBRE = "INVESTIGADOR OMEGA"

    USER_AGENT = (
        "CEREBRO-OMEGA/2.0 "
        "(motor de investigacion modular)"
    )

    TIMEOUT = 12

    MAX_RESULTADOS = 12

    MAX_TEXTO = 5000

    def __init__(
        self,
        idioma="es",
        max_resultados=12
    ):

        self.idioma = idioma
        self.max_resultados = max(
            3,
            min(max_resultados, 30)
        )

        self.experiencias = []

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": self.USER_AGENT,
            "Accept": "application/json"
        })

    # ========================================================
    # UTILIDADES
    # ========================================================

    def limpiar(self, texto):

        if not texto:
            return ""

        texto = re.sub(
            r"<[^>]+>",
            " ",
            str(texto)
        )

        texto = re.sub(
            r"\s+",
            " ",
            texto
        )

        return texto.strip()

    # ========================================================
    # HUELLA
    # ========================================================

    def huella(self, texto):

        return hashlib.sha256(
            texto.lower()
            .strip()
            .encode("utf-8")
        ).hexdigest()[:16]

    # ========================================================
    # DOMINIO
    # ========================================================

    def dominio(self, url):

        try:

            return urlparse(url).netloc.lower()

        except Exception:

            return ""

    # ========================================================
    # PETICIÓN SEGURA
    # ========================================================

    def get_json(
        self,
        url,
        params=None
    ):

        try:

            respuesta = self.session.get(
                url,
                params=params,
                timeout=self.TIMEOUT
            )

            if respuesta.status_code != 200:

                return None

            return respuesta.json()

        except Exception:

            return None

    # ========================================================
    # ANALIZAR PREGUNTA
    # ========================================================

    def analizar_pregunta(self, pregunta):

        pregunta = self.limpiar(pregunta)

        palabras = re.findall(
            r"\b[\wáéíóúüñ]+\b",
            pregunta.lower()
        )

        palabras_clave = [
            palabra
            for palabra in palabras
            if len(palabra) >= 4
        ]

        tipo = "general"

        texto = pregunta.lower()

        if any(
            x in texto
            for x in [
                "historia",
                "histórico",
                "historico",
                "antes",
                "pasado",
                "origen",
                "fundó",
                "fundo"
            ]
        ):

            tipo = "histórico"

        elif any(
            x in texto
            for x in [
                "futuro",
                "podría",
                "podria",
                "pasará",
                "pasara",
                "escenario",
                "predecir"
            ]
        ):

            tipo = "futuros"

        elif any(
            x in texto
            for x in [
                "comparar",
                "compara",
                "diferencia",
                "mejor",
                "versus"
            ]
        ):

            tipo = "comparativo"

        elif any(
            x in texto
            for x in [
                "cómo funciona",
                "como funciona",
                "explica",
                "funciona"
            ]
        ):

            tipo = "explicativo"

        elif any(
            x in texto
            for x in [
                "por qué",
                "porque",
                "causa",
                "causó",
                "causo"
            ]
        ):

            tipo = "causal"

        return {

            "pregunta": pregunta,

            "tipo": tipo,

            "palabras_clave":
                list(dict.fromkeys(
                    palabras_clave
                )),

            "huella":
                self.huella(pregunta)
        }

    # ========================================================
    # GENERAR CONSULTAS
    # ========================================================

    def generar_consultas(
        self,
        pregunta,
        analisis
    ):

        base = self.limpiar(pregunta)

        consultas = [
            base
        ]

        tipo = analisis["tipo"]

        if tipo == "histórico":

            consultas.extend([
                f"{base} historia",
                f"{base} origen",
                f"{base} timeline"
            ])

        elif tipo == "causal":

            consultas.extend([
                f"{base} causas",
                f"{base} consecuencias",
                f"{base} evidencia"
            ])

        elif tipo == "comparativo":

            consultas.extend([
                f"{base} comparación",
                f"{base} diferencias",
                f"{base} similarities"
            ])

        elif tipo == "explicativo":

            consultas.extend([
                f"{base} explicación",
                f"{base} cómo funciona"
            ])

        elif tipo == "futuros":

            consultas.extend([
                f"{base} tendencias",
                f"{base} escenarios",
                f"{base} proyecciones"
            ])

        else:

            consultas.extend([
                f"{base} explicación",
                f"{base} información",
                f"{base} evidencia"
            ])

        resultado = []

        vistas = set()

        for consulta in consultas:

            consulta = self.limpiar(
                consulta
            )

            clave = consulta.lower()

            if clave not in vistas:

                vistas.add(clave)

                resultado.append(
                    consulta
                )

        return resultado[:8]

    # ========================================================
    # WIKIPEDIA / MEDIAWIKI
    # ========================================================

    def buscar_wikipedia(
        self,
        consulta
    ):

        endpoint = (
            f"https://{self.idioma}.wikipedia.org"
            "/w/api.php"
        )

        datos = self.get_json(
            endpoint,
            {
                "action": "query",
                "list": "search",
                "srsearch": consulta,
                "srlimit": 5,
                "format": "json"
            }
        )

        if not datos:

            return []

        resultados = []

        paginas = (
            datos
            .get("query", {})
            .get("search", [])
        )

        for pagina in paginas:

            titulo = self.limpiar(
                pagina.get(
                    "title",
                    ""
                )
            )

            if not titulo:
                continue

            url = (
                f"https://{self.idioma}"
                f".wikipedia.org/wiki/"
                f"{quote(titulo.replace(' ', '_'))}"
            )

            resumen = self.buscar_resumen_wikipedia(
                titulo
            )

            resultados.append({

                "titulo":
                    titulo,

                "texto":
                    resumen,

                "url":
                    url,

                "fuente":
                    "Wikipedia",

                "tipo_fuente":
                    "enciclopedia",

                "consulta":
                    consulta
            })

        return resultados

    # ========================================================
    # RESUMEN WIKIPEDIA
    # ========================================================

    def buscar_resumen_wikipedia(
        self,
        titulo
    ):

        url = (
            f"https://{self.idioma}.wikipedia.org"
            "/api/rest_v1/page/summary/"
            f"{quote(titulo)}"
        )

        datos = self.get_json(url)

        if not datos:

            return ""

        return self.limpiar(
            datos.get(
                "extract",
                ""
            )
        )

    # ========================================================
    # WIKIDATA
    # ========================================================

    def buscar_wikidata(
        self,
        consulta
    ):

        endpoint = (
            "https://www.wikidata.org/w/api.php"
        )

        datos = self.get_json(
            endpoint,
            {
                "action": "wbsearchentities",
                "search": consulta,
                "language": self.idioma,
                "limit": 5,
                "format": "json"
            }
        )

        if not datos:

            return []

        resultados = []

        for item in datos.get(
            "search",
            []
        ):

            etiqueta = self.limpiar(
                item.get(
                    "label",
                    ""
                )
            )

            descripcion = self.limpiar(
                item.get(
                    "description",
                    ""
                )
            )

            qid = item.get(
                "id",
                ""
            )

            if not etiqueta:

                continue

            resultados.append({

                "titulo":
                    etiqueta,

                "texto":
                    descripcion,

                "url":
                    f"https://www.wikidata.org/wiki/{qid}",

                "fuente":
                    "Wikidata",

                "tipo_fuente":
                    "base_conocimiento",

                "consulta":
                    consulta
            })

        return resultados

    # ========================================================
    # CROSSREF
    # ========================================================

    def buscar_crossref(
        self,
        consulta
    ):

        endpoint = (
            "https://api.crossref.org/works"
        )

        datos = self.get_json(
            endpoint,
            {
                "query.bibliographic":
                    consulta,

                "rows":
                    5
            }
        )

        if not datos:

            return []

        resultados = []

        items = (
            datos
            .get("message", {})
            .get("items", [])
        )

        for item in items:

            titulo_lista = item.get(
                "title",
                []
            )

            titulo = ""

            if titulo_lista:

                titulo = self.limpiar(
                    titulo_lista[0]
                )

            autores = []

            for autor in item.get(
                "author",
                []
            )[:5]:

                nombre = " ".join(
                    filter(
                        None,
                        [
                            autor.get(
                                "given",
                                ""
                            ),
                            autor.get(
                                "family",
                                ""
                            )
                        ]
                    )
                )

                if nombre:

                    autores.append(
                        nombre
                    )

            fecha = (
                item
                .get("published-print", {})
                .get("date-parts", [[]])
            )

            año = ""

            if fecha and fecha[0]:

                año = str(
                    fecha[0][0]
                )

            url = item.get(
                "URL",
                ""
            )

            texto = titulo

            if autores:

                texto += (
                    ". Autores: "
                    + ", ".join(autores)
                )

            if año:

                texto += (
                    f". Año: {año}"
                )

            if not titulo:

                continue

            resultados.append({

                "titulo":
                    titulo,

                "texto":
                    self.limpiar(texto),

                "url":
                    url,

                "fuente":
                    "Crossref",

                "tipo_fuente":
                    "bibliografica",

                "consulta":
                    consulta
            })

        return resultados

    # ========================================================
    # PUNTUACIÓN DE FUENTES
    # ========================================================

    def puntuar_fuente(
        self,
        resultado
    ):

        puntuacion = 0

        fuente = resultado.get(
            "fuente",
            ""
        )

        tipo = resultado.get(
            "tipo_fuente",
            ""
        )

        texto = resultado.get(
            "texto",
            ""
        )

        if fuente == "Crossref":

            puntuacion += 3

        elif fuente == "Wikidata":

            puntuacion += 2

        elif fuente == "Wikipedia":

            puntuacion += 2

        if tipo == "bibliografica":

            puntuacion += 2

        if len(texto) > 300:

            puntuacion += 1

        if resultado.get("url"):

            puntuacion += 1

        return puntuacion

    # ========================================================
    # DEDUPLICACIÓN
    # ========================================================

    def deduplicar(
        self,
        resultados
    ):

        encontrados = {}

        for resultado in resultados:

            titulo = self.limpiar(
                resultado.get(
                    "titulo",
                    ""
                )
            )

            texto = self.limpiar(
                resultado.get(
                    "texto",
                    ""
                )
            )

            clave = self.huella(
                titulo + "|" + texto[:500]
            )

            if clave not in encontrados:

                resultado["id"] = clave

                resultado["puntuacion"] = (
                    self.puntuar_fuente(
                        resultado
                    )
                )

                encontrados[clave] = resultado

            else:

                actual = encontrados[clave]

                actual["puntuacion"] = max(
                    actual["puntuacion"],
                    self.puntuar_fuente(
                        resultado
                    )
                )

        resultados = list(
            encontrados.values()
        )

        resultados.sort(
            key=lambda x: x.get(
                "puntuacion",
                0
            ),
            reverse=True
        )

        return resultados[
            :self.max_resultados
        ]

    # ========================================================
    # NORMALIZACIÓN DE TEXTO
    # ========================================================

    def palabras_importantes(
        self,
        texto
    ):

        stopwords = {
            "para",
            "como",
            "este",
            "esta",
            "estos",
            "estas",
            "sobre",
            "desde",
            "entre",
            "donde",
            "cuando",
            "porque",
            "también",
            "tambien",
            "tiene",
            "tener",
            "fue",
            "son",
            "los",
            "las",
            "del",
            "una",
            "uno",
            "que",
            "con",
            "por",
            "sus"
        }

        palabras = re.findall(
            r"\b[\wáéíóúüñ]+\b",
            texto.lower()
        )

        return {
            p
            for p in palabras
            if len(p) >= 5
            and p not in stopwords
        }

    # ========================================================
    # SIMILITUD ENTRE FUENTES
    # ========================================================

    def similitud(
        self,
        texto_a,
        texto_b
    ):

        a = self.palabras_importantes(
            texto_a
        )

        b = self.palabras_importantes(
            texto_b
        )

        if not a or not b:

            return 0.0

        interseccion = len(
            a.intersection(b)
        )

        union = len(
            a.union(b)
        )

        if union == 0:

            return 0.0

        return round(
            interseccion / union,
            3
        )

    # ========================================================
    # AGRUPAR EVIDENCIAS
    # ========================================================

    def agrupar_evidencias(
        self,
        resultados
    ):

        grupos = []

        for resultado in resultados:

            colocado = False

            for grupo in grupos:

                similitud_maxima = max(
                    [
                        self.similitud(
                            resultado.get(
                                "texto",
                                ""
                            ),
                            otro.get(
                                "texto",
                                ""
                            )
                        )
                        for otro in grupo
                    ] or [0]
                )

                if similitud_maxima >= 0.25:

                    grupo.append(
                        resultado
                    )

                    colocado = True

                    break

            if not colocado:

                grupos.append([
                    resultado
                ])

        return grupos

    # ========================================================
    # DETECTAR POSIBLES CONTRADICCIONES
    # ========================================================

    def detectar_contradicciones(
        self,
        resultados
    ):

        contradicciones = []

        patrones = [

            r"\bno\b",

            r"\bnunca\b",

            r"\bjamás\b",

            r"\bjamás\b",

            r"\bfalso\b",

            r"\bincorrecto\b",

            r"\bdesconocido\b",

            r"\bcontrovertido\b"
        ]

        for i in range(
            len(resultados)
        ):

            texto_a = resultados[i].get(
                "texto",
                ""
            )

            for j in range(
                i + 1,
                len(resultados)
            ):

                texto_b = resultados[j].get(
                    "texto",
                    ""
                )

                similitud = self.similitud(
                    texto_a,
                    texto_b
                )

                if similitud < 0.08:

                    continue

                negativo_a = any(
                    re.search(
                        patron,
                        texto_a.lower()
                    )
                    for patron in patrones
                )

                negativo_b = any(
                    re.search(
                        patron,
                        texto_b.lower()
                    )
                    for patron in patrones
                )

                if negativo_a != negativo_b:

                    contradicciones.append({

                        "fuente_a":
                            resultados[i].get(
                                "fuente"
                            ),

                        "fuente_b":
                            resultados[j].get(
                                "fuente"
                            ),

                        "tema_a":
                            resultados[i].get(
                                "titulo"
                            ),

                        "tema_b":
                            resultados[j].get(
                                "titulo"
                            ),

                        "similitud":
                            similitud,

                        "tipo":
                            "posible_contradiccion",

                        "advertencia":
                            (
                                "Las fuentes contienen "
                                "señales lingüísticas "
                                "potencialmente diferentes."
                            )
                    })

        return contradicciones

    # ========================================================
    # CALCULAR CONFIANZA
    # ========================================================

    def calcular_confianza(
        self,
        resultados,
        contradicciones
    ):

        if not resultados:

            return 0

        fuentes = set(
            r.get(
                "fuente"
            )
            for r in resultados
        )

        puntuacion = 25

        puntuacion += min(
            len(resultados) * 5,
            30
        )

        puntuacion += min(
            len(fuentes) * 8,
            24
        )

        if len(resultados) >= 3:

            puntuacion += 10

        puntuacion -= min(
            len(contradicciones) * 8,
            30
        )

        return max(
            0,
            min(
                100,
                puntuacion
            )
        )

    # ========================================================
    # NIVEL DE CONFIANZA
    # ========================================================

    def nivel_confianza(
        self,
        puntuacion
    ):

        if puntuacion >= 80:

            return "ALTA"

        if puntuacion >= 55:

            return "MEDIA"

        if puntuacion >= 30:

            return "BAJA"

        return "INSUFICIENTE"

    # ========================================================
    # CONSTRUIR SÍNTESIS
    # ========================================================

    def sintetizar(
        self,
        pregunta,
        resultados
    ):

        if not resultados:

            return (
                "No se obtuvo suficiente "
                "información externa para "
                "construir una síntesis."
            )

        partes = []

        vistos = set()

        for resultado in resultados:

            texto = self.limpiar(
                resultado.get(
                    "texto",
                    ""
                )
            )

            if not texto:

                continue

            clave = self.huella(
                texto[:700]
            )

            if clave in vistos:

                continue

            vistos.add(clave)

            fuente = resultado.get(
                "fuente",
                "fuente desconocida"
            )

            partes.append(
                f"[{fuente}] {texto}"
            )

        if not partes:

            return (
                "Las fuentes fueron encontradas "
                "pero no contienen suficiente "
                "texto utilizable."
            )

        texto_final = (
            f"Investigación sobre: {pregunta}\n\n"
            + "\n\n".join(partes)
        )

        return texto_final[
            :self.MAX_TEXTO
        ]

    # ========================================================
    # EXTRAER CONCLUSIONES
    # ========================================================

    def extraer_conclusiones(
        self,
        resultados
    ):

        conclusiones = []

        for resultado in resultados:

            texto = self.limpiar(
                resultado.get(
                    "texto",
                    ""
                )
            )

            if not texto:

                continue

            frases = re.split(
                r"(?<=[.!?])\s+",
                texto
            )

            for frase in frases:

                frase = frase.strip()

                if len(frase) < 40:

                    continue

                conclusiones.append({

                    "conclusion":
                        frase[:500],

                    "fuente":
                        resultado.get(
                            "fuente"
                        ),

                    "url":
                        resultado.get(
                            "url"
                        )
                })

                if len(conclusiones) >= 10:

                    return conclusiones

        return conclusiones

    # ========================================================
    # CREAR PROPUESTA DE MEMORIA
    # ========================================================

    def preparar_memoria(
        self,
        pregunta,
        analisis,
        resultados,
        confianza
    ):

        if not resultados:

            return None

        sintesis = self.sintetizar(
            pregunta,
            resultados
        )

        fuentes = []

        for resultado in resultados:

            fuente = {

                "nombre":
                    resultado.get(
                        "fuente"
                    ),

                "url":
                    resultado.get(
                        "url"
                    ),

                "titulo":
                    resultado.get(
                        "titulo"
                    )
            }

            fuentes.append(
                fuente
            )

        return {

            "concepto":
                pregunta.strip().lower(),

            "informacion":
                sintesis,

            "tipo":
                "investigacion",

            "confianza":
                confianza,

            "nivel_confianza":
                self.nivel_confianza(
                    confianza
                ),

            "fuentes":
                fuentes,

            "fecha":
                datetime.now().isoformat(),

            "investigador":
                self.VERSION
        }

    # ========================================================
    # INVESTIGACIÓN COMPLETA
    # ========================================================

    def investigar(
        self,
        pregunta,
        profundidad=2
    ):

        inicio = time.time()

        pregunta = self.limpiar(
            pregunta
        )

        if not pregunta:

            return {

                "ok": False,

                "error":
                    "No se recibió ninguna pregunta."
            }

        profundidad = max(
            1,
            min(
                int(profundidad),
                4
            )
        )

        analisis = self.analizar_pregunta(
            pregunta
        )

        consultas = self.generar_consultas(
            pregunta,
            analisis
        )

        # --------------------------------------------
        # RESULTADOS
        # --------------------------------------------

        resultados = []

        for consulta in consultas:

            resultados.extend(
                self.buscar_wikipedia(
                    consulta
                )
            )

            if profundidad >= 2:

                resultados.extend(
                    self.buscar_wikidata(
                        consulta
                    )
                )

            if profundidad >= 3:

                resultados.extend(
                    self.buscar_crossref(
                        consulta
                    )
                )

            # Evita sobrecargar las APIs
            time.sleep(0.15)

        # --------------------------------------------
        # LIMPIEZA
        # --------------------------------------------

        resultados = self.deduplicar(
            resultados
        )

        grupos = self.agrupar_evidencias(
            resultados
        )

        contradicciones = (
            self.detectar_contradicciones(
                resultados
            )
        )

        confianza = self.calcular_confianza(
            resultados,
            contradicciones
        )

        nivel = self.nivel_confianza(
            confianza
        )

        conclusiones = (
            self.extraer_conclusiones(
                resultados
            )
        )

        memoria = self.preparar_memoria(
            pregunta,
            analisis,
            resultados,
            confianza
        )

        duracion = round(
            time.time() - inicio,
            2
        )

        experiencia = {

            "tipo":
                "investigacion",

            "pregunta":
                pregunta,

            "tipo_pregunta":
                analisis["tipo"],

            "fuentes_consultadas":
                sorted(
                    set(
                        r.get(
                            "fuente"
                        )
                        for r in resultados
                    )
                ),

            "resultados":
                len(resultados),

            "grupos_evidencia":
                len(grupos),

            "contradicciones":
                len(contradicciones),

            "confianza":
                confianza,

            "fecha":
                datetime.now().isoformat(),

            "duracion_segundos":
                duracion
        }

        self.experiencias.append(
            experiencia
        )

        return {

            "ok":
                bool(resultados),

            "investigador":
                self.NOMBRE,

            "version":
                self.VERSION,

            "pregunta":
                pregunta,

            "analisis":
                analisis,

            "consultas":
                consultas,

            "resultados":
                resultados,

            "evidencias":
                grupos,

            "contradicciones":
                contradicciones,

            "conclusiones":
                conclusiones,

            "confianza":
                confianza,

            "nivel_confianza":
                nivel,

            "memoria":
                memoria,

            "experiencia":
                experiencia,

            "duracion_segundos":
                duracion
        }

    # ========================================================
    # ESTADO
    # ========================================================

    def estado(self):

        return {

            "nombre":
                self.NOMBRE,

            "version":
                self.VERSION,

            "idioma":
                self.idioma,

            "experiencias":
                len(self.experiencias),

            "fuentes":
                [
                    "Wikipedia",
                    "Wikidata",
                    "Crossref"
                ]
        }


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

def crear_modulo():

    return InvestigadorOmega()
