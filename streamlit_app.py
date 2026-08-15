import streamlit as st
import numpy as np
import io
import os
import json
import zipfile
import tempfile
from scipy.io import wavfile

# ============================================================
# CEREBRO RABINO PRO
# AI MUSIC STUDIO
# RABINO RAP
# ============================================================

st.set_page_config(
    page_title="CEREBRO RABINO PRO",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTADO
# ============================================================

DEFAULTS = {
    "letra": "",
    "beat": None,
    "drums": None,
    "bass": None,
    "melody": None,
    "project_name": "De Lodo a Corona",
    "last_prompt": ""
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 2px;
}

.subtitle {
    font-size: 18px;
    opacity: .75;
}

.metric-box {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,.12);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CABECERA
# ============================================================

st.markdown(
    '<div class="main-title">🧠 CEREBRO RABINO PRO</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">🎤 AI MUSIC STUDIO — RABINO RAP</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# API GEMINI
# ============================================================

def cargar_gemini():

    try:

        import google.generativeai as genai

        api_key = st.secrets.get(
            "GOOGLE_API_KEY",
            ""
        )

        if not api_key:
            return None

        genai.configure(
            api_key=api_key
        )

        return genai.GenerativeModel(
            "gemini-1.5-flash"
        )

    except Exception:
        return None


modelo = cargar_gemini()


# ============================================================
# UTILIDADES DE AUDIO
# ============================================================

SR = 44100


def normalizar(audio, peak=0.92):

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    maximo = np.max(
        np.abs(audio)
    )

    if maximo <= 0:
        return audio

    return (
        audio / maximo
    ) * peak


def convertir_wav(audio):

    audio = normalizar(audio)

    audio_int = (
        audio * 32767
    ).astype(np.int16)

    buffer = io.BytesIO()

    wavfile.write(
        buffer,
        SR,
        audio_int
    )

    return buffer.getvalue()


def guardar_wav(audio, path):

    audio = normalizar(audio)

    audio_int = (
        audio * 32767
    ).astype(np.int16)

    wavfile.write(
        path,
        SR,
        audio_int
    )


# ============================================================
# SINTETIZADORES
# ============================================================

def envelope(length, attack=0.005, release=0.15):

    t = np.arange(length) / SR

    env = np.ones(length)

    attack_samples = max(
        1,
        int(attack * SR)
    )

    release_samples = max(
        1,
        int(release * SR)
    )

    attack_samples = min(
        attack_samples,
        length
    )

    release_samples = min(
        release_samples,
        length
    )

    env[:attack_samples] = np.linspace(
        0,
        1,
        attack_samples
    )

    env[-release_samples:] *= np.linspace(
        1,
        0,
        release_samples
    )

    return env


def synth_kick(duration=.35):

    n = int(
        duration * SR
    )

    t = np.arange(n) / SR

    freq = (
        130 * np.exp(-18 * t)
        + 42
    )

    phase = 2 * np.pi * np.cumsum(freq) / SR

    body = np.sin(phase)

    click = (
        np.random.randn(n)
        * np.exp(-100 * t)
        * .15
    )

    return (
        body * np.exp(-10 * t)
        + click
    ) * .95


def synth_snare(duration=.22):

    n = int(
        duration * SR
    )

    t = np.arange(n) / SR

    noise = np.random.randn(n)

    noise *= np.exp(
        -22 * t
    )

    tone = (
        np.sin(
            2 * np.pi * 190 * t
        )
        * np.exp(-18 * t)
    )

    return (
        noise * .55
        + tone * .30
    )


def synth_hat(duration=.06):

    n = int(
        duration * SR
    )

    t = np.arange(n) / SR

    noise = np.random.randn(n)

    high = noise * np.exp(
        -65 * t
    )

    return high * .20


def synth_bass(freq, duration):

    n = int(
        duration * SR
    )

    t = np.arange(n) / SR

    fundamental = np.sin(
        2 * np.pi * freq * t
    )

    harmonic = .25 * np.sin(
        2 * np.pi * freq * 2 * t
    )

    sub = .20 * np.sin(
        2 * np.pi * freq / 2 * t
    )

    return (
        fundamental
        + harmonic
        + sub
    ) * envelope(
        n,
        .01,
        .15
    ) * .65


def synth_piano(freq, duration):

    n = int(
        duration * SR
    )

    t = np.arange(n) / SR

    signal = (
        np.sin(2 * np.pi * freq * t)
        + .35 * np.sin(2 * np.pi * freq * 2 * t)
        + .15 * np.sin(2 * np.pi * freq * 3 * t)
    )

    return signal * envelope(
        n,
        .01,
        min(.5, duration * .5)
    ) * .22


# ============================================================
# NOTAS
# ============================================================

NOTE_FREQ = {

    "C": 130.81,
    "C#": 138.59,
    "D": 146.83,
    "D#": 155.56,
    "E": 164.81,
    "F": 174.61,
    "F#": 185.00,
    "G": 196.00,
    "G#": 207.65,
    "A": 220.00,
    "A#": 233.08,
    "B": 246.94
}


# ============================================================
# BEAT ENGINE
# ============================================================

def generar_beat_pro(
    bpm,
    duracion,
    tonalidad,
    intensidad,
    swing,
    estilo
):

    total = int(
        SR * duracion
    )

    drums = np.zeros(
        total,
        dtype=np.float32
    )

    bass = np.zeros(
        total,
        dtype=np.float32
    )

    melody = np.zeros(
        total,
        dtype=np.float32
    )

    beat = 60 / bpm
    bar = beat * 4

    # Escala menor natural
    scale_intervals = [
        0,
        2,
        3,
        5,
        7,
        8,
        10
    ]

    root = NOTE_FREQ.get(
        tonalidad,
        NOTE_FREQ["C"]
    )

    scale = [
        root * (
            2 ** (i / 12)
        )
        for i in scale_intervals
    ]

    # --------------------------------------------------------
    # PATRÓN DE BATERÍA
    # --------------------------------------------------------

    bars = int(
        duracion / bar
    ) + 1

    for b in range(bars):

        base = b * bar

        # KICK
        kick_positions = [
            0,
            1.5,
            2.75
        ]

        if estilo == "Boom Bap Cristiano":
            kick_positions = [
                0,
                1.5,
                2.75
            ]

        elif estilo == "Trap":
            kick_positions = [
                0,
                1.25,
                2.5,
                3.25
            ]

        elif estilo == "Dembow":
            kick_positions = [
                0,
                1.75,
                2.5
            ]

        for pos in kick_positions:

            tiempo = (
                base
                + pos * beat
            )

            if tiempo >= duracion:
                continue

            sound = synth_kick()

            start = int(
                tiempo * SR
            )

            end = min(
                start + len(sound),
                total
            )

            drums[start:end] += (
                sound[:end-start]
                * .95
            )

        # SNARE 2 Y 4
        for pos in [1, 3]:

            tiempo = (
                base
                + pos * beat
            )

            if tiempo >= duracion:
                continue

            sound = synth_snare()

            start = int(
                tiempo * SR
            )

            end = min(
                start + len(sound),
                total
            )

            drums[start:end] += (
                sound[:end-start]
                * .75
            )

        # HI HATS
        for step in range(8):

            pos = step * .5

            offset = 0

            if (
                swing > 0
                and step % 2 == 1
            ):
                offset = (
                    swing * beat * .08
                )

            tiempo = (
                base
                + pos * beat
                + offset
            )

            if tiempo >= duracion:
                continue

            sound = synth_hat()

            start = int(
                tiempo * SR
            )

            end = min(
                start + len(sound),
                total
            )

            drums[start:end] += (
                sound[:end-start]
            )

        # ----------------------------------------------------
        # BAJO
        # ----------------------------------------------------

        bass_pattern = [
            0,
            0,
            4,
            3
        ]

        for i, degree in enumerate(
            bass_pattern
        ):

            tiempo = (
                base
                + i * beat
            )

            if tiempo >= duracion:
                continue

            freq = (
                scale[degree]
                / 2
            )

            sound = synth_bass(
                freq,
                beat * .75
            )

            start = int(
                tiempo * SR
            )

            end = min(
                start + len(sound),
                total
            )

            bass[start:end] += (
                sound[:end-start]
            )

        # ----------------------------------------------------
        # MELODÍA / PIANO
        # ----------------------------------------------------

        chord_degrees = [
            0,
            3,
            4,
            2
        ]

        for i, degree in enumerate(
            chord_degrees
        ):

            tiempo = (
                base
                + i * beat
            )

            if tiempo >= duracion:
                continue

            freq = scale[
                degree
            ]

            sound = synth_piano(
                freq,
                beat * 1.8
            )

            start = int(
                tiempo * SR
            )

            end = min(
                start + len(sound),
                total
            )

            melody[start:end] += (
                sound[:end-start]
            )

    # --------------------------------------------------------
    # INTENSIDAD
    # --------------------------------------------------------

    factor = (
        intensity / 10
    )

    drums *= factor
    bass *= factor
    melody *= factor

    # --------------------------------------------------------
    # MASTER
    # --------------------------------------------------------

    master = (
        drums
        + bass
        + melody
    )

    master = normalizar(
        master,
        .90
    )

    return (
        master,
        drums,
        bass,
        melody
    )


# ============================================================
# GENERADOR DE LETRA
# ============================================================

def generar_letra(
    tema,
    genero,
    bpm,
    energia
):

    if modelo is None:

        return (
            "⚠️ Falta GOOGLE_API_KEY.\n\n"
            "Añade GOOGLE_API_KEY en "
            "Streamlit Secrets."
        )

    prompt = f"""

CEREBRO RABINO PRO
MODO COMPOSITOR PROFESIONAL

ARTISTA:
Rabino Rap

TEMA:
{tema}

GÉNERO:
{genero}

BPM:
{bpm}

ENERGÍA:
{energia}/10

IDIOMA:
Español latino.

CREA UNA CANCIÓN ORIGINAL.

ESTRUCTURA EXACTA:

[INTRO]
4 barras.

[VERSO 1]
16 barras EXACTAS.
Rima ABAB.

[PRE-CORO]
4 barras.

[CORO]
8 barras.

[CORO X2]
Repetir el coro.

[VERSO 2]
16 barras EXACTAS.
Rima ABAB.

[PUENTE]
6 barras.

[CORO FINAL]
8 barras.

[OUTRO]
4 barras.

PALABRAS OBLIGATORIAS:

fe
lodo
corona
propósito
Rabino Rap

DIRECCIÓN ARTÍSTICA:

Rap cristiano moderno.
Agresivo pero esperanzador.
Profundo.
Espiritual.
Motivador.
Contundente.
Caribeño.
Fácil de interpretar.

REGLAS:

- No copiar canciones existentes.
- No mencionar otros artistas.
- No explicar la letra.
- Entregar solamente la canción.
- Evitar relleno.
- Rimas naturales.
- Métrica compatible con {bpm} BPM.
- Coro extremadamente memorable.
- Crear imágenes visuales fuertes.
- Mantener un mensaje cristiano claro.
"""

    try:

        response = modelo.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"❌ Error IA: {e}"


# ============================================================
# GENERADOR DE PROMPT MUSICAL
# ============================================================

def crear_prompt_musical(
    tema,
    bpm,
    tonalidad,
    estilo,
    intensidad
):

    return f"""
CEREBRO RABINO PRO — BEAT SPEC

Tema:
{tema}

Estilo:
{estilo}

BPM:
{bpm}

Tonalidad:
{tonalidad} menor

Intensidad:
{intensidad}/10

Drums:
Boom bap moderno.
Kick contundente.
Snare seco y agresivo.
Hi-hats con variaciones.
Ghost notes.
Fills antes de los coros.

Bajo:
Profundo.
Potente.
Subgrave controlado.
Seguir la tonalidad.

Melodía:
Piano oscuro.
Texturas cinematográficas.
Elementos worship.
Ambiente espiritual.

Resultado:
Beat instrumental profesional.
Espacio suficiente para voz de rap.
Máxima energía en el coro final.
"""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ CONTROL CENTRAL")

    nombre_proyecto = st.text_input(
        "Nombre del proyecto",
        "DE LODO A CORONA"
    )

    st.session_state[
        "project_name"
    ] = nombre_proyecto

    st.divider()

    st.subheader(
        "🎛️ Configuración musical"
    )

    bpm_global = st.slider(
        "BPM",
        60,
        180,
        107
    )

    tonalidad_global = st.selectbox(
        "Tonalidad",
        list(NOTE_FREQ.keys()),
        index=0
    )

    intensidad_global = st.slider(
        "Intensidad",
        1,
        10,
        8
    )

    swing_global = st.slider(
        "Swing",
        0.0,
        1.0,
        0.20
    )

    st.divider()

    st.metric(
        "BPM",
        bpm_global
    )

    st.metric(
        "ENERGÍA",
        f"{intensidad_global}/10"
    )

    st.metric(
        "TONALIDAD",
        f"{tonalidad_global} menor"
    )


# ============================================================
# TABS
# ============================================================

tabs = st.tabs([
    "🧠 CEREBRO",
    "✍️ LETRA",
    "🥁 BEAT",
    "🎤 VOZ",
    "🎚️ MIX",
    "📦 EXPORTAR"
])


# ============================================================
# CEREBRO
# ============================================================

with tabs[0]:

    st.header(
        "🧠 DIRECTOR MUSICAL"
    )

    tema_cerebro = st.text_input(
        "¿Qué canción quieres crear?",
        "Dios me levantó del lodo"
    )

    estilo_cerebro = st.selectbox(
        "Dirección",
        [
            "Rap Cristiano + Worship",
            "Boom Bap Cristiano",
            "Trap Cristiano",
            "Dembow Cristiano",
            "Worship Cinemático"
        ]
    )

    energia_cerebro = st.slider(
        "Energía",
        1,
        10,
        8
    )

    if st.button(
        "🚀 CREAR PROYECTO",
        use_container_width=True
    ):

        with st.spinner(
            "CEREBRO está diseñando el proyecto..."
        ):

            letra = generar_letra(
                tema_cerebro,
                estilo_cerebro,
                bpm_global,
                energia_cerebro
            )

            st.session_state[
                "letra"
            ] = letra

            master, drums, bass, melody = (
                generar_beat_pro(
                    bpm_global,
                    150,
                    tonalidad_global,
                    intensidad_global,
                    swing_global,
                    estilo_cerebro
                )
            )

            st.session_state[
                "beat"
            ] = master

            st.session_state[
                "drums"
            ] = drums

            st.session_state[
                "bass"
            ] = bass

            st.session_state[
                "melody"
            ] = melody

        st.success(
            "🔥 Proyecto creado."
        )

    st.divider()

    st.subheader(
        "📋 Estado del proyecto"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "LETRA",
        "✅" if st.session_state["letra"]
        else "❌"
    )

    c2.metric(
        "BEAT",
        "✅" if st.session_state["beat"] is not None
        else "❌"
    )

    c3.metric(
        "DRUMS",
        "✅" if st.session_state["drums"] is not None
        else "❌"
    )

    c4.metric(
        "BAJO",
        "✅" if st.session_state["bass"] is not None
        else "❌"
    )


# ============================================================
# LETRA
# ============================================================

with tabs[1]:

    st.header(
        "✍️ GENERADOR DE LETRAS"
    )

    tema = st.text_input(
        "Tema",
        "Dios me levantó del lodo"
    )

    genero = st.selectbox(
        "Género",
        [
            "Rap Cristiano + Worship",
            "Rap Cristiano",
            "Trap Cristiano",
            "Worship",
            "Dembow Cristiano"
        ]
    )

    if st.button(
        "🧠 GENERAR LETRA",
        use_container_width=True
    ):

        with st.spinner(
            "Escribiendo..."
        ):

            st.session_state[
                "letra"
            ] = generar_letra(
                tema,
                genero,
                bpm_global,
                intensidad_global
            )

    letra_actual = st.text_area(
        "EDITOR",
        st.session_state["letra"],
        height=600
    )

    st.session_state[
        "letra"
    ] = letra_actual


# ============================================================
# BEAT
# ============================================================

with tabs[2]:

    st.header(
        "🥁 BEAT ENGINE"
    )

    estilo_beat = st.selectbox(
        "Estilo",
        [
            "Boom Bap Cristiano",
            "Boom Bap",
            "Trap",
            "Dembow",
            "Worship"
        ]
    )

    duracion_beat = st.slider(
        "Duración",
        30,
        300,
        150
    )

    if st.button(
        "🔥 GENERAR BEAT PRO",
        use_container_width=True
    ):

        with st.spinner(
            "Construyendo batería, bajo y melodía..."
        ):

            (
                master,
                drums,
                bass,
                melody
            ) = generar_beat_pro(
                bpm_global,
                duracion_beat,
                tonalidad_global,
                intensidad_global,
                swing_global,
                estilo_beat
            )

            st.session_state[
                "beat"
            ] = master

            st.session_state[
                "drums"
            ] = drums

            st.session_state[
                "bass"
            ] = bass

            st.session_state[
                "melody"
            ] = melody

        st.success(
            "🔥 Beat generado."
        )

    if st.session_state[
        "beat"
    ] is not None:

        st.subheader(
            "🎧 MASTER"
        )

        master_wav = convertir_wav(
            st.session_state["beat"]
        )

        st.audio(
            master_wav,
            format="audio/wav"
        )

        st.download_button(
            "⬇️ DESCARGAR BEAT WAV",
            master_wav,
            file_name=(
                st.session_state[
                    "project_name"
                ]
                + "_MASTER.wav"
            ),
            mime="audio/wav"
        )

        st.divider()

        st.subheader(
            "🎚️ STEMS"
        )

        col1, col2, col3 = st.columns(3)

        drums_wav = convertir_wav(
            st.session_state["drums"]
        )

        bass_wav = convertir_wav(
            st.session_state["bass"]
        )

        melody_wav = convertir_wav(
            st.session_state["melody"]
        )

        with col1:

            st.write("🥁 DRUMS")

            st.audio(
                drums_wav,
                format="audio/wav"
            )

            st.download_button(
                "⬇️ DRUMS",
                drums_wav,
                file_name="drums.wav",
                mime="audio/wav"
            )

        with col2:

            st.write("🔊 BASS")

            st.audio(
                bass_wav,
                format="audio/wav"
            )

            st.download_button(
                "⬇️ BASS",
                bass_wav,
                file_name="bass.wav",
                mime="audio/wav"
            )

        with col3:

            st.write("🎹 MELODY")

            st.audio(
                melody_wav,
                format="audio/wav"
            )

            st.download_button(
                "⬇️ MELODY",
                melody_wav,
                file_name="melody.wav",
                mime="audio/wav"
            )


# ============================================================
# VOZ
# ============================================================

with tabs[3]:

    st.header(
        "🎤 VOCES"
    )

    st.warning(
        "La voz que tienes actualmente con gTTS "
        "es voz hablada. No es un motor de rap/canto."
    )

    st.write(
        "Aquí dejamos preparado el punto de conexión "
        "para un motor vocal local."
    )

    st.code(
        """
LETRA
   ↓
MODELO VOCAL
   ↓
VOZ RAP
   ↓
WAV
   ↓
MIX
        """
    )

    st.info(
        "La siguiente evolución será conectar "
        "un modelo de voz musical que funcione "
        "localmente en tu PC."
    )


# ============================================================
# MIX
# ============================================================

with tabs[4]:

    st.header(
        "🎚️ MEZCLADOR"
    )

    volumen = st.slider(
        "🔊 Volumen",
        0.0,
        1.0,
        0.8
    )

    graves = st.slider(
        "🥁 Graves",
        -12.0,
        12.0,
        3.0
    )

    agudos = st.slider(
        "✨ Agudos",
        -12.0,
        12.0,
        2.0
    )

    reverb = st.slider(
        "🌊 Reverb",
        0.0,
        1.0,
        0.3
    )

    delay = st.slider(
        "⏱️ Delay",
        0.0,
        1.0,
        0.1
    )

    st.divider()

    st.write(
        "🎛️ CONFIGURACIÓN ACTUAL"
    )

    st.json({
        "volumen": volumen,
        "graves_db": graves,
        "agudos_db": agudos,
        "reverb": reverb,
        "delay": delay
    })

    st.info(
        "El mezclador está preparado para la "
        "siguiente etapa: procesamiento DSP real "
        "de stems y voces."
    )


# ============================================================
# EXPORTAR
# ============================================================

with tabs[5]:

    st.header(
        "📦 EXPORTAR PROYECTO"
    )

    if (
        st.session_state["beat"] is None
        and not st.session_state["letra"]
    ):

        st.warning(
            "Todavía no hay un proyecto para exportar."
        )

    else:

        if st.button(
            "📦 CREAR PAQUETE DEL PROYECTO",
            use_container_width=True
        ):

            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(
                zip_buffer,
                "w",
                zipfile.ZIP_DEFLATED
            ) as z:

                # LETRA
                z.writestr(
                    "letra.txt",
                    st.session_state[
                        "letra"
                    ]
                )

                # CONFIG
                config = {
                    "project": st.session_state[
                        "project_name"
                    ],
                    "bpm": bpm_global,
                    "key": tonalidad_global,
                    "intensity": intensidad_global,
                    "swing": swing_global
                }

                z.writestr(
                    "config.json",
                    json.dumps(
                        config,
                        indent=4,
                        ensure_ascii=False
                    )
                )

                # STEMS
                if st.session_state[
                    "beat"
                ] is not None:

                    z.writestr(
                        "MASTER.wav",
                        convertir_wav(
                            st.session_state[
                                "beat"
                            ]
                        )
                    )

                    z.writestr(
                        "DRUMS.wav",
                        convertir_wav(
                            st.session_state[
                                "drums"
                            ]
                        )
                    )

                    z.writestr(
                        "BASS.wav",
                        convertir_wav(
                            st.session_state[
                                "bass"
                            ]
                        )
                    )

                    z.writestr(
                        "MELODY.wav",
                        convertir_wav(
                            st.session_state[
                                "melody"
                            ]
                        )
                    )

            zip_buffer.seek(0)

            st.download_button(
                "⬇️ DESCARGAR PROYECTO COMPLETO",
                zip_buffer,
                file_name=(
                    st.session_state[
                        "project_name"
                    ]
                    + ".zip"
                ),
                mime="application/zip"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.success(
    "🧠 CEREBRO RABINO PRO — MOTOR MUSICAL ACTIVO"
)

st.caption(
    "Rabino Rap © 2026 — AI MUSIC STUDIO"
    )
