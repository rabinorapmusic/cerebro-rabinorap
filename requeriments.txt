import streamlit as st
import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import tempfile
import os

st.set_page_config(page_title="CEREBRO RABINO CABINA PRO", page_icon="👑", layout="wide")

# ESTILO NEGRO + DORADO + MORADO
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #000, #1a0033); color: #FFD700;}
h1, h2, h3 {color: #FFD700!important; text-shadow: 0 0 10px #8A2BE2;}
.stButton>button {background: #8A2BE2; color: #FFD700; border-radius: 10px; font-weight: bold;}
.stTextInput>div>div>input {background: #1a1a1a; color: #FFD700; border: 2px solid #FFD700;}
</style>
""", unsafe_allow_html=True)

st.title("👑 CEREBRO RABINO CABINA PRO v12.0")
st.subheader("Tu estudio cristiano con IA")

tab1, tab2, tab3 = st.tabs(["📜 ESCRITOR PROFÉTICO", "🥁 FABRICA DE BEATS", "🎛️ MEZCLADOR FINAL"])

# PESTAÑA 1: LETRAS
with tab1:
    st.header("Escribe como los profetas")
    nombre = st.text_input("Nombre del Artista", "RabinoRap")
    tema = st.text_input("Tema Profético", "Victoria en Cristo")
    estilo = st.selectbox("Unción / Estilo", ["Rap Cristiano", "Drill Cristiano", "Adoración Trap"])
    
    if st.button("SOLTAR LA LETRA 🔥"):
        with st.spinner("El Espíritu está escribiendo..."):
            letra = f"""
[INTRO]
Yo soy {nombre}, con la unción de Dios
Tema: {tema} - Estilo: {estilo}

[VERSO 1]
Me levanto en fe porque Cristo es mi voz
Nada me detiene, camino con el Rey
{tema} es mi porción, lo declaro hoy
Su palabra es espada, corta toda ley

[HOOK]
{tema}, {tema}
En el nombre de Jesús yo venceré
{tema}, {tema} 
Su promesa nunca falla, lo veré

[VERSO 2]
Desde Los Alcarrizos hasta las naciones
Llevamos el mensaje con las nuevas generaciones
No es por fama, es por salvación
CEREBRO RABINO activado con unción

[BRIDGE]
Todo lo puedo en Cristo que me fortalece
Filipenses 4:13, su poder permanece
"""
            st.text_area("TU LETRA SANTA:", letra, height=400)
            st.download_button("DESCARGAR LETRA", letra, file_name=f"{nombre}_{tema}.txt")

# PESTAÑA 2: BEATS
with tab2:
    st.header("Genera beats originales con IA")
    beat_estilo = st.selectbox("Estilo del Beat", ["rap cristiano", "drill cristiano", "trap cristiano"])
    bpm = st.slider("BPM", 70, 150, 90)
    
    if st.button("GENERAR BEAT SANTO 🥁"):
        with st.spinner("Creando beat original... Tarda 2 min"):
            model = MusicGen.get_pretrained('facebook/musicgen-small')
            model.set_generation_params(duration=30)
            description = f"{beat_estilo} beat, {bpm} bpm, uplifting, no vocals, instrumental"
            wav = model.generate([description])
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                audio_write(tmp.name, wav[0].cpu(), model.sample_rate, format="wav")
                st.audio(tmp.name)
                with open(tmp.name, "rb") as f:
                    st.download_button("DESCARGAR BEAT", f, file_name=f"beat_{beat_estilo}.wav")

# PESTAÑA 3: MEZCLADOR
with tab3:
    st.header("Mezcla y Domina")
    st.info("""
    **PASOS PARA GRABAR:**
    1. Descarga tu beat de la pestaña 2
    2. Grábate en tu cel con BandLab o Voice Memos
    3. Próximamente: Clonador de Voz IA
    """)

st.markdown("---")
st.caption("CEREBRO RABINO © 2026 | Hecho para la gloria de Dios")
