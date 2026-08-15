with tab3:
    st.header("🎚️ BEAT MAKER — CONCEPTO PROFESIONAL")

    col1, col2 = st.columns(2)

    with col1:
        genero = st.selectbox(
            "Género",
            [
                "Rap",
                "Trap",
                "Dembow",
                "Hip-Hop",
                "Drill",
                "Worship Rap",
                "Boom Bap",
                "Reggaetón"
            ]
        )

        mood = st.selectbox(
            "Mood / Ambiente",
            [
                "Oscuro",
                "Motivador",
                "Espiritual",
                "Agresivo",
                "Melancólico",
                "Épico",
                "Romántico",
                "Triunfal"
            ]
        )

    with col2:
        bpm = st.slider("BPM", min_value=60, max_value=180, value=95)

        tonalidad = st.selectbox(
            "Tonalidad",
            [
                "C menor",
                "D menor",
                "E menor",
                "F menor",
                "G menor",
                "A menor",
                "B menor",
                "C mayor",
                "D mayor",
                "E mayor",
                "F mayor",
                "G mayor",
                "A mayor",
                "B mayor"
            ]
        )

    tema_beat = st.text_input(
        "¿De qué quieres que trate el beat?",
        placeholder="Ejemplo: batalla espiritual, barrio, superación..."
    )

    if st.button("🔥 CREAR CONCEPTO DEL BEAT"):
        prompt = f"""
Eres un productor musical profesional especializado en música urbana.

Crea un concepto profesional para un beat con estas características:

Género: {genero}
BPM: {bpm}
Tonalidad: {tonalidad}
Mood: {mood}
Tema: {tema_beat}

Entrega la respuesta con esta estructura:

1. NOMBRE DEL BEAT
2. CONCEPTO GENERAL
3. BATERÍA
   - Kick
   - Snare/Clap
   - Hi-hats
   - Percusión
4. BAJO / 808
5. MELODÍA PRINCIPAL
6. ACORDES
7. INSTRUMENTOS RECOMENDADOS
8. ESTRUCTURA
   - Intro
   - Verso
   - Coro
   - Puente
   - Outro
9. EFECTOS Y TEXTURAS
10. SONIDO FINAL / MASTERING
11. REFERENCIA DE ENERGÍA
12. PROMPT PARA GENERAR EL BEAT CON IA

Hazlo profesional, moderno y fácil de llevar a FL Studio, BandLab o Ableton.
"""

        with st.spinner("🎧 Diseñando el beat..."):
            response = model.generate_content(prompt)

        st.success("🔥 CONCEPTO CREADO")
        st.markdown(response.text)

        st.download_button(
            "📥 DESCARGAR CONCEPTO",
            response.text,
            file_name="concepto_beat_rabino.txt",
            mime="text/plain"
        )
