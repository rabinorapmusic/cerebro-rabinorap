import streamlit as st
import json
import os
import re
import hashlib
from datetime import datetime


# ============================================================
# 🧠 CEREBRO OMEGA ∞
# MOTOR COGNITIVO V3
# ============================================================
#
# ENTRADA
#   ↓
# COMPRENDER
#   ↓
# RECORDAR
#   ↓
# ASOCIAR
#   ↓
# DETECTAR PATRONES
#   ↓
# DETECTAR CONTRADICCIONES
#   ↓
# RAZONAR
#   ↓
# EVALUAR
#   ↓
# APRENDER
#   ↓
# ACTUALIZAR CONOCIMIENTO
#   ↓
# ∞
#
# TODO EN UN SOLO ARCHIVO
# ============================================================


st.set_page_config(
    page_title="CEREBRO OMEGA ∞ V3",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# ARCHIVO PRINCIPAL DE MEMORIA
# ============================================================

MEMORIA_FILE = "memoria_omega_v3.json"

VERSION = "3.0.0"


# ============================================================
# CEREBRO OMEGA
# ============================================================

class CerebroOmega:

    def __init__(self):

        self.memoria = self.cargar()

        self.ciclos = self.memoria.get(
            "ciclos",
            0
        )

        self.experiencias = self.memoria.get(
            "experiencias",
            []
        )

        self.conocimientos = self.memoria.get(
            "conocimientos",
            []
        )

        self.relaciones = self.memoria.get(
            "relaciones",
            []
        )

        self.patrones = self.memoria.get(
            "patrones",
            []
        )


    # ========================================================
    # MEMORIA VACÍA
    # ========================================================

    def memoria_vacia(self):

        return {

            "version": VERSION,

            "ciclos": 0,

            "experiencias": [],

            "conocimientos": [],

            "relaciones": [],

            "patrones": []

        }


    # ========================================================
    # CARGAR
    # ========================================================

    def cargar(self):

        if not os.path.exists(
            MEMORIA_FILE
        ):

            return self.memoria_vacia()

        try:

            with open(
                MEMORIA_FILE,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(
                    archivo
                )

            if not isinstance(
                datos,
                dict
            ):

                return self.memoria_vacia()

            base = self.memoria_vacia()

            for clave in base:

                if clave in datos:

                    base[clave] = datos[clave]

            return base

        except Exception:

            return self.memoria_vacia()


    # ========================================================
    # GUARDAR DE FORMA SEGURA
    # ========================================================

    def guardar(self):

        datos = {

            "version": VERSION,

            "ciclos": self.ciclos,

            "experiencias":
                self.experiencias,

            "conocimientos":
                self.conocimientos,

            "relaciones":
                self.relaciones,

            "patrones":
                self.patrones

        }

        temporal = MEMORIA_FILE + ".tmp"

        try:

            with open(
                temporal,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=2
                )

            os.replace(
                temporal,
                MEMORIA_FILE
            )

            return True

        except Exception:

            if os.path.exists(
                temporal
            ):

                try:

                    os.remove(
                        temporal
                    )

                except Exception:

                    pass

            return False


    # ========================================================
    # NORMALIZAR
    # ========================================================

    def normalizar(
        self,
        texto
    ):

        texto = str(
            texto or ""
        ).lower()

        texto = re.sub(
            r"\s+",
            " ",
            texto
        )

        return texto.strip()


    # ========================================================
    # EXTRAER CONCEPTOS
    # ========================================================

    def extraer_conceptos(
        self,
        texto
    ):

        texto = self.normalizar(
            texto
        )

        palabras = re.findall(
            r"[a-záéíóúüñ0-9]+",
            texto
        )

        ignorar = {

            "que",
            "como",
            "para",
            "por",
            "una",
            "uno",
            "los",
            "las",
            "del",
            "con",
            "sin",
            "sobre",
            "este",
            "esta",
            "esto",
            "es",
            "son",
            "ser",
            "de",
            "la",
            "el",
            "en",
            "un",
            "y",
            "o",
            "a"

        }

        conceptos = []

        for palabra in palabras:

            if len(palabra) < 4:

                continue

            if palabra in ignorar:

                continue

            if palabra not in conceptos:

                conceptos.append(
                    palabra
                )

        return conceptos[:20]


    # ========================================================
    # ID ÚNICO
    # ========================================================

    def generar_id(
        self,
        texto
    ):

        base = (
            self.normalizar(texto)
            + str(datetime.now())
        )

        return hashlib.sha256(
            base.encode(
                "utf-8"
            )
        ).hexdigest()[:16]


    # ========================================================
    # SIMILITUD
    # ========================================================

    def similitud(
        self,
        texto1,
        texto2
    ):

        a = set(
            self.extraer_conceptos(
                texto1
            )
        )

        b = set(
            self.extraer_conceptos(
                texto2
            )
        )

        if not a or not b:

            return 0.0

        interseccion = a & b

        union = a | b

        return (
            len(interseccion)
            / len(union)
        )


    # ========================================================
    # RECORDAR
    # ========================================================

    def recordar(
        self,
        entrada,
        limite=7
    ):

        resultados = []

        for experiencia in self.experiencias:

            texto = (
                experiencia.get(
                    "entrada",
                    ""
                )
            )

            puntuacion = self.similitud(
                entrada,
                texto
            )

            if puntuacion > 0:

                resultados.append({

                    "id":
                        experiencia.get(
                            "id"
                        ),

                    "entrada":
                        texto,

                    "respuesta":
                        experiencia.get(
                            "respuesta",
                            ""
                        ),

                    "similitud":
                        round(
                            puntuacion,
                            3
                        )

                })

        resultados.sort(
            key=lambda x:
            x["similitud"],
            reverse=True
        )

        return resultados[:limite]


    # ========================================================
    # BUSCAR CONOCIMIENTOS
    # ========================================================

    def buscar_conocimientos(
        self,
        conceptos
    ):

        encontrados = []

        for conocimiento in (
            self.conocimientos
        ):

            conceptos_memoria = set(
                conocimiento.get(
                    "conceptos",
                    []
                )
            )

            coincidencias = (
                set(conceptos)
                & conceptos_memoria
            )

            if coincidencias:

                encontrados.append({

                    "conocimiento":
                        conocimiento,

                    "coincidencias":
                        list(
                            coincidencias
                        ),

                    "cantidad":
                        len(
                            coincidencias
                        )

                })

        encontrados.sort(
            key=lambda x:
            (
                x["cantidad"],
                x["conocimiento"].get(
                    "confianza",
                    0
                )
            ),
            reverse=True
        )

        return encontrados[:10]


    # ========================================================
    # DETECTAR CONTRADICCIONES
    # ========================================================

    def detectar_contradicciones(
        self,
        entrada,
        respuesta
    ):

        contradicciones = []

        entrada_conceptos = set(
            self.extraer_conceptos(
                entrada
            )
        )

        for conocimiento in (
            self.conocimientos
        ):

            conceptos = set(
                conocimiento.get(
                    "conceptos",
                    []
                )
            )

            coincidencias = (
                entrada_conceptos
                & conceptos
            )

            if not coincidencias:

                continue

            viejo = self.normalizar(
                conocimiento.get(
                    "contenido",
                    ""
                )
            )

            nuevo = self.normalizar(
                respuesta
            )

            if (
                viejo
                and nuevo
                and viejo != nuevo
            ):

                palabras_viejas = set(
                    self.extraer_conceptos(
                        viejo
                    )
                )

                palabras_nuevas = set(
                    self.extraer_conceptos(
                        nuevo
                    )
                )

                if (
                    palabras_viejas
                    and palabras_nuevas
                ):

                    diferencia = (
                        palabras_viejas
                        ^ palabras_nuevas
                    )

                    if len(diferencia) >= 2:

                        contradicciones.append({

                            "conocimiento_id":
                                conocimiento.get(
                                    "id"
                                ),

                            "anterior":
                                conocimiento.get(
                                    "contenido",
                                    ""
                                ),

                            "nuevo":
                                respuesta,

                            "conceptos_compartidos":
                                list(
                                    coincidencias
                                )

                        })

        return contradicciones[:5]


    # ========================================================
    # DETECTAR PATRONES
    # ========================================================

    def detectar_patrones(
        self,
        conceptos
    ):

        patrones = []

        for concepto in conceptos:

            apariciones = 0

            experiencias_ids = []

            for experiencia in (
                self.experiencias
            ):

                conceptos_exp = set(
                    experiencia.get(
                        "conceptos",
                        []
                    )
                )

                if concepto in conceptos_exp:

                    apariciones += 1

                    experiencias_ids.append(
                        experiencia.get(
                            "id"
                        )
                    )

            if apariciones >= 2:

                patrones.append({

                    "concepto":
                        concepto,

                    "apariciones":
                        apariciones,

                    "experiencias":
                        experiencias_ids[-10:]

                })

        return patrones


    # ========================================================
    # CREAR RELACIONES
    # ========================================================

    def crear_relaciones(
        self,
        conceptos
    ):

        nuevas = []

        for i in range(
            len(conceptos)
        ):

            for j in range(
                i + 1,
                len(conceptos)
            ):

                a = conceptos[i]

                b = conceptos[j]

                if a == b:

                    continue

                existe = False

                for relacion in (
                    self.relaciones
                ):

                    par = {
                        relacion.get("a"),
                        relacion.get("b")
                    }

                    if par == {a, b}:

                        existe = True

                        relacion[
                            "fuerza"
                        ] = (
                            relacion.get(
                                "fuerza",
                                1
                            ) + 1
                        )

                        break

                if not existe:

                    relacion = {

                        "a": a,

                        "b": b,

                        "fuerza": 1,

                        "fecha":
                            datetime.now().isoformat()

                    }

                    self.relaciones.append(
                        relacion
                    )

                    nuevas.append(
                        relacion
                    )

        return nuevas


    # ========================================================
    # EVALUAR
    # ========================================================

    def evaluar(
        self,
        entrada,
        respuesta,
        recuerdos,
        conocimientos,
        contradicciones
    ):

        claridad = 0.5

        coherencia = 0.5

        utilidad = 0.5


        if len(
            entrada.strip()
        ) >= 10:

            claridad = 0.8

        if len(
            entrada.strip()
        ) >= 40:

            claridad = 0.9


        if len(
            respuesta.strip()
        ) >= 10:

            coherencia = 0.8

        if len(
            respuesta.strip()
        ) >= 40:

            coherencia = 0.9


        if recuerdos:

            utilidad += 0.1

        if conocimientos:

            utilidad += 0.1

        if contradicciones:

            coherencia -= 0.1


        claridad = max(
            0.0,
            min(1.0, claridad)
        )

        coherencia = max(
            0.0,
            min(1.0, coherencia)
        )

        utilidad = max(
            0.0,
            min(1.0, utilidad)
        )


        confianza = (
            claridad
            + coherencia
            + utilidad
        ) / 3


        return {

            "claridad":
                round(
                    claridad,
                    2
                ),

            "coherencia":
                round(
                    coherencia,
                    2
                ),

            "utilidad":
                round(
                    utilidad,
                    2
                ),

            "confianza":
                round(
                    confianza,
                    2
                )

        }


    # ========================================================
    # RAZONAMIENTO
    # ========================================================

    def razonar(
        self,
        entrada,
        respuesta,
        conceptos,
        recuerdos,
        conocimientos,
        patrones,
        contradicciones
    ):

        partes = []


        # ----------------------------------------------------
        # COMPRENSIÓN
        # ----------------------------------------------------

        if conceptos:

            partes.append(
                "Conceptos detectados: "
                + ", ".join(
                    conceptos[:10]
                )
                + "."
            )


        # ----------------------------------------------------
        # MEMORIA
        # ----------------------------------------------------

        if recuerdos:

            mejor = recuerdos[0]

            partes.append(
                "La memoria contiene "
                f"una experiencia relacionada "
                f"(#{mejor['id']}) con "
                f"{mejor['similitud']:.0%} "
                "de similitud."
            )

        else:

            partes.append(
                "No existe una experiencia "
                "anterior suficientemente similar."
            )


        # ----------------------------------------------------
        # CONOCIMIENTO
        # ----------------------------------------------------

        if conocimientos:

            partes.append(
                "Existen conocimientos "
                "relacionados almacenados."
            )


        # ----------------------------------------------------
        # PATRONES
        # ----------------------------------------------------

        if patrones:

            nombres = [
                p["concepto"]
                for p in patrones[:5]
            ]

            partes.append(
                "Se detectaron patrones "
                "repetidos: "
                + ", ".join(
                    nombres
                )
                + "."
            )


        # ----------------------------------------------------
        # CONTRADICCIONES
        # ----------------------------------------------------

        if contradicciones:

            partes.append(
                "⚠️ Se detectaron posibles "
                "conflictos con conocimientos "
                "anteriores. El sistema no "
                "los elimina automáticamente."
            )

        else:

            partes.append(
                "No se detectaron "
                "contradicciones directas."
            )


        # ----------------------------------------------------
        # CONCLUSIÓN
        # ----------------------------------------------------

        partes.append(
            "La experiencia puede incorporarse "
            "a la memoria como conocimiento "
            "con el nivel de confianza obtenido "
            "durante este ciclo."
        )


        return " ".join(
            partes
        )


    # ========================================================
    # APRENDER CONOCIMIENTO
    # ========================================================

    def aprender_conocimiento(
        self,
        entrada,
        respuesta,
        conceptos,
        confianza
    ):

        contenido = (
            respuesta.strip()
            if respuesta.strip()
            else entrada.strip()
        )

        contenido_normalizado = (
            self.normalizar(
                contenido
            )
        )


        # ----------------------------------------------------
        # BUSCAR CONOCIMIENTO EXISTENTE
        # ----------------------------------------------------

        for conocimiento in (
            self.conocimientos
        ):

            existente = self.normalizar(
                conocimiento.get(
                    "contenido",
                    ""
                )
            )

            similitud = self.similitud(
                contenido_normalizado,
                existente
            )

            if similitud >= 0.75:

                conocimiento[
                    "veces_confirmado"
                ] = (
                    conocimiento.get(
                        "veces_confirmado",
                        1
                    ) + 1
                )

                conocimiento[
                    "confianza"
                ] = round(
                    min(
                        1.0,
                        conocimiento.get(
                            "confianza",
                            0.5
                        ) + 0.05
                    ),
                    2
                )

                conocimiento[
                    "ultima_actualizacion"
                ] = datetime.now().isoformat()

                return conocimiento


        # ----------------------------------------------------
        # NUEVO CONOCIMIENTO
        # ----------------------------------------------------

        conocimiento = {

            "id":
                len(
                    self.conocimientos
                ) + 1,

            "contenido":
                contenido,

            "conceptos":
                conceptos,

            "confianza":
                round(
                    confianza,
                    2
                ),

            "veces_confirmado":
                1,

            "fecha":
                datetime.now().isoformat(),

            "ultima_actualizacion":
                datetime.now().isoformat()

        }


        self.conocimientos.append(
            conocimiento
        )


        return conocimiento


    # ========================================================
    # EJECUTAR CICLO COGNITIVO
    # ========================================================

    def ejecutar(
        self,
        entrada,
        respuesta
    ):

        entrada = entrada.strip()

        respuesta = respuesta.strip()


        # ----------------------------------------------------
        # CICLO
        # ----------------------------------------------------

        self.ciclos += 1


        # ----------------------------------------------------
        # CONCEPTOS
        # ----------------------------------------------------

        conceptos = self.extraer_conceptos(
            entrada
            + " "
            + respuesta
        )


        # ----------------------------------------------------
        # RECORDAR
        # ----------------------------------------------------

        recuerdos = self.recordar(
            entrada
        )


        # ----------------------------------------------------
        # CONOCIMIENTOS
        # ----------------------------------------------------

        conocimientos = (
            self.buscar_conocimientos(
                conceptos
            )
        )


        # ----------------------------------------------------
        # CONTRADICCIONES
        # ----------------------------------------------------

        contradicciones = (
            self.detectar_contradicciones(
                entrada,
                respuesta
            )
        )


        # ----------------------------------------------------
        # PATRONES
        # ----------------------------------------------------

        patrones = self.detectar_patrones(
            conceptos
        )


        # ----------------------------------------------------
        # RELACIONES
        # ----------------------------------------------------

        relaciones = self.crear_relaciones(
            conceptos
        )


        # ----------------------------------------------------
        # EVALUACIÓN
        # ----------------------------------------------------

        evaluacion = self.evaluar(
            entrada,
            respuesta,
            recuerdos,
            conocimientos,
            contradicciones
        )


        # ----------------------------------------------------
        # RAZONAMIENTO
        # ----------------------------------------------------

        conclusion = self.razonar(
            entrada,
            respuesta,
            conceptos,
            recuerdos,
            conocimientos,
            patrones,
            contradicciones
        )


        # ----------------------------------------------------
        # EXPERIENCIA
        # ----------------------------------------------------

        experiencia = {

            "id":
                len(
                    self.experiencias
                ) + 1,

            "fecha":
                datetime.now().isoformat(),

            "ciclo":
                self.ciclos,

            "entrada":
                entrada,

            "respuesta":
                respuesta,

            "conceptos":
                conceptos,

            "evaluacion":
                evaluacion,

            "conclusion":
                conclusion,

            "memorias_relacionadas":
                len(recuerdos),

            "conocimientos_relacionados":
                len(conocimientos),

            "contradicciones":
                len(contradicciones),

            "relaciones_creadas":
                len(relaciones)

        }


        self.experiencias.append(
            experiencia
        )


        # ----------------------------------------------------
        # APRENDER
        # ----------------------------------------------------

        conocimiento = (
            self.aprender_conocimiento(
                entrada,
                respuesta,
                conceptos,
                evaluacion[
                    "confianza"
                ]
            )
        )


        # ----------------------------------------------------
        # ACTUALIZAR PATRONES
        # ----------------------------------------------------

        for patron in patrones:

            encontrado = False

            for existente in (
                self.patrones
            ):

                if (
                    existente.get(
                        "concepto"
                    )
                    ==
                    patron.get(
                        "concepto"
                    )
                ):

                    existente[
                        "apariciones"
                    ] = patron[
                        "apariciones"
                    ]

                    existente[
                        "ultima_actualizacion"
                    ] = datetime.now().isoformat()

                    encontrado = True

                    break


            if not encontrado:

                self.patrones.append(
                    patron
                )


        # ----------------------------------------------------
        # GUARDAR
        # ----------------------------------------------------

        guardado = self.guardar()


        return {

            "ciclo":
                self.ciclos,

            "conceptos":
                conceptos,

            "recuerdos":
                recuerdos,

            "conocimientos":
                conocimientos,

            "contradicciones":
                contradicciones,

            "patrones":
                patrones,

            "relaciones":
                relaciones,

            "evaluacion":
                evaluacion,

            "conclusion":
                conclusion,

            "conocimiento_aprendido":
                conocimiento,

            "guardado":
                guardado

        }


    # ========================================================
    # ESTADO
    # ========================================================

    def estado(self):

        return {

            "ciclos":
                self.ciclos,

            "experiencias":
                len(
                    self.experiencias
                ),

            "conocimientos":
                len(
                    self.conocimientos
                ),

            "relaciones":
                len(
                    self.relaciones
                ),

            "patrones":
                len(
                    self.patrones
                )

        }


    # ========================================================
    # BORRAR MEMORIA
    # ========================================================

    def borrar_memoria(self):

        self.ciclos = 0

        self.experiencias = []

        self.conocimientos = []

        self.relaciones = []

        self.patrones = []

        self.guardar()


# ============================================================
# INICIAR CEREBRO
# ============================================================

if (
    "cerebro_omega"
    not in st.session_state
):

    st.session_state.cerebro_omega = (
        CerebroOmega()
    )


cerebro = (
    st.session_state.cerebro_omega
)


# ============================================================
# CABECERA
# ============================================================

st.title(
    "🧠 CEREBRO OMEGA ∞"
)

st.caption(
    "MOTOR COGNITIVO V3"
)

st.write(
    "COMPRENDER → RECORDAR → ASOCIAR → "
    "RAZONAR → APRENDER → EVOLUCIONAR → ∞"
)


# ============================================================
# ESTADO
# ============================================================

estado = cerebro.estado()


a, b, c, d, e = st.columns(5)


with a:

    st.metric(
        "CICLOS",
        estado["ciclos"]
    )


with b:

    st.metric(
        "EXPERIENCIAS",
        estado["experiencias"]
    )


with c:

    st.metric(
        "CONOCIMIENTOS",
        estado["conocimientos"]
    )


with d:

    st.metric(
        "RELACIONES",
        estado["relaciones"]
    )


with e:

    st.metric(
        "PATRONES",
        estado["patrones"]
    )


st.divider()


# ============================================================
# CENTRO COGNITIVO
# ============================================================

st.header(
    "🧠 CENTRO COGNITIVO"
)


entrada = st.text_area(

    "Entrada",

    placeholder=(
        "Escribe una pregunta, idea, "
        "conocimiento o experiencia..."
    ),

    height=120
)


respuesta = st.text_area(

    "Respuesta / conocimiento",

    placeholder=(
        "Escribe aquí la respuesta "
        "o conocimiento que quieres "
        "que CEREBRO OMEGA analice..."
    ),

    height=150
)


if st.button(
    "♾️ EJECUTAR CICLO COGNITIVO",
    use_container_width=True
):

    if not entrada.strip():

        st.warning(
            "Escribe una entrada primero."
        )

    else:

        resultado = cerebro.ejecutar(
            entrada,
            respuesta
        )


        st.success(
            "♾️ CICLO "
            f"#{resultado['ciclo']} "
            "COMPLETADO"
        )


        # ====================================================
        # CONCLUSIÓN
        # ====================================================

        st.subheader(
            "🧠 CONCLUSIÓN DEL MOTOR"
        )

        st.info(
            resultado[
                "conclusion"
            ]
        )


        # ====================================================
        # CONCEPTOS
        # ====================================================

        st.subheader(
            "🔎 CONCEPTOS DETECTADOS"
        )

        if resultado[
            "conceptos"
        ]:

            st.write(
                " • ".join(
                    resultado[
                        "conceptos"
                    ]
                )
            )

        else:

            st.write(
                "No se detectaron conceptos."
            )


        # ====================================================
        # MEMORIA
        # ====================================================

        st.subheader(
            "📚 MEMORIA RECUPERADA"
        )

        recuerdos = resultado[
            "recuerdos"
        ]

        if recuerdos:

            for recuerdo in recuerdos:

                st.write(
                    f"🧠 Experiencia "
                    f"#{recuerdo['id']} "
                    f"— {recuerdo['similitud']:.0%}"
                )

                st.write(
                    recuerdo[
                        "entrada"
                    ]
                )

        else:

            st.write(
                "No había recuerdos relacionados."
            )


        # ====================================================
        # CONOCIMIENTOS
        # ====================================================

        st.subheader(
            "📖 CONOCIMIENTOS RELACIONADOS"
        )

        conocimientos = resultado[
            "conocimientos"
        ]

        if conocimientos:

            for item in conocimientos:

                conocimiento = item[
                    "conocimiento"
                ]

                st.write(
                    f"📖 #{conocimiento['id']} "
                    f"— confianza "
                    f"{conocimiento.get('confianza', 0):.0%}"
                )

                st.write(
                    conocimiento[
                        "contenido"
                    ]
                )

        else:

            st.write(
                "No se encontraron conocimientos relacionados."
            )


        # ====================================================
        # PATRONES
        # ====================================================

        st.subheader(
            "🔁 PATRONES DETECTADOS"
        )

        patrones = resultado[
            "patrones"
        ]

        if patrones:

            for patron in patrones:

                st.write(
                    f"🔁 {patron['concepto']} "
                    f"— {patron['apariciones']} "
                    "apariciones"
                )

        else:

            st.write(
                "Todavía no hay patrones suficientes."
            )


        # ====================================================
        # RELACIONES
        # ====================================================

        st.subheader(
            "🔗 RELACIONES CREADAS"
        )

        relaciones = resultado[
            "relaciones"
        ]

        if relaciones:

            for relacion in relaciones:

                st.write(
                    f"🔗 {relacion['a']} "
                    f"↔ {relacion['b']}"
                )

        else:

            st.write(
                "No se crearon relaciones nuevas."
            )


        # ====================================================
        # CONTRADICCIONES
        # ====================================================

        st.subheader(
            "⚠️ CONTRADICCIONES"
        )

        contradicciones = resultado[
            "contradicciones"
        ]

        if contradicciones:

            st.warning(
                f"Se encontraron "
                f"{len(contradicciones)} "
                "posibles conflictos."
            )

            for conflicto in contradicciones:

                st.write(
                    "**Anterior:**"
                )

                st.write(
                    conflicto[
                        "anterior"
                    ]
                )

                st.write(
                    "**Nuevo:**"
                )

                st.write(
                    conflicto[
                        "nuevo"
                    ]
                )

        else:

            st.success(
                "No se detectaron "
                "conflictos directos."
            )


        # ====================================================
        # EVALUACIÓN
        # ====================================================

        st.subheader(
            "📊 AUTOEVALUACIÓN"
        )

        evaluacion = resultado[
            "evaluacion"
        ]

        q1, q2, q3, q4 = st.columns(4)


        with q1:

            st.metric(
                "Claridad",
                f"{evaluacion['claridad']:.2f}"
            )


        with q2:

            st.metric(
                "Coherencia",
                f"{evaluacion['coherencia']:.2f}"
            )


        with q3:

            st.metric(
                "Utilidad",
                f"{evaluacion['utilidad']:.2f}"
            )


        with q4:

            st.metric(
                "Confianza",
                f"{evaluacion['confianza']:.2f}"
            )


        if resultado[
            "guardado"
        ]:

            st.success(
                "💾 Memoria persistente actualizada."
            )

        else:

            st.error(
                "No se pudo guardar la memoria."
            )


# ============================================================
# MEMORIA
# ============================================================

st.divider()

st.header(
    "📚 MEMORIA"
)


if cerebro.experiencias:

    for experiencia in reversed(
        cerebro.experiencias[-10:]
    ):

        with st.expander(
            f"🧠 EXPERIENCIA #{experiencia['id']} "
            f"| CICLO {experiencia['ciclo']}"
        ):

            st.write(
                "**Entrada:**"
            )

            st.write(
                experiencia[
                    "entrada"
                ]
            )


            if experiencia[
                "respuesta"
            ]:

                st.write(
                    "**Respuesta:**"
                )

                st.write(
                    experiencia[
                        "respuesta"
                    ]
                )


            st.write(
                "**Conceptos:**"
            )

            st.write(
                ", ".join(
                    experiencia[
                        "conceptos"
                    ]
                )
            )


            st.write(
                "**Conclusión:**"
            )

            st.write(
                experiencia[
                    "conclusion"
                ]
            )


            st.json(
                experiencia[
                    "evaluacion"
                ]
            )

else:

    st.info(
        "Memoria vacía."
    )


# ============================================================
# CONOCIMIENTOS
# ============================================================

st.divider()

st.header(
    "📖 BASE DE CONOCIMIENTOS"
)


if cerebro.conocimientos:

    for conocimiento in reversed(
        cerebro.conocimientos[-15:]
    ):

        with st.expander(
            f"📖 #{conocimiento['id']} "
            f"| Confianza "
            f"{conocimiento.get('confianza', 0):.0%}"
        ):

            st.write(
                conocimiento[
                    "contenido"
                ]
            )

            st.write(
                "**Conceptos:** "
                + ", ".join(
                    conocimiento.get(
                        "conceptos",
                        []
                    )
                )
            )

            st.write(
                "**Confirmaciones:** "
                + str(
                    conocimiento.get(
                        "veces_confirmado",
                        1
                    )
                )
            )

else:

    st.info(
        "Todavía no hay conocimientos."
    )


# ============================================================
# RELACIONES
# ============================================================

st.divider()

st.header(
    "🔗 RED DE RELACIONES"
)


if cerebro.relaciones:

    for relacion in cerebro.relaciones[-20:]:

        st.write(
            f"**{relacion['a']}** "
            f"↔ "
            f"**{relacion['b']}** "
            f"| fuerza: "
            f"{relacion['fuerza']}"
        )

else:

    st.info(
        "Todavía no existen relaciones."
    )


# ============================================================
# PATRONES
# ============================================================

st.divider()

st.header(
    "🔁 PATRONES DEL CEREBRO"
)


if cerebro.patrones:

    for patron in sorted(
        cerebro.patrones,
        key=lambda x:
        x.get(
            "apariciones",
            0
        ),
        reverse=True
    )[:20]:

        st.write(
            f"🔁 **{patron['concepto']}** "
            f"— {patron['apariciones']} apariciones"
        )

else:

    st.info(
        "Todavía no hay patrones suficientes."
    )


# ============================================================
# ADMINISTRACIÓN
# ============================================================

st.divider()

with st.expander(
    "⚙️ ADMINISTRACIÓN"
):

    st.write(
        f"Versión: **{VERSION}**"
    )

    st.write(
        f"Archivo: **{MEMORIA_FILE}**"
    )

    st.warning(
        "Borrar memoria elimina experiencias, "
        "conocimientos, relaciones y patrones."
    )

    if st.button(
        "🗑️ BORRAR TODA LA MEMORIA"
    ):

        cerebro.borrar_memoria()

        st.success(
            "Memoria eliminada correctamente."
        )

        st.rerun()


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "🧠 CEREBRO OMEGA ∞ | "
    "MOTOR COGNITIVO V3 | "
    "MEMORIA ASOCIATIVA | "
    "APRENDIZAJE PERSISTENTE"
)
