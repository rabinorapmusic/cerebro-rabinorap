import streamlit as st
import json
import os
from datetime import datetime


# ============================================================
# CEREBRO OMEGA ∞
# SUPRACONSCIENCIA V1
# TODO EN UN SOLO ARCHIVO
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide"
)


ARCHIVO_EXPERIENCIAS = "experiencias_supraconsciencia.json"


# ============================================================
# SUPRACONSCIENCIA OMEGA
# ============================================================

class SupraconscienciaOmega:

    def __init__(self):
        self.estado = "ACTIVA"
        self.ciclos = 0
        self.experiencias = self._cargar_experiencias()

    # --------------------------------------------------------
    # CARGAR MEMORIA
    # --------------------------------------------------------

    def _cargar_experiencias(self):

        if not os.path.exists(ARCHIVO_EXPERIENCIAS):
            return []

        try:

            with open(
                ARCHIVO_EXPERIENCIAS,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

                if isinstance(datos, list):
                    return datos

                return []

        except Exception:
            return []

    # --------------------------------------------------------
    # GUARDAR MEMORIA
    # --------------------------------------------------------

    def _guardar_experiencias(self):

        try:

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

            return True

        except Exception:
            return False

    # --------------------------------------------------------
    # OBSERVAR
    # --------------------------------------------------------

    def observar(self, entrada, respuesta=None):

        return {
            "fecha": datetime.now().isoformat(),
            "entrada": str(entrada),
            "respuesta": (
                str(respuesta)
                if respuesta
                else ""
            )
        }

    # --------------------------------------------------------
    # EVALUAR
    # --------------------------------------------------------

    def evaluar(self, entrada, respuesta=None):

        claridad = 0.5
        coherencia = 0.5
        utilidad = 0.5

        if entrada and len(
            entrada.strip()
        ) > 3:

            claridad = 0.8

        if respuesta and len(
            respuesta.strip()
        ) > 3:

            coherencia = 0.8
            utilidad = 0.8

        confianza = (
            claridad
            + coherencia
            + utilidad
        ) / 3

        return {
            "claridad": round(
                claridad, 2
            ),
            "coherencia": round(
                coherencia, 2
            ),
            "utilidad": round(
                utilidad, 2
            ),
            "confianza": round(
                confianza, 2
            )
        }

    # --------------------------------------------------------
    # APRENDER
    # --------------------------------------------------------

    def aprender(
        self,
        observacion,
        evaluacion
    ):

        experiencia = {

            "id": (
                len(self.experiencias) + 1
            ),

            "fecha": datetime.now().isoformat(),

            "observacion": observacion,

            "evaluacion": evaluacion
        }

        self.experiencias.append(
            experiencia
        )

        guardado = (
            self._guardar_experiencias()
        )

        experiencia["guardado"] = guardado

        return experiencia

    # --------------------------------------------------------
    # CICLO DE SUPRACONSCIENCIA
    # --------------------------------------------------------

    def ciclo(
        self,
        entrada,
        respuesta=None
    ):

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

            "experiencia_guardada":
                experiencia["id"],

            "memoria_guardada":
                experiencia["guardado"]
        }

    # --------------------------------------------------------
    # ESTADO
    # --------------------------------------------------------

    def estado_actual(self):

        return {

            "estado": self.estado,

            "ciclos": self.ciclos,

            "experiencias":
                len(self.experiencias)
        }


# ============================================================
# INICIAR CEREBRO
# ============================================================

if "cerebro_omega" not in st.session_state:

    st.session_state.cerebro_omega = (
        SupraconscienciaOmega()
    )


cerebro = (
    st.session_state.cerebro_omega
)


# ============================================================
# INTERFAZ
# ============================================================

st.title("🧠 CEREBRO OMEGA ∞")

st.subheader(
    "SUPRACONSCIENCIA OMEGA"
)

st.write(
    "OBSERVAR → EVALUAR → APRENDER → RECORDAR → ∞"
)


# ============================================================
# ESTADO
# ============================================================

estado = cerebro.estado_actual()

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "ESTADO",
        estado["estado"]
    )


with col2:

    st.metric(
        "CICLOS",
        estado["ciclos"]
    )


with col3:

    st.metric(
        "EXPERIENCIAS",
        estado["experiencias"]
    )


st.divider()


# ============================================================
# CENTRO DE PENSAMIENTO
# ============================================================

st.header(
    "🧠 CENTRO DE PENSAMIENTO"
)


entrada = st.text_area(
    "Dale una orden o conocimiento "
    "a CEREBRO OMEGA:",
    placeholder=(
        "Ejemplo: ¿Qué significa aprender?"
    )
)


respuesta = st.text_area(
    "Respuesta para que la "
    "supraconciencia la evalúe:",
    placeholder=(
        "Escribe aquí una respuesta..."
    )
)


# ============================================================
# CICLO
# ============================================================

if st.button(
    "🧠 EJECUTAR SUPRACONSCIENCIA",
    use_container_width=True
):

    if not entrada.strip():

        st.warning(
            "Escribe primero una entrada."
        )

    else:

        resultado = cerebro.ciclo(
            entrada,
            respuesta
        )

        st.success(
            "♾️ Ciclo completado."
        )

        # ----------------------------------------------------
        # OBSERVACIÓN
        # ----------------------------------------------------

        st.subheader(
            "👁️ AUTOOBSERVACIÓN"
        )

        st.json(
            resultado["observacion"]
        )

        # ----------------------------------------------------
        # EVALUACIÓN
        # ----------------------------------------------------

        st.subheader(
            "📊 AUTOEVALUACIÓN"
        )

        evaluacion = (
            resultado["evaluacion"]
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Claridad",
                f"{evaluacion['claridad']:.2f}"
            )

        with c2:

            st.metric(
                "Coherencia",
                f"{evaluacion['coherencia']:.2f}"
            )

        with c3:

            st.metric(
                "Utilidad",
                f"{evaluacion['utilidad']:.2f}"
            )

        with c4:

            st.metric(
                "Confianza",
                f"{evaluacion['confianza']:.2f}"
            )

        # ----------------------------------------------------
        # APRENDIZAJE
        # ----------------------------------------------------

        st.subheader(
            "📚 APRENDIZAJE"
        )

        if resultado["memoria_guardada"]:

            st.success(
                "Experiencia guardada en memoria."
            )

        else:

            st.error(
                "No se pudo guardar la experiencia."
            )


# ============================================================
# MEMORIA
# ============================================================

st.divider()

st.header(
    "📚 MEMORIA DE LA SUPRACONSCIENCIA"
)


if cerebro.experiencias:

    for experiencia in reversed(
        cerebro.experiencias[-10:]
    ):

        numero = experiencia["id"]

        with st.expander(
            f"🧠 EXPERIENCIA #{numero}"
        ):

            observacion = (
                experiencia["observacion"]
            )

            evaluacion = (
                experiencia["evaluacion"]
            )

            st.write(
                "**Entrada:**"
            )

            st.write(
                observacion["entrada"]
            )

            if observacion["respuesta"]:

                st.write(
                    "**Respuesta:**"
                )

                st.write(
                    observacion["respuesta"]
                )

            st.write(
                "**Evaluación:**"
            )

            st.json(
                evaluacion
            )

else:

    st.info(
        "La supraconciencia todavía "
        "no tiene experiencias."
    )


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "🧠 CEREBRO OMEGA ∞ | "
    "SUPRACONSCIENCIA V1"
)
