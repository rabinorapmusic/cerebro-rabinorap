import streamlit as st
from core.nucleus import OmegaCore

st.set_page_config(
    page_title="CEREBRO OMEGA",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 CEREBRO OMEGA ♾️")
st.subheader("Generador y explorador de posibilidades")

st.divider()

objective = st.text_input(
    "🎯 ¿Qué quieres explorar?",
    placeholder="Escribe un objetivo..."
)

amount = st.slider(
    "♾️ Número de posibilidades",
    min_value=1,
    max_value=20,
    value=8
)

if st.button("⚡ GENERAR POSIBILIDADES"):

    if not objective.strip():
        st.warning("Escribe un objetivo primero.")
    else:
        try:
            omega = OmegaCore()

            results = omega.explore(
                objective,
                amount
            )

            st.success("🧠 OMEGA está explorando...")

            for i, result in enumerate(results, 1):

                st.write(
                    f"### {i}. ♾️ {result.idea}"
                )

                st.progress(
                    float(result.score)
                )

                st.caption(
                    f"Evaluación: {result.score:.2f}"
                )

        except Exception as error:

            st.error(
                f"⚠️ Error del sistema: {error}"
            )

st.divider()

st.caption(
    "☁️ CEREBRO OMEGA — Núcleo experimental"
)
