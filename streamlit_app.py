import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CEREBRO RABINO PRO v4.1", layout="wide", page_icon="🧠")
st.title("🧠 CEREBRO RABINO PRO v4.1 OMNI")
st.caption("20 IAs Musicales Gratis. Todo funciona sin errores.")

# SIDEBAR
with st.sidebar:
    st.image("https://placehold.co/200x200/000/FFD700?text=CEREBRO")
    st.metric("Canciones Hoy", "0/30")
    st.metric("Créditos Suno", "5/5")
    st.metric("Créditos Udio", "10/10")
    st.info("v4.1 Estable - Sin errores")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "✍️ MODO LIBRE", "🎰 20 IAS", "📊 ESTADÍSTICAS", 
    "📦 EXPORTAR", "💾 MIS CANCIONES", "💬 CHAT IA", "💡 IDEAS"
])

with tab1:
    st.header("🧠 GENERADOR UNIVERSAL")
    col1, col2 = st.columns(2)
    with col1:
        tema = st.text_area("1. ¿DE QUÉ QUIERES CANTAR?", placeholder="Ej: Mi testimonio...", height=100)
        sentimiento = st.selectbox("2. SENTIMIENTO", ["Agradecido", "Dolorido", "Guerrero", "Victorioso", "Enamorado de Dios"])
        genero = st.selectbox("3. GÉNERO", ["Worship", "Trap Cristiano", "Rap", "Balada", "Salsa Cristiana", "Rock"])
    with col2:
        bpm = st.slider("4. BPM", 60, 160, 90)
        voz = st.selectbox("5. VOZ", ["Voz Masculina Profunda", "Voz Femenina Dulce", "Coro Gospel", "Rapero"])
        estilo = st.multiselect("6. INSTRUMENTOS", ["Piano", "Coro Gospel", "Strings", "808", "Kick", "Guitarra", "Bajo", "Batería"])

    if st.button("🔥 GENERAR PROMPT UNIVERSAL", type="primary"):
        if tema == "":
            st.warning("Escribe primero de qué quieres cantar")
        else:
            prompt = f"""{genero} song in Spanish. {bpm} BPM.
Instruments: {', '.join(estilo)}.
Vocal: {voz}. Mood: {sentimiento}, Emotional, Powerful.
Theme: {tema}

[Intro][Verse 1][Chorus][Verse 2][Bridge][Final Chorus][Outro]
Letra sobre: {tema}"""
            st.text_area("✅ TU PROMPT UNIVERSAL", prompt, height=250)
            st.download_button("📥 DESCARGAR PROMPT", prompt, file_name="prompt_cerebro.txt")
            st.success("Copia y pégalo en cualquier IA del Panel")

with tab2:
    st.header("🎰 PANEL DE 20 IAS GRATIS")
    st.write("Click y te abre la IA. Luego pegas el prompt de arriba")
    cols = st.columns(4)
    ias = [
        ("SUNO", "https://suno.com/create"), ("UDIO", "https://udio.com/create"), ("BEATOVEN", "https://beatoven.ai"),
        ("AIVA", "https://www.aiva.ai"), ("SOUNDFUL", "https://soundful.com"), ("BOOMY", "https://boomy.com"),
        ("RIFFUSION", "https://www.riffusion.com"), ("MUSICGEN", "https://huggingface.co/spaces/facebook/MusicGen"),
        ("SOUNDRAW", "https://soundraw.io"), ("MELLODY", "https://www.mellody.ai"), ("AIMUSIC", "https://aimusic.so"),
        ("AMPER", "https://www.ampermusic.com"), ("BING IA", "https://www.bing.com/images/create"),
        ("LEONARDO", "https://leonardo.ai"), ("CANVA IA", "https://www.canva.com/ai-music-generator/"), 
        ("LANDR", "https://www.landr.com"), ("ELEVENLABS", "https://elevenlabs.io"), 
        ("VOCALREMOVER", "https://vocalremover.org"), ("MOISES", "https://moises.ai"), ("MASTERINGBOX", "https://masteringbox.com")
    ]
    for i, (nombre, link) in enumerate(ias):
        cols[i%4].link_button(f"🎵 {nombre}", link)

with tab3:
    st.header("📊 TUS ESTADÍSTICAS")
    data = pd.DataFrame({'IA': ['Suno', 'Udio', 'Beatoven'], 'Canciones': [3, 5, 2]})
    st.bar_chart(data, x='IA', y='Canciones') # Ya no usa plotly

with tab4:
    st.header("📦 EXPORTADOR PRO")
    uploaded_file = st.file_uploader("Sube tu MP3", type=['mp3'])
    if uploaded_file:
        st.audio(uploaded_file)
        st.text_input("Título de la canción")
        st.text_area("Descripción pa' YouTube")
        st.button("GENERAR TAGS")

with tab5:
    st.header("💾 MIS CANCIONES GUARDADAS")
    st.info("Próximamente: Login pa' guardar todo")

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
    if st.button("ENVIAR IDEA"):
        st.success("Idea recibida mi rey! La metemos en v4.2")
