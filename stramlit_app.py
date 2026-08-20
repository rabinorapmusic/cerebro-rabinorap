import streamlit as st
import json
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="CEREBRO OMEGA ∞", page_icon="🧠", layout="wide")

MEMORIA_FILE = "memoria.json"
EXPERIENCIAS_FILE = "experiencias.json"

# --- FUNCIONES PARA GUARDAR/CARGAR ---
def cargar_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# Cargar estado
if "memoria" not in st.session_state:
    st.session_state.memoria = cargar_datos(MEMORIA_FILE)
if "experiencias" not in st.session_state:
    st.session_state.experiencias = cargar_datos(EXPERIENCIAS_FILE)
if "ciclos" not in st.session_state:
    st.session_state.ciclos = len(st.session_state.experiencias)

# --- ESTILOS VERDES NEON ---
st.markdown("""
<style>
    .stApp { background-color: #000; color: #FFFFFF; }
    .neon-green { color: #00FF88; font-weight: bold; }
    .box { background-color: #0A1F0A; padding: 15px; border-radius: 10px; border: 1px solid #00FF88; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🧠 CEREBRO OMEGA ∞")
st.markdown("**APRENDER → RECORDAR → RAZONAR → EVOLUCIONAR → ∞**")
st.markdown("Liderazgo central del sistema.")

col1, col2, col3 = st.columns(3)
col1.metric("ESTADO", "ACTIVO 🟢")
col2.metric("CONOCIMIENTO", len(st.session_state.memoria))
col3.metric("CICLOS ∞", st.session_state.ciclos)

st.divider()

# --- CENTRO DE PENSAMIENTO ---
st.header("🧠 CENTRO DE PENSAMIENTO")
st.write("Dale una orden a CEREBRO OMEGA:")

orden = st.text_area("Escribe una misión para CEREBRO OMEGA...", height=150, label_visibility="collapsed")

if st.button("⚡ EJECUTAR CICLO", use_container_width=True, type="primary"):
    if orden.strip() != "":
        # APRENDER: guardar en memoria
        nuevo_conocimiento = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "contenido": orden
        }
        st.session_state.memoria.append(nuevo_conocimiento)
        
        # EXPERIENCIA: registrar el ciclo
        nueva_experiencia = {
            "ciclo": st.session_state.ciclos + 1,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "orden": orden,
            "resultado": f"CEREBRO OMEGA procesó: '{orden}'. Conocimiento integrado."
        }
        st.session_state.experiencias.append(nueva_experiencia)
        st.session_state.ciclos += 1
        
        # Guardar en archivos
        guardar_datos(MEMORIA_FILE, st.session_state.memoria)
        guardar_datos(EXPERIENCIAS_FILE, st.session_state.experiencias)
        
        st.success("✅ Ciclo ejecutado. Conocimiento guardado en la memoria.")
        st.rerun()
    else:
        st.warning("Escribe una orden primero.")

st.divider()

# --- MEMORIA ---
st.header("💾 MEMORIA")
if len(st.session_state.memoria) == 0:
    st.info("La memoria está vacía.")
else:
    for item in reversed(st.session_state.memoria[-5:]): # muestra las últimas 5
        st.markdown(f"<div class='box'><b>{item['fecha']}</b><br>{item['contenido']}</div>", unsafe_allow_html=True)

st.divider()

# --- EXPERIENCIAS ---
st.header("🧬 EXPERIENCIAS")
if len(st.session_state.experiencias) == 0:
    st.info("Todavía no hay experiencias.")
else:
    for exp in reversed(st.session_state.experiencias):
        st.markdown(f"<div class='box'><b>Ciclo {exp['ciclo']} - {exp['fecha']}</b><br><b>Orden:</b> {exp['orden']}<br><b>Resultado:</b> {exp['resultado']}</div>", unsafe_allow_html=True)

st.divider()
st.markdown("<h2 style='text-align: center;'>CEREBRO OMEGA <span class='neon-green'>∞</span></h2>", unsafe_allow_html=True)
st.caption("CEREBRO OMEGA ∞ | LIDERAZGO 1.0")
