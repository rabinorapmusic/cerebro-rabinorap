import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="CEREBRO OMEGA", page_icon="🧠")

ARCHIVO = "memoria.json"

def cargar():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar(mem):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(mem, f, ensure_ascii=False, indent=2)

if "mem" not in st.session_state:
    st.session_state.mem = cargar()

def bible(tema):
    try:
        r = requests.get(f"https://bible-api.com/?q={tema}&translation=rvr1960", timeout=3).json()
        return f"📖 {r['reference']}: {r['text'][:250]}"
    except:
        return ""

def knowledge(tema):
    for k in st.session_state.mem:
        if k in tema.lower():
            return f"🧠 {st.session_state.mem[k]}"
    return f"🧠 Analizando: {tema}"

def hablar(texto):
    js = f"""
    <script>
    function hablar() {{
        speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance(`{texto.replace('`','')}`);
        msg.lang = 'es-MX';
        msg.rate = 0.85;
        msg.pitch = 0.6;
        speechSynthesis.speak(msg);
    }}
    hablar();
    </script>
    <button onclick="hablar()">🔊 REPETIR</button>
    """
    st.components.v1.html(js, height=50)

st.title("🧠 CEREBRO OMEGA")

orden = st.text_area("ORDEN", height=100)

col1, col2 = st.columns(2)
with col1:
    if st.button("EJECUTAR", use_container_width=True):
        b = bible(orden)
        k = knowledge(orden)
        res = f"{b}\n\n{k}"
        st.session_state.res = res
with col2:
    palabra = st.text_input("ENSEÑAR")
    if st.button("GUARDAR", use_container_width=True) and palabra:
        st.session_state.mem[palabra.lower()] = orden
        guardar(st.session_state.mem)

if "res" in st.session_state:
    st.text(st.session_state.res)
    hablar(st.session_state.res)
