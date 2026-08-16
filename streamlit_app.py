import streamlit as st

st.set_page_config(page_title="CEREBRO RABINO PRO v2.0", layout="wide")
st.title("🧠 CEREBRO RABINO PRO v2.0")
st.caption("Tu Centro de Mando de Todas las IAs Musicales Gratis")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["✍️ LETRAS", "🎨 PORTADAS", "🎰 PANEL DE IAS", "📦 EXPORTAR", "🎚️ MIX"])

with tab1:
    st.header("Generador de Letras + Prompts")
    tema = st.text_input("Tema de la canción", "Dios me levantó del lodo")
    bpm = st.slider("BPM", 60, 160, 72)
    estilo = st.multiselect("Instrumentos", ["Piano", "Coro Gospel", "Strings", "808", "Kick", "Guitarra"])

    if st.button("🧠 GENERAR PROMPTS"):
        prompt_estilo = f"[Worship] Worship. {bpm} BPM. Instrumentos: {', '.join(estilo)}. Vocal: Voz Masculina Profunda en Español."
        prompt_letra = f"[Verse 1]\nEstaba en el lodo...\n[Chorus]\nDios me levantó del lodo"

        st.text_area("1. PROMPT DE ESTILO - Pega en SUNO/UDIO", prompt_estilo, height=100)
        st.text_area("2. LETRA COMPLETA", prompt_letra, height=200)

with tab5:
    st.header("Panel de Créditos Gratis")
    st.info("Marca aquí cuántos usaste hoy. Se recargan cada 24h")
    st.metric("SUNO", "0/5 usados")
    st.metric("UDIO", "0/10 usados")

with tab3: # ESTA ES LA NUEVA
    st.header("🎰 ABRE TODAS LAS IAS DESDE AQUÍ")
    st.write("1 Click y te lleva directo. Luego solo pegas el prompt de arriba")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("PA' CANCIONES CON VOZ")
        st.link_button("🎵 1. ABRIR SUNO", "https://suno.com/create")
        st.caption("5 créditos gratis cada día")
        st.link_button("🔥 2. ABRIR UDIO", "https://udio.com/create")
        st.caption("10 créditos gratis cada día")

    with col2:
        st.subheader("PA' INSTRUMENTALES")
        st.link_button("🥁 3. ABRIR BEATOVEN", "https://beatoven.ai")
        st.caption("Ilimitado - Solo música")
        st.link_button("🎹 4. ABRIR AIVA", "https://www.aiva.ai")
        st.caption("3/mes - Orquesta/Worship")

    st.divider()
    st.subheader("PA' SUBIR A SPOTIFY")
    st.link_button("📀 5. ABRIR BOOMY", "https://boomy.com")
    st.caption("Distribución gratis ilimitada")

    st.subheader("PA' PORTADAS")
    st.link_button("🎨 6. ABRIR BING IMAGE CREATOR", "https://www.bing.com/images/create")
    st.caption("Ilimitado con cuenta Microsoft")

with tab2:
    st.header("Generador de Portadas")
with tab4:
    st.header("Exportador de Canciones")
