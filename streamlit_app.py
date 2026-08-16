import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="CEREBRO RABINO PRO v4.0", layout="wide", page_icon="🧠")
st.title("🧠 CEREBRO RABINO PRO v4.0 OMNI")
st.caption("Todo lo que Streamlit puede hacer. Gratis para siempre.")

# SIDEBAR - TODO EN 1 LUGAR
with st.sidebar:
    st.image("https://placehold.co/200x200/000/FFD700?text=CEREBRO")
    st.metric("Canciones Hoy", "0/30")
    st.metric("Créditos Suno", "5/5")
    st.metric("Créditos Udio", "10/10")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "✍️ MODO LIBRE", "🎰 20 IAS", "📊 ESTADÍSTICAS", 
    "📦 EXPORTAR", "💾 MIS CANCIONES", "💬 CHAT IA", "💡 IDEAS"
])

with tab1:
    st.header("🧠 GENERADOR UNIVERSAL")
    col1, col2 = st.columns(2)
    with col1:
        tema = st.text_area("1. ¿DE QUÉ QUIERES CANTAR?", height=100)
        sentimiento = st.selectbox("2. SENTIMIENTO", ["Agradecido", "Dolorido", "Guerrero", "Victorioso"])
        genero = st.selectbox("3. GÉNERO", ["Worship", "Trap Cristiano", "Rap", "Balada", "Salsa"])
    with col2:
        bpm = st.slider("4. BPM", 60, 160, 90)
        voz = st.selectbox("5. VOZ", ["Masculina Profunda", "Femenina Dulce", "Coro Gospel"])
        estilo = st.multiselect("6. INSTRUMENTOS", ["Piano", "Coro", "Strings", "808", "Guitarra", "Bajo"])

    if st.button("🔥 GENERAR PROMPT UNIVERSAL", type="primary"):
        prompt = f"{genero} {bpm} BPM. {voz}. {sentimiento}. Tema: {tema}. Inst: {', '.join(estilo)}"
        st.text_area("TU PROMPT UNIVERSAL", prompt, height=200)
        st.download_button("📥 DESCARGAR PROMPT", prompt, file_name="prompt.txt")

with tab3:
    st.header("📊 TUS ESTADÍSTICAS")
    data = pd.DataFrame({
        'IA': ['Suno', 'Udio', 'Beatoven'],
        'Canciones': [3, 5, 2]
    })
    fig = px.bar(data, x='IA', y='Canciones', title="Canciones por IA")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🎰 PANEL DE 20 IAS GRATIS")
    cols = st.columns(4)
    ias = [
        ("SUNO", "https://suno.com"), ("UDIO", "https://udio.com"), ("BEATOVEN", "https://beatoven.ai"),
        ("AIVA", "https://aiva.ai"), ("SOUNDFUL", "https://soundful.com"), ("BOOMY", "https://boomy.com"),
        ("RIFFUSION", "https://riffusion.com"), ("MUSICGEN", "https://huggingface.co/facebook/MusicGen"),
        ("SOUNDRAW", "https://soundraw.io"), ("MELLODY", "https://mellody.ai"), ("AIMUSIC", "https://aimusic.so"),
        ("AMPER", "https://ampermusic.com"), ("BING IA", "https://bing.com/images/create"),
        ("LEONARDO", "https://leonardo.ai"), ("CANVA IA", "https://canva.com"), ("LANDR", "https://landr.com"),
        ("ELEVENLABS", "https://elevenlabs.io"), ("VOCALREMOVER", "https://vocalremover.org"),
        ("MOISES", "https://moises.ai"), ("MASTERINGBOX", "https://masteringbox.com")
    ]
    for i, (nombre, link) in enumerate(ias):
        cols[i%4].link_button(f"🎵 {nombre}", link)

with tab4:
    st.header("📦 EXPORTADOR PRO")
    uploaded_file = st.file_uploader("Sube tu MP3", type=['mp3'])
    if uploaded_file:
        st.audio(uploaded_file)
        st.text_input("Título de la canción")
        st.text_area("Descripción pa' YouTube")
        st.button("GENERAR TAGS Y PORTADA")

with tab5:
    st.header("💾 MIS CANCIONES GUARDADAS")
    st.info("Aquí se guardan todos tus prompts y links. Próximamente con login")

with tab6:
    st.header("💬 CHAT CON CEREBRO")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])
    if prompt := st.chat_input("Pregúntale a CEREBRO"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write(f"Te ayudo con: {prompt}")

with tab7:
    st.header("💡 BANCO DE IDEAS")
    idea = st.text_area("Tu idea mayor pa' CEREBRO")
    st.button("ENVIAR IDEA")
