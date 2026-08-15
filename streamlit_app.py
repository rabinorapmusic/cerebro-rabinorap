import streamlit as st
import numpy as np
import io
import wave
import json
import zipfile
from gtts import gTTS

# ============================================================
# GEMINI
# ============================================================

try:
    import google.generativeai as genai
except ImportError:
    genai = None


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="CEREBRO RABINO PRO",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 CEREBRO RABINO PRO")
st.caption("🎤 AI MUSIC STUDIO — RABINO RAP")


# ============================================================
# CONFIGURACIÓN GEMINI
# ============================================================

modelo = None

try:
    GOOGLE_API_KEY = st.secrets.get(
        "GOOGLE_API_KEY",
        ""
    )

    if GOOGLE_API_KEY and genai:

        genai.configure(
            api_key=GOOGLE_API_KEY
        )

        modelo = genai.GenerativeModel(
            "gemini-1.5-flash"
        )

except Exception as e:

    modelo = None


# ============================================================
# SESSION STATE
# ============================================================

if "letra" not in st.session_state:
    st.session_state.letra = ""

if "beat" not in st.session_state:
    st.session_state.beat = None

if "drums" not in st.session_state:
    st.session_state.drums = None

if "bass" not in st.session_state:
    st.session_state.bass = None

if "melody" not in st.session_state:
    st.session_state.melody = None

if "voz" not in st.session_state:
    st.session_state.voz = None

if "project_name" not in st.session_state:
    st.session_state.project_name = "DE LODO A CORONA"


# ============================================================
# AUDIO
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

    audio = normalizar(
        audio,
        0.92
    )

    audio_int16 = (
        audio * 32767
    ).astype(np.int16)

    buffer = io.BytesIO()

    with wave.open(
        buffer,
        "wb"
    ) as archivo:

        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(SR)

        archivo.writeframes(
            audio_int16.tobytes()
        )

    return buffer.getvalue()


# ============================================================
# SINTETIZADORES
# ============================================================

def crear_envolvente(
    cantidad,
    ataque=0.005,
    release=0.15
):

    t = np.arange(
        cantidad
    ) / SR

    env = np.ones(
        cantidad,
        dtype=np.float32
    )

    attack_samples = max(
        1,
        int(ataque * SR)
    )

    release_samples = max(
        1,
        int(release * SR)
    )

    attack_samples = min(
        attack_samples,
        cantidad
    )

    release_samples = min(
        release_samples,
        cantidad
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


def sintetizar_kick():

    duracion = 0.35

    n = int(
        duracion * SR
    )

    t = np.arange(n) / SR

    frecuencia = (
        140 * np.exp(-18 * t)
        + 42
    )

    fase = (
        2
        * np.pi
        * np.cumsum(frecuencia)
        / SR
    )

    cuerpo = np.sin(
        fase
    )

    click = (
        np.random.randn(n)
        * np.exp(-100 * t)
        * 0.12
    )

    return (
        cuerpo * np.exp(-10 * t)
        + click
    )


def sintetizar_snare():

    duracion = 0.22

    n = int(
        duracion * SR
    )

    t = np.arange(n) / SR

    ruido = np.random.randn(n)

    ruido *= np.exp(
        -22 * t
    )

    tono = (
        np.sin(
            2
            * np.pi
            * 190
            * t
        )
        * np.exp(-18 * t)
    )

    return (
        ruido * 0.55
        + tono * 0.30
    )


def sintetizar_hat():

    duracion = 0.055

    n = int(
        duracion * SR
    )

    t = np.arange(n) / SR

    ruido = np.random.randn(n)

    return (
        ruido
        * np.exp(-70 * t)
        * 0.20
    )


def sintetizar_bajo(
    frecuencia,
    duracion
):

    n = int(
        duracion * SR
    )

    t = np.arange(n) / SR

    fundamental = np.sin(
        2
        * np.pi
        * frecuencia
        * t
    )

    segundo_armonico = (
        0.25
        * np.sin(
            2
            * np.pi
            * frecuencia
            * 2
            * t
        )
    )

    sub = (
        0.20
        * np.sin(
            2
            * np.pi
            * frecuencia
            / 2
            * t
        )
    )

    señal = (
        fundamental
        + segundo_armonico
        + sub
    )

    return (
        señal
        * crear_envolvente(
            n,
            0.01,
            0.15
        )
        * 0.65
    )


def sintetizar_piano(
    frecuencia,
    duracion
):

    n = int(
        duracion * SR
    )

    t = np.arange(n) / SR

    señal = (
        np.sin(
            2
            * np.pi
            * frecuencia
            * t
        )
        + 0.35
        * np.sin(
            2
            * np.pi
            * frecuencia
            * 2
            * t
        )
        + 0.15
        * np.sin(
            2
            * np.pi
            * frecuencia
            * 3
            * t
        )
    )

    return (
        señal
        * crear_envolvente(
            n,
            0.01,
            min(
                0.5,
                duracion * 0.5
            )
        )
        * 0.22
    )


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
# INSERTAR SONIDO
# ============================================================

def insertar_audio(
    destino,
    sonido,
    tiempo
):

    inicio = int(
        tiempo * SR
    )

    if inicio >= len(destino):
        return

    final = min(
        inicio + len(sonido),
        len(destino)
    )

    destino[inicio:final] += (
        sonido[:final - inicio]
    )


# ============================================================
# GENERADOR DE BEAT
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

    compas = beat * 4

    root = NOTE_FREQ.get(
        tonalidad,
        NOTE_FREQ["C"]
    )

    # Escala menor
    intervalos = [
        0,
        2,
        3,
        5,
        7,
        8,
        10
    ]

    escala = [
        root * (
            2 ** (intervalo / 12)
        )
        for intervalo in intervalos
    ]

    cantidad_compases = int(
        duracion / compas
    ) + 1

    for compas_num in range(
        cantidad_compases
    ):

        inicio_compas = (
            compas_num
            * compas
        )

        # ----------------------------------------------------
        # KICK
        # ----------------------------------------------------

        if estilo == "Dembow":

            kick_pattern = [
                0,
                1.75,
                2.5
            ]

        elif estilo == "Trap":

            kick_pattern = [
                0,
                1.25,
                2.5,
                3.25
            ]

        else:

            kick_pattern = [
                0,
                1.5,
                2.75
            ]

        for posicion in kick_pattern:

            tiempo = (
                inicio_compas
                + posicion * beat
            )

            if tiempo >= duracion:
                continue

            insertar_audio(
                drums,
                sintetizar_kick(),
                tiempo
            )

        # ----------------------------------------------------
        # SNARE
        # ----------------------------------------------------

        for posicion in [
            1,
            3
        ]:

            tiempo = (
                inicio_compas
                + posicion * beat
            )

            if tiempo >= duracion:
                continue

            insertar_audio(
                drums,
                sintetizar_snare(),
                tiempo
            )

        # ----------------------------------------------------
        # HI-HATS
        # ----------------------------------------------------

        for paso in range(8):

            posicion = (
                paso * 0.5
            )

            desplazamiento = 0

            if (
                swing > 0
                and paso % 2 == 1
            ):

                desplazamiento = (
                    swing
                    * beat
                    * 0.08
                )

            tiempo = (
                inicio_compas
                + posicion * beat
                + desplazamiento
            )

            if tiempo >= duracion:
                continue

            insertar_audio(
                drums,
                sintetizar_hat(),
                tiempo
            )

        # ----------------------------------------------------
        # BAJO
        # ----------------------------------------------------

        patron_bajo = [
            0,
            0,
            4,
            3
        ]

        for i, grado in enumerate(
            patron_bajo
        ):

            tiempo = (
                inicio_compas
                + i * beat
            )

            if tiempo >= duracion:
                continue

            frecuencia = (
                escala[grado]
                / 2
            )

            insertar_audio(
                bass,
                sintetizar_bajo(
                    frecuencia,
                    beat * 0.75
                ),
                tiempo
            )

        # ----------------------------------------------------
        # MELODÍA
        # ----------------------------------------------------

        patron_melodia = [
            0,
            3,
            4,
            2
        ]

        for i, grado in enumerate(
            patron_melodia
        ):

            tiempo = (
                inicio_compas
                + i * beat
            )

            if tiempo >= duracion:
                continue

            insertar_audio(
                melody,
                sintetizar_piano(
                    escala[grado],
                    beat * 1.8
                ),
                tiempo
            )

    # --------------------------------------------------------
    # INTENSIDAD
    # --------------------------------------------------------

    factor = (
        intensidad / 10
    )

    drums *= factor
    bass *= factor
    melody *= factor

    master = (
        drums
        + bass
        + melody
    )

    master = normalizar(
        master,
        0.90
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
    intensidad
):

    if modelo is None:

        return (
            "⚠️ No hay conexión con Gemini.\n\n"
            "Configura GOOGLE_API_KEY "
            "en Streamlit Secrets."
        )

    prompt = f"""
CEREBRO RABINO PRO
MODO ESTUDIO COMPLETO

ARTISTA:
Rabino Rap

TEMA:
{tema}

GÉNERO:
{genero}

BPM:
{bpm}

INTENSIDAD:
{intensidad}/10

IDIOMA:
Español latino.

CREA UNA CANCIÓN COMPLETAMENTE ORIGINAL.

ESTRUCTURA OBLIGATORIA:

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
Repetir exactamente el coro.

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

DIRECCIÓN:

Rap Cristiano + Worship.
Agresivo pero con esperanza.
Épico.
Espiritual.
Motivador.
Profundo.
Contundente.
Fácil de rapear.
Coro memorable.

REGLAS:

- Letra 100% original.
- No copiar canciones.
- No imitar literalmente a otros artistas.
- No explicar la canción.
- Entregar únicamente la letra.
- No usar relleno.
- Rimas naturales.
- Métrica compatible con {bpm} BPM.
- Mantener mensaje cristiano.
"""

    try:

        respuesta = modelo.generate_content(
            prompt
        )

        if respuesta and respuesta.text:

            return respuesta.text

        return "No se recibió contenido."

    except Exception as e:

        return (
            f"❌ Error de Gemini:\n{e}"
        )


# ============================================================
# GENERADOR DE VOZ
# ============================================================

def generar_voz(texto):

    buffer = io.BytesIO()

    tts = gTTS(
        text=texto,
        lang="es",
        slow=False
    )

    tts.write_to_fp(
        buffer
    )

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "⚙️ CONTROL CENTRAL"
    )

    st.session_state.project_name = (
        st.text_input(
            "Proyecto",
            st.session_state.project_name
        )
    )

    bpm = st.slider(
        "🥁 BPM",
        60,
        180,
        107
    )

    tonalidad = st.selectbox(
        "🎹 Tonalidad",
        list(
            NOTE_FREQ.keys()
        ),
        index=0
    )

    intensidad = st.slider(
        "🔥 Intensidad",
        1,
        10,
        8
    )

    swing = st.slider(
        "🎵 Swing",
        0.0,
        1.0,
        0.20
    )

    st.divider()

    st.metric(
        "BPM",
        bpm
    )

    st.metric(
        "TONALIDAD",
        tonalidad + " menor"
    )

    st.metric(
        "ENERGÍA",
        f"{intensidad}/10"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🧠 CEREBRO",
        "✍️ LETRAS",
        "🥁 BEATS",
        "🎤 VOCES",
        "🎚️ ESTUDIO",
        "📦 EXPORTAR"
    ]
)


# ============================================================
# CEREBRO
# ============================================================

with tab1:

    st.header(
        "🧠 DIRECTOR MUSICAL"
    )

    tema = st.text_input(
        "Tema principal",
        "Dios me levantó del lodo"
    )

    genero = st.selectbox(
        "Género",
        [
            "Rap Cristiano + Worship",
            "Boom Bap Cristiano",
            "Trap Cristiano",
            "Dembow Cristiano",
            "Worship"
        ]
    )

    if st.button(
        "🚀 CREAR PROYECTO COMPLETO",
        use_container_width=True
    ):

        with st.spinner(
            "🧠 CEREBRO está creando letra y beat..."
        ):

            # LETRA
            st.session_state.letra = (
                generar_letra(
                    tema,
                    genero,
                    bpm,
                    intensidad
                )
            )

            # BEAT
            (
                master,
                drums,
                bass,
                melody
            ) = generar_beat_pro(
                bpm,
                150,
                tonalidad,
                intensidad,
                swing,
                genero
            )

            st.session_state.beat = master
            st.session_state.drums = drums
            st.session_state.bass = bass
            st.session_state.melody = melody

        st.success(
            "🔥 PROYECTO CREADO"
        )

    st.divider()

    st.subheader(
        "📊 ESTADO"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "LETRA",
        "✅"
        if st.session_state.letra
        else "❌"
    )

    c2.metric(
        "BEAT",
        "✅"
        if st.session_state.beat is not None
        else "❌"
    )

    c3.metric(
        "DRUMS",
        "✅"
        if st.session_state.drums is not None
        else "❌"
    )

    c4.metric(
        "BAJO",
        "✅"
        if st.session_state.bass is not None
        else "❌"
    )


# ============================================================
# LETRAS
# ============================================================

with tab2:

    st.header(
        "✍️ GENERADOR DE LETRAS IA"
    )

    tema_letra = st.text_input(
        "Tema",
        "Dios me levantó del lodo",
        key="tema_letra"
    )

    genero_letra = st.selectbox(
        "Estilo",
        [
            "Rap Cristiano + Worship",
            "Rap Cristiano",
            "Trap Cristiano",
            "Worship",
            "Dembow Cristiano"
        ],
        key="genero_letra"
    )

    if st.button(
        "🧠 GENERAR LETRA",
        use_container_width=True
    ):

        with st.spinner(
            "Escribiendo canción..."
        ):

            st.session_state.letra = (
                generar_letra(
                    tema_letra,
                    genero_letra,
                    bpm,
                    intensidad
                )
            )

    letra_editada = st.text_area(
        "EDITOR DE LETRA",
        st.session_state.letra,
        height=600
    )

    st.session_state.letra = (
        letra_editada
    )


# ============================================================
# BEATS
# ============================================================

with tab3:

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
        ],
        key="estilo_beat"
    )

    duracion = st.slider(
        "Duración del beat",
        30,
        300,
        150
    )

    if st.button(
        "🔥 GENERAR BEAT PRO",
        use_container_width=True
    ):

        with st.spinner(
            "🥁 Generando batería + bajo + melodía..."
        ):

            (
                master,
                drums,
                bass,
                melody
            ) = generar_beat_pro(
                bpm,
                duracion,
                tonalidad,
                intensidad,
                swing,
                estilo_beat
            )

            st.session_state.beat = master
            st.session_state.drums = drums
            st.session_state.bass = bass
            st.session_state.melody = melody

        st.success(
            "🔥 BEAT LISTO"
        )

    if st.session_state.beat is not None:

        master_wav = convertir_wav(
            st.session_state.beat
        )

        st.subheader(
            "🎧 MASTER"
        )

        st.audio(
            master_wav,
            format="audio/wav"
        )

        st.download_button(
            "⬇️ DESCARGAR MASTER WAV",
            master_wav,
            file_name=(
                st.session_state.project_name
                + "_MASTER.wav"
            ),
            mime="audio/wav"
        )

        st.divider()

        st.subheader(
            "🎚️ STEMS"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            drums_wav = convertir_wav(
                st.session_state.drums
            )

            st.write(
                "🥁 BATERÍA"
            )

            st.audio(
                drums_wav,
                format="audio/wav"
            )

            st.download_button(
                "⬇️ DRUMS",
                drums_wav,
                file_name="DRUMS.wav",
                mime="audio/wav"
            )

        with col2:

            bass_wav = convertir_wav(
                st.session_state.bass
            )

            st.write(
                "🔊 BAJO"
            )

            st.audio(
                bass_wav,
                format="audio/wav"
            )

            st.download_button(
                "⬇️ BASS",
                bass_wav,
                file_name="BASS.wav",
                mime="audio/wav"
            )

        with col3:

            melody_wav = convertir_wav(
                st.session_state.melody
            )

            st.write(
                "🎹 MELODÍA"
            )

            st.audio(
                melody_wav,
                format="audio/wav"
            )

            st.download_button(
                "⬇️ MELODY",
                melody_wav,
                file_name="MELODY.wav",
                mime="audio/wav"
            )


# ============================================================
# VOCES
# ============================================================

with tab4:

    st.header(
        "🎤 VOCES"
    )

    st.warning(
        "gTTS genera voz hablada, no una voz de rap/canto profesional."
    )

    texto_voz = st.text_area(
        "Texto para voz",
        st.session_state.letra,
        height=300
    )

    if st.button(
        "🎤 GENERAR VOZ",
        use_container_width=True
    ):

        if not texto_voz.strip():

            st.warning(
                "Primero genera una letra."
            )

        else:

            with st.spinner(
                "Generando voz..."
            ):

                try:

                    st.session_state.voz = (
                        generar_voz(
                            texto_voz
                        )
                    )

                    st.success(
                        "Voz generada."
                    )

                except Exception as e:

                    st.error(
                        f"Error de voz: {e}"
                    )

    if st.session_state.voz:

        st.audio(
            st.session_state.voz,
            format="audio/mp3"
        )

        st.download_button(
            "⬇️ DESCARGAR VOZ",
            st.session_state.voz,
            file_name="Rabino_Rap_Voz.mp3",
            mime="audio/mp3"
        )


# ============================================================
# ESTUDIO
# ============================================================

with tab5:

    st.header(
        "🎚️ ESTUDIO"
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

    st.json({
        "volumen": volumen,
        "EQ_graves": f"{graves} dB",
        "EQ_agudos": f"{agudos} dB",
        "reverb": reverb,
        "delay": delay
    })

    st.info(
        "🎚️ Los controles están preparados. "
        "La siguiente etapa es aplicar DSP real "
        "al beat y a las voces."
    )


# ============================================================
# EXPORTAR
# ============================================================

with tab6:

    st.header(
        "📦 EXPORTAR PROYECTO"
    )

    if st.button(
        "📦 CREAR ZIP COMPLETO",
        use_container_width=True
    ):

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(
            zip_buffer,
            "w",
            zipfile.ZIP_DEFLATED
        ) as archivo_zip:

            # ------------------------------------------------
            # LETRA
            # ------------------------------------------------

            archivo_zip.writestr(
                "LETRA.txt",
                st.session_state.letra
            )

            # ------------------------------------------------
            # CONFIGURACIÓN
            # ------------------------------------------------

            configuracion = {

                "proyecto":
                    st.session_state.project_name,

                "artista":
                    "Rabino Rap",

                "bpm":
                    bpm,

                "tonalidad":
                    tonalidad,

                "modo":
                    tonalidad + " menor",

                "intensidad":
                    intensidad,

                "swing":
                    swing
            }

            archivo_zip.writestr(
                "CONFIG.json",
                json.dumps(
                    configuracion,
                    indent=4,
                    ensure_ascii=False
                )
            )

            # ------------------------------------------------
            # AUDIO
            # ------------------------------------------------

            if st.session_state.beat is not None:

                archivo_zip.writestr(
                    "MASTER.wav",
                    convertir_wav(
                        st.session_state.beat
                    )
                )

                archivo_zip.writestr(
                    "DRUMS.wav",
                    convertir_wav(
                        st.session_state.drums
                    )
                )

                archivo_zip.writestr(
                    "BASS.wav",
                    convertir_wav(
                        st.session_state.bass
                    )
                )

                archivo_zip.writestr(
                    "MELODY.wav",
                    convertir_wav(
                        st.session_state.melody
                    )
                )

            # ------------------------------------------------
            # VOZ
            # ------------------------------------------------

            if st.session_state.voz:

                archivo_zip.writestr(
                    "VOZ.mp3",
                    st.session_state.voz
                )

        zip_buffer.seek(0)

        st.success(
            "📦 Proyecto preparado."
        )

        st.download_button(
            "⬇️ DESCARGAR PROYECTO COMPLETO",
            zip_buffer,
            file_name=(
                st.session_state.project_name
                + ".zip"
            ),
            mime="application/zip"
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.success(
    "🧠 CEREBRO RABINO PRO — ACTIVO"
)

st.caption(
    "Rabino Rap • AI Music Studio"
)
