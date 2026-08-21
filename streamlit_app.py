import streamlit as st

from modules.supraconsciencia_omega import SupraconscienciaOmega


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# INICIAR SUPRACONSCIENCIA
# ============================================================

if "supraconsciencia" not in st.session_state:
    st.session_state.supraconsciencia = SupraconscienciaOmega()

cerebro = st.session_state.supraconsciencia


# ============================================================
# INTERFAZ
# ============================================================

st.title("🧠 CEREBRO OMEGA ∞")

st.subheader(
    "SUPRACONSCIENCIA OMEGA"
)

st.write(
    "OBSERVAR → EVALUAR → APRENDER → RECORDAR"
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

st.header("🧠 Centro de Pensamiento")

entrada = st.text_area(
    "Dale una orden o conocimiento a CEREBRO OMEGA:",
    placeholder="Ejemplo: ¿Qué significa aprender?"
)


respuesta = st.text_area(
    "Respuesta de CEREBRO:",
    placeholder="Escribe aquí la respuesta que quieres que evalúe."
)


# ============================================================
# EJECUTAR CICLO
# ============================================================

if st.button(
    "🧠 EJECUTAR CICLO DE SUPRACONSCIENCIA",
    use_container_width=True
):

    if not entrada.strip():
        st.warning("Escribe primero una entrada.")
    else:

        resultado = cerebro.ciclo(
            entrada,
            respuesta
        )

        st.success("Ciclo completado correctamente.")

        st.subheader("👁️ Observación")

        st.json(
            resultado["observacion"]
        )

        st.subheader("📊 Evaluación")

        evaluacion = resultado["evaluacion"]

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

        st.subheader("💾 Memoria")

        st.info(
            f"Experiencia #{resultado['experiencia_guardada']} "
            "guardada correctamente."
        )


# ============================================================
# EXPERIENCIAS
# ============================================================

st.divider()

st.header("📚 Experiencias de la Supraconciencia")

if cerebro.experiencias:

    for experiencia in reversed(
        cerebro.experiencias[-10:]
    ):

        with st.expander(
            f"Experiencia #{experiencia['id']}"
        ):

            st.write(
                "**Entrada:**",
                experiencia["observacion"]["entrada"]
            )

            st.write(
                "**Respuesta:**",
                experiencia["observacion"]["respuesta"]
            )

            st.json(
                experiencia["evaluacion"]
            )

else:

    st.info(
        "La supraconciencia todavía no tiene experiencias."
    )


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "🧠 CEREBRO OMEGA ∞ — SUPRACONSCIENCIA V1"
)
