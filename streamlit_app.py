import streamlit as st
import numpy as np
import io
import wave

st.set_page_config(
    page_title="CEREBRO RABINO PRO",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 CEREBRO RABINO PRO")
st.caption("🎤 AI MUSIC STUDIO — Rabino Rap")

# =========================
# FUNCIONES
# =========================

def generar_beat(bpm, tonalidad, duracion, intensidad):

    sr = 44100
    total = int(sr * duracion)
    audio = np.zeros(total, dtype=np.float32)

    notas = {
        "C": 261.63,
        "D": 293.66,
        "E": 329.63,
        "F": 349.23,
        "G": 392.00,
        "A": 440.00,
        "B": 493.88
    }

    freq = notas[tonalidad]
    beat = 60 / bpm

    # Melodía
    for tiempo in np.arange(0, duracion, beat):

        inicio = int(tiempo * sr)
        fin = min(
            inicio + int(beat * sr),
            total
        )

        t = np.arange(fin - inicio) / sr

        audio[inicio:fin] += (
            0.10 *
            np.sin(2 * np.pi * freq * t)
        )

    # Kick
    for tiempo in np.arange(0, duracion, beat * 2):

        inicio = int(tiempo * sr)
        fin = min(
            inicio + int(0.25 * sr),
            total
        )

        t = np.arange(fin - inicio) / sr

        kick = (
            0.7 *
            np.sin(2 * np.pi * 100 * t) *
            np.exp(-12 * t)
        )

        audio[inicio:fin] += kick

    # Snare
    for tiempo in np.arange(
        beat,
        duracion,
        beat * 2
    ):

        inicio = int(tiempo * sr)
        fin = min(
            inicio + int(0.15 * sr),
            total
        )

        ruido = np.random.normal(
            0,
            1,
            fin - inicio
        )

        envelope = np.exp(
            -25 *
            np.arange(fin - inicio)
            / sr
        )

        audio[inicio:fin] += (
            ruido *
            envelope *
            0.18
        )

    # Hi-hat
    for tiempo in np.arange(
        0,
        duracion,
        beat / 2
    ):

        inicio = int(tiempo * sr)
        fin = min(
            inicio + int(0.05 * sr),
            total
        )

        ruido = np.random.normal(
            0,
            1,
            fin - inicio
        )

        envelope = np.exp(
            -60 *
            np.arange(fin - inicio)
            / sr
        )

        audio[inicio:fin] += (
            ruido *
            envelope *
            0.07
        )

    # Intensidad
    audio *= intensidad / 7

    # Normalizar
    maximo = np.max(np.abs(audio))

    if maximo > 0:
        audio = audio / maximo * 0.90

    audio = (
        audio * 32767
    ).astype(np.int16)

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as archivo:

        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(sr)

        archivo.writeframes(
            audio.tobytes()
        )

    return buffer.getvalue()


def generar_letra(tema, genero):

    return f"""🎵 {tema.upper()}

[INTRO]
Yeah...
Rabino Rap...

[VERSO 1]
Camino con propósito,
mantengo la visión,
cada palabra lleva
fuego en el corazón.

[CORO]
No voy a detenerme,
voy a seguir adelante,
mi voz lleva un mensaje,
mi sueño está gigante.

[VERSO 2]
Sube el ritmo,
sube la energía,
cada barra representa
una nueva melodía.

[OUTRO]
Rabino Rap.
CEREBRO RABINO PRO.
"""


# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "✍️ LETRAS",
    "🥁 BEATS",
    "🎤 VOCES",
    "🎚️ ESTUDIO",
    "🎨 PORTADAS"
])


# =========================
# LETRAS
# =========================

with tab1:

    st.header("✍️ GENERADOR DE LETRAS")

    tema = st.text_input(
        "Tema",
        "Dios me levantó"
    )

    genero = st.selectbox(
        "Género",
        [
            "Rap",
            "Trap",
            "Dembow",
            "Hip-Hop",
            "Reggaetón",
            "Worship"
        ]
    )

    if st.button(
        "🧠 GENERAR LETRA",
        use_container_width=True
    ):

        letra = generar_letra(
            tema,
            genero
        )

        st.text_area(
            "LETRA GENERADA",
            letra,
            height=400
        )


# =========================
# BEATS
# =========================

with tab2:

    st.header("🥁 GENERADOR DE BEATS")

    col1, col2, col3 = st.columns(3)

    with col1:

        genero_beat = st.selectbox(
            "Estilo",
            [
                "Dembow",
                "Trap",
                "Hip-Hop",
                "Reggaetón",
                "Boom Bap",
                "Drill",
                "Afrobeat",
                "Worship"
            ]
        )

    with col2:

        bpm = st.slider(
            "BPM",
            60,
            180,
            100
        )

    with col3:

        tonalidad = st.selectbox(
            "Tonalidad",
            [
                "C",
                "D",
                "E",
                "F",
                "G",
                "A",
                "B"
            ]
        )

    duracion = st.slider(
        "Duración",
        10,
        60,
        30
    )

    intensidad = st.slider(
        "🔥 Intensidad",
        1,
        10,
        7
    )

    if st.button(
        "🔥 GENERAR BEAT",
        use_container_width=True
    ):

        beat = generar_beat(
            bpm,
            tonalidad,
            duracion,
            intensidad
        )

        st.success(
            f"Beat listo — {genero_beat} — {bpm} BPM"
        )

        st.audio(
            beat,
            format="audio/wav"
        )

        st.download_button(
            "⬇️ DESCARGAR WAV",
            beat,
            file_name="rabino_rap_beat.wav",
            mime="audio/wav",
            use_container_width=True
        )


# =========================
# VOCES
# =========================

with tab3:

    st.header("🎤 VOCES IA")

    st.info(
        "Módulo preparado para conectar un motor de voz IA."
    )

    st.selectbox(
        "Tipo de voz",
        [
            "Rap",
            "Melódica",
            "Masculina",
            "Femenina",
            "Coro"
        ]
    )

    st.button(
        "🎤 GENERAR VOZ",
        use_container_width=True
    )


# =========================
# ESTUDIO
# =========================

with tab4:

    st.header("🎚️ ESTUDIO")

    st.slider("🔊 Volumen", 0.0, 1.0, 0.8)
    st.slider("🎛️ EQ", -10.0, 10.0, 0.0)
    st.slider("🌊 Reverb", 0.0, 1.0, 0.2)
    st.slider("⏱️ Delay", 0.0, 1.0, 0.1)

    st.info(
        "Mezcla y mastering avanzado se conectarán aquí."
    )


# =========================
# PORTADAS
# =========================

with tab5:

    st.header("🎨 PORTADAS")

    titulo = st.text_input(
        "Título de la canción"
    )

    artista = st.text_input(
        "Artista",
        "Rabino Rap"
    )

    concepto = st.text_area(
        "Describe la portada"
    )

    st.info(
        "Generador de imágenes listo para conectar."
    )

    st.write(
        f"🎵 {titulo} — 🎤 {artista}"
    )

st.divider()

st.success(
    "🧠 CEREBRO RABINO PRO está ENCENDIDO."
        )
