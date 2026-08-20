import streamlit as st
from motor_omega import CerebroOmega

# ============================================================
# CEREBRO OMEGA ∞
# INTERFAZ
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# MATRIX INFINITY
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 50% 0%,
            rgba(0,255,136,.12),
            transparent 38%
        ),
        #010604;
    color:#eafff1;
}

header,
footer,
#MainMenu {
    visibility:hidden;
}

.omega {
    text-align:center;
    font-family:monospace;
    font-size:42px;
    font-weight:bold;
    letter-spacing:5px;
}

.infinity {
    color:#00ff88;
    font-size:78px;
    text-shadow:
        0 0 8px #00ff88,
        0 0 20px #00ff88,
        0 0 45px #00ff88,
        0 0 80px #00ff88;
}

.line {
    height:1px;
    margin:22px 0;
    background:linear-gradient(
        90deg,
        transparent,
        #00ff88,
        transparent
    );
}

.panel {
    background:rgba(0,20,10,.75);
    border:1px solid rgba(0,255,136,.3);
    border-radius:15px;
    padding:22px;
    box-shadow:
        inset 0 0 30px rgba(0,255,136,.03),
        0 0 20px rgba(0,255,136,.04);
}

.stButton>button {
    background:#002b16 !important;
    color:#00ff88 !important;
    border:1px solid #00ff88 !important;
    border-radius:10px !important;
    font-family:monospace !important;
    font-weight:bold !important;
}

.stButton>button:hover {
    background:#00ff88 !important;
    color:#001207 !important;
    box-shadow:0 0 30px #00ff88;
}

textarea {
    background:#010b05 !important;
    color:#dffff0 !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# CEREBRO
# ============================================================

try:

    cerebro = CerebroOmega()

except Exception as error:

    st.error(
        "CEREBRO OMEGA no pudo iniciar."
    )

    st.code(str(error))

    st.stop()

# ============================================================
# IDENTIDAD
# ============================================================

st.markdown("""
<div class="omega">
    🧠 CEREBRO OMEGA
    <span class="infinity">∞</span>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

# ============================================================
# ESTADO
# ============================================================

estado = cerebro.estado()

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "ESTADO",
        "🟢 ACTIVO"
    )

with col2:

    st.metric(
        "CONOCIMIENTO",
        estado["conocimiento"]
    )

with col3:

    st.metric(
        "EXPERIENCIAS",
        estado["experiencias"]
    )

with col4:

    st.metric(
        "CICLOS ∞",
        estado["ciclos"]
    )

# ============================================================
# CENTRO DE PENSAMIENTO
# ============================================================

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

st.subheader(
    "🧠 CENTRO DE PENSAMIENTO"
)

mision = st.text_area(
    "Dale una orden a CEREBRO OMEGA:",
    height=160,
    placeholder=(
        "Escribe una misión para CEREBRO OMEGA..."
    )
)

ejecutar = st.button(
    "⚡ EJECUTAR CICLO",
    use_container_width=True
)

# ============================================================
# EJECUCIÓN
# ============================================================

if ejecutar:

    if not mision.strip():

        st.warning(
            "CEREBRO OMEGA necesita una misión."
        )

    else:

        with st.spinner(
            "CEREBRO OMEGA ∞ procesando..."
        ):

            resultado = cerebro.ejecutar(
                mision
            )

        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        if not resultado.get("ok"):

            st.error(
                resultado.get(
                    "error",
                    "Error desconocido."
                )
            )

            if resultado.get(
                "memoria_encontrada"
            ):

                st.markdown(
                    '<div class="panel">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    "### 💾 Memoria relacionada"
                )

                for recuerdo in resultado[
                    "memoria_encontrada"
                ]:

                    st.write(
                        "• "
                        + recuerdo["contenido"]
                    )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        else:

            st.markdown(
                '<div class="panel">',
                unsafe_allow_html=True
            )

            st.markdown(
                "## 🧠 CEREBRO OMEGA ∞"
            )

            st.markdown(
                resultado["resultado"]
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # PROCESO
            # ------------------------------------------------

            with st.expander(
                "VER PROCESO DEL CICLO"
            ):

                st.markdown(
                    "### Análisis"
                )

                st.write(
                    resultado["analisis"]
                )

                st.markdown(
                    "### Razonamiento"
                )

                st.write(
                    resultado["razonamiento"]
                )

                st.markdown(
                    "### Crítica"
                )

                st.write(
                    resultado["critica"]
                )

                st.markdown(
                    "### Síntesis"
                )

                st.write(
                    resultado["sintesis"]
                )

                st.caption(
                    "Proveedor: "
                    + resultado["proveedor"]
                )

# ============================================================
# MEMORIA
# ============================================================

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

st.subheader(
    "💾 MEMORIA"
)

memoria = cerebro.memoria.todos()

if memoria:

    for recuerdo in reversed(
        memoria[-10:]
    ):

        st.write(
            "• "
            + recuerdo["contenido"]
        )

else:

    st.write(
        "La memoria está vacía."
    )

# ============================================================
# EXPERIENCIAS
# ============================================================

st.subheader(
    "🧬 EXPERIENCIAS"
)

experiencias = (
    cerebro.experiencias.todas()
)

if experiencias:

    for experiencia in reversed(
        experiencias[-5:]
    ):

        with st.expander(
            "CICLO "
            + str(
                experiencia["ciclo"]
            )
        ):

            st.write(
                experiencia["mision"]
            )

            st.write(
                experiencia["resultado"]
            )

else:

    st.write(
        "Todavía no hay experiencias."
    )

# ============================================================
# FINAL
# ============================================================

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

st.markdown("""
<div style="
text-align:center;
font-family:monospace;
font-size:24px;
">
CEREBRO OMEGA
<span style="
color:#00ff88;
font-size:60px;
text-shadow:
0 0 10px #00ff88,
0 0 30px #00ff88,
0 0 60px #00ff88;
">∞</span>
</div>
""", unsafe_allow_html=True)
