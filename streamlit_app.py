import streamlit as st

st.title("🧠 CEREBRO RABINO PRO - SUNO MASTER")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎵 SUNO MASTER", "✍️ LETRAS", "🎨 PORTADAS", "📦 EXPORTAR", "🎚️ MIX"])

with tab1:
    st.header("🎵 GENERADOR DE PROMPTS PARA SUNO - 100% COMPLETO")
    st.caption("Llena todos los campos y CEREBRO te da el prompt perfecto")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1. BASE")
        tema = st.text_input("Tema/Lyric Idea", "Dios me levantó del lodo")
        genero = st.selectbox("Género Principal", ["Rap Cristiano", "Trap Cristiano", "Worship", "Dembow Gospel", "Afrobeats Gospel", "Rock Cristiano"])
        subgenero = st.text_input("Sub-género / Vibe", "Boom Bap, 90s, con piano")
        
    with col2:
        st.subheader("2. SONIDO")
        bpm = st.slider("BPM", 60, 180, 107)
        tonalidad = st.selectbox("Tonalidad", ["C", "D", "E", "F", "G", "A", "B"])
        instrumentos = st.multiselect("Instrumentos", 
            ["808", "Kick", "Snare", "Hi-Hats", "Piano", "Guitarra", "Bajo", "Strings", "Synth", "Coro Gospel", "Pad"],
            ["808", "Kick", "Piano", "Coro Gospel"])
        voz = st.selectbox("Voz", ["Voz Masculina Profunda", "Voz Masculina Aguda", "Voz Femenina", "Dueto", "Coro"])
        
    with col3:
        st.subheader("3. ESTRUCTURA Y MEZCLA")
        estructura = st.selectbox("Estructura", ["Intro-Verse-Chorus-Verse-Chorus-Bridge-Outro", "Intro-Chorus-Verse-Chorus-Outro"])
        mezcla = st.selectbox("Calidad de Mezcla", ["Radio Ready", "Profesional", "Lo-fi", "Épico", "Íntimo"])
        idioma = st.selectbox("Idioma", ["Español", "Español + Inglés"])
    
    letra_guia = st.text_area("Letra guía o palabras clave", "superación, fe, no me rindo, Dios conmigo")
    
    if st.button("🧠 CEREBRO: GENERAR PROMPT COMPLETO", use_container_width=True, type="primary"):
        
        # PROMPT PRINCIPAL PARA SUNO
        prompt_principal = f"""[{genero}] {subgenero}. {bpm} BPM, Key of {tonalidad}.
Instrumentos: {', '.join(instrumentos)}.
Vocal: {voz} singing in {idioma}.
Style: {mezcla} mix, professional production, radio ready, clear vocals.
Theme: {tema}. Keywords: {letra_guia}.
Structure: {estructura}."""

        # PROMPT DE LETRA PARA SUNO
        prompt_letra = f"""[Verse 1]
Sobre {tema}
{letra_guia}

[Chorus]
Coro pegajoso sobre {tema}

[Verse 2]
Segunda parte con más profundidad

[Bridge]
Puente emocional

[Outro]
Final glorioso"""

        st.success("✅ PROMPT LISTO. COPIA Y PEGA EN SUNO.COM")
        
        st.markdown("### **1. PROMPT DE ESTILO - Pégalo en 'Style of Music'**")
        st.code(prompt_principal, language="text")
        
        st.markdown("### **2. PROMPT DE LETRA - Pégalo en 'Lyrics'**")
        st.code(prompt_letra, language="text")
        
        st.link_button("🚀 ABRIR SUNO.COM", "https://suno.com/create", use_container_width=True)
        
        st.info("💡 **PRO TIP**: En Suno activa 'Custom Mode'. Pega Estilo arriba y Letra abajo. Desactiva 'Instrumental' si quieres voz.")

with tab2:
    st.header("✍️ GENERADOR DE LETRAS")
    st.write("Aquí luego conectamos Gemini pa' que CEREBRO escriba la letra completa")

with tab3:
    st.header("🎨 GENERADOR DE PORTADAS")
    st.write("Aquí luego conectamos IA pa' portadas")

with tab4:
    st.header("📦 EXPORTAR")
    st.file_uploader("Sube tu MP3 de Suno aquí", type=["mp3", "wav"])

with tab5:
    st.header("🎚️ GUARDAR PRESETS")
    st.write("Guarda tus combinaciones favoritas de beats")
