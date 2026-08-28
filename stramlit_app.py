import streamlit as st
import json
import os
from datetime import datetime

# ============================================================
# CEREBRO OMEGA ∞
# STREAMLIT APP — TODO EN UN SOLO ARCHIVO
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="∞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# ARCHIVOS
# ============================================================

MEMORIA_FILE = "cerebro_memoria.json"
EXPERIENCIAS_FILE = "cerebro_experiencias.json"


# ============================================================
# FUNCIONES DE ARCHIVOS
# ============================================================

def cargar_json(archivo, defecto):
    try:
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return defecto


def guardar_json(archivo, datos):
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


# ============================================================
# MEMORIA
# ============================================================

if "memoria" not in st.session_state:
    st.session_state.memoria = cargar_json(MEMORIA_FILE, [])

if "experiencias" not in st.session_state:
    st.session_state.experiencias = cargar_json(EXPERIENCIAS_FILE, [])

if "ciclos" not in st.session_state:
    st.session_state.ciclos = 0

if "respuesta" not in st.session_state:
    st.session_state.respuesta = ""


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top, #111827 0%, #050505 45%, #000000 100%);
    color: #ffffff;
}

.block-container {
    max-width: 1250px;
    padding-top: 25px;
}

.omega-title {
    text-align: center;
    font-size: 64px;
    font-weight: 900;
    letter-spacing: 8px;
    margin-bottom: 0;
    text-shadow:
        0 0 10px #00ff88,
        0 0 25px #00ff88,
        0 0 50px #008844;
}

.omega-subtitle {
    text-align: center;
    color: #00ff88;
    font-size: 16px;
    letter-spacing: 5px;
    margin-bottom: 35px;
}

.panel {
    background: rgba(10, 15, 20, 0.90);
    border: 1px solid rgba(0, 255, 136, 0.30);
    border-radius: 18px;
    padding: 25px;
    box-shadow:
        0 0 25px rgba(0, 255, 136, 0.08),
        inset 0 0 25px rgba(0, 255, 136, 0.02);
    margin-bottom: 20px;
}

.status {
    text-align: center;
    color: #00ff88;
    font-weight: bold;
    letter-spacing: 2px;
}

.metric {
    text-align: center;
    padding: 18px;
    border-radius: 15px;
    background: rgba(0, 255, 136, 0.05);
    border: 1px solid rgba(0, 255, 136, 0.15);
}

.metric-number {
    font-size: 32px;
    font-weight: bold;
    color: #00ff88;
}

.metric-label {
    font-size: 12px;
    color: #aaa;
    letter-spacing: 2px;
}

.response {
    background: #050b08;
    border-left: 4px solid #00ff88;
    border-radius: 10px;
    padding: 20px;
    line-height: 1.7;
    white-space: pre-wrap;
}

.infinity {
    text-align: center;
    font-size: 100px;
    color: #00ff88;
    text-shadow:
        0 0 15px #00ff88,
        0 0 40px #00ff88;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CABECERA
# ============================================================

st.markdown(
    '<div class="omega-title">CEREBRO OMEGA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="omega-subtitle">SUPRACONSCIENCIA • SISTEMA EVOLUTIVO</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="infinity">∞</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status">● SISTEMA ACTIVO</div>',
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# ESTADÍSTICAS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-number">{len(st.session_state.memoria)}</div>
        <div class="metric-label">CONOCIMIENTO</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-number">{len(st.session_state.experiencias)}</div>
        <div class="metric-label">EXPERIENCIAS</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric">
        <div class="metric-number">{st.session_state.ciclos}</div>
        <div class="metric-label">CICLOS ∞</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric">
        <div class="metric-number">∞</div>
        <div class="metric-label">EVOLUCIÓN</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# CEREBRO
# ============================================================

st.markdown('<div class="panel">', unsafe_allow_html=True)

st.subheader("🧠 Entrada al CEREBRO")

entrada = st.text_area(
    "Escribe una pregunta, idea, conocimiento o instrucción:",
    height=130,
    placeholder="Ejemplo: ¿Qué es el hip hop?"
)

col_a, col_b = st.columns(2)

with col_a:
    procesar = st.button(
        "⚡ PROCESAR",
        use_container_width=True
    )

with col_b:
    evolucionar = st.button(
        "∞ EVOLUCIONAR",
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# MOTOR DE RESPUESTA
# ============================================================

def buscar_conocimiento(texto):

    texto_lower = texto.lower()

    coincidencias = []

    for item in st.session_state.memoria:

        concepto = item.get("concepto", "").lower()
        conocimiento = item.get("conocimiento", "")

        if concepto and (
            concepto in texto_lower or
            texto_lower in concepto
        ):
            coincidencias.append(
                conocimiento
            )

    return coincidencias


def generar_respuesta(texto):

    coincidencias = buscar_conocimiento(texto)

    if coincidencias:

        respuesta = (
            "🧠 CEREBRO OMEGA\n\n"
            "He encontrado conocimiento relacionado "
            "en mi memoria:\n\n"
        )

        for conocimiento in coincidencias[:5]:
            respuesta += f"• {conocimiento}\n"

        return respuesta

    texto_lower = texto.lower()

    if "hola" in texto_lower:
        return (
            "🧠 CEREBRO OMEGA ∞\n\n"
            "Sistema activo.\n"
            "Estoy preparado para recibir conocimiento."
        )

    if "hip
