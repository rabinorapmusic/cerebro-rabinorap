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
ESTUDIO_CEREBRO_RABINO_PRO = """
# 🎤 CEREBRO RABINO PRO — ESTUDIO COMPLETO

## 1. LETRA

Título: Dios me levantó del lodo
Artista: Rabino Rap
Género: Rap Cristiano + Worship
Subgénero: Boom Bap Cristiano moderno
Idioma: Español

Vibe:
Agresivo, épico, espiritual, motivador y lleno de esperanza.

Mensaje:
Dios rescata al ser humano de su pasado, lo restaura, le devuelve
identidad y lo levanta para cumplir su propósito.

PALABRAS OBLIGATORIAS:
fe, lodo, corona, propósito, Rabino Rap

ESTRUCTURA EXACTA:

INTRO:
4 barras.

VERSO 1:
Exactamente 16 barras.
Esquema de rima ABAB.
Flow agresivo pero claro.
Hablar del pasado, caída, dolor y rescate de Dios.

PRE-CORO:
4 barras.
Aumentar progresivamente la emoción.

CORO:
8 barras.
Melódico, poderoso y fácil de recordar.
Mezcla de rap y worship.
Debe transmitir victoria y esperanza.
Incluir naturalmente las palabras fe, lodo y corona.

CORO X2:
Repetir exactamente el coro.
La segunda repetición debe tener mayor intensidad.

VERSO 2:
Exactamente 16 barras.
Esquema de rima ABAB.
Más agresivo que el verso 1.
Hablar de transformación, propósito, victoria y nueva identidad.
Incluir naturalmente "Rabino Rap".

PUENTE:
6 barras.
Más worship.
Sensación de elevación espiritual.

CORO FINAL:
8 barras.
Máxima intensidad.
Voz principal + dobles + ad-libs.
Sensación de victoria.

OUTRO:
4 barras.
Cierre emocional.
Terminar con una frase contundente relacionada con
Dios levantando al protagonista del lodo.

REGLAS:
- Letra completamente original.
- No copiar canciones existentes.
- Español latino/caribeño.
- Rimas naturales.
- No usar relleno.
- Mantener coherencia narrativa.
- Métrica compatible con 107 BPM.
- Mantener mensaje cristiano.
- Flow agresivo pero esperanzador.


## 2. BEAT

Estilo: Boom Bap Cristiano moderno
BPM: 107
Tonalidad: C menor
Duración: 2:30
Intensidad: 8/10

BATERÍA:
- Kick fuerte.
- Kick principal en 1 y 3.
- Snare fuerte en 2 y 4.
- Hi-hats con dobles golpes y variaciones.
- Ghost notes sutiles.
- Fills antes de coros.

BAJO:
- Potente y profundo.
- Tonalidad C menor.
- Subgrave controlado.
- No competir con la voz.

INSTRUMENTOS:
- Piano oscuro en C menor.
- Texturas worship.
- Cuerdas cinematográficas.
- Atmósferas espirituales.
- Melodía memorable sin competir con la voz.

ESTRUCTURA DEL BEAT:

0:00 - 0:10  INTRO
0:10 - 0:42  VERSO 1
0:42 - 0:52  PRE-CORO
0:52 - 1:10  CORO
1:10 - 1:28  CORO X2
1:28 - 2:00  VERSO 2
2:00 - 2:10  PUENTE
2:10 - 2:25  CORO FINAL
2:25 - 2:30  OUTRO


## 3. VOCES

Tipo:
Voz masculina.

Idioma:
Español.

Estilo:
Rap cristiano agresivo moderno.

Velocidad:
Normal.

Dicción:
Clara, fuerte y contundente.

Emoción:
Confianza + unción + esperanza + autoridad.

INTERPRETACIÓN:

VERSOS:
Rap firme y agresivo.

PRE-CORO:
Aumentar emoción.

CORO:
Interpretación melódica/worship.

PUENTE:
Más emocional y espiritual.

CORO FINAL:
Máxima potencia.

CAPAS:
- Voz principal centrada.
- Dobles discretos.
- Ad-libs.
- Coros más amplios.
- No saturar de efectos.


## 4. MEZCLA

Volumen objetivo: 0.8

EQ VOCAL:
Graves: +3 dB
Agudos: +2 dB

EFECTOS:
Reverb vocal: 0.3
Delay del coro: 0.1

Además:
- Compresión vocal moderada.
- Control de sibilancias.
- Voz siempre al frente.
- Bajo potente pero limpio.
- Evitar clipping.
- Evitar distorsión digital.
- Master fuerte pero limpio.


## 5. PORTADA

Título:
DE LODO A CORONA

Artista:
Rabino Rap

CONCEPTO:

Un hombre emerge de un terreno de lodo oscuro.
El lodo representa el pasado, dolor, pecado y dificultades.

Sobre él aparece una corona formada por luz dorada,
representando restauración, victoria, identidad y propósito.

ESTILO:
- Fondo negro profundo.
- Iluminación dorada cinematográfica.
- Contraste alto.
- 3D épico.
- Realista.
- Atmósfera espiritual.
- Rayos de luz.
- Partículas doradas.
- Sensación de transformación y victoria.

TEXTO PRINCIPAL:
DE LODO A CORONA

TEXTO SECUNDARIO:
Rabino Rap

TEXTO DE MARCA:
CEREBRO RABINO PRO

FORMATO:
3000 x 3000 px
Cuadrado
Alta resolución
Diseño profesional para plataformas musicales.


## OBJETIVO FINAL

Crear un proyecto musical profesional llamado:

"DE LODO A CORONA"

Artista:
Rabino Rap

El resultado debe sentirse:
ÉPICO + ESPIRITUAL + AGRESIVO + MOTIVADOR + PROFESIONAL.

Mensaje central:

"Dios puede sacar a una persona del lodo,
restaurarla, darle una corona y devolverle su propósito."
"""


# ============================================================
# FUNCIÓN PARA CONSTRUIR EL PROMPT FINAL
# ============================================================

def generar_prompt_estudio(
    tema="Dios me levantó del lodo",
    artista="Rabino Rap"
):
    prompt = ESTUDIO_CEREBRO_RABINO_PRO

    prompt += f"""

DATOS DEL PROYECTO:

Tema: {tema}
Artista: {artista}

IMPORTANTE:
Respeta exactamente la estructura indicada.
Los versos deben tener exactamente 16 barras cada uno.
Mantén el esquema ABAB en los versos.
No elimines las palabras obligatorias.
No cambies el BPM, tonalidad ni duración.
Genera contenido original.
"""

    return prompt


# ============================================================
# EJEMPLO
# ============================================================

if __name__ == "__main__":

    prompt_final = generar_prompt_estudio()

    print("=" * 70)
    print("🎤 CEREBRO RABINO PRO")
    print("=" * 70)
    print(prompt_final)
