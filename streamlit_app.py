import streamlit as st
import requests
import json
import random
import math
import io
import wave
import re
from datetime import datetime

# ==========================================================
# CEREBRO OMEGA v2
# ==========================================================

st.set_page_config(
    page_title="CEREBRO OMEGA v2",
    page_icon="🧠",
    layout="wide"
)

# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULTS = {
    "respuesta": "",
    "memoria": [],
    "experimentos": [],
    "audio": None,
    "ultimo_prompt": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

MODELOS = [
    "llama3.2",
    "qwen2.5",
    "gemma3",
    "mistral"
]


# ==========================================================
# ESTILO
# ==========================================================

st.markdown("""
<style>

.omega-title {
    text-align:center;
    font-size:48px;
    font-weight:900;
}

.omega-subtitle {
    text-align:center;
    opacity:.75;
    margin-bottom:25px;
}

.card {
    padding:18px;
    border-radius:16px;
    border:1px solid rgba(128,128,128,.25);
    margin-bottom:12px;
}

.big-button {
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# FUNCIONES GENERALES
# ==========================================================

def guardar_memoria(tipo, contenido):

    registro = {
        "fecha": datetime.now().isoformat(),
        "tipo": tipo,
        "contenido": contenido
    }

    st.session_state.memoria.append(registro)


def limpiar_nombre(texto):

    texto = re.sub(
        r"[^a-zA-Z0-9_\-]",
        "_",
        texto
    )

    return texto[:80]


# ==========================================================
# OLLAMA
# ==========================================================

def ollama_disponible():

    try:

        r = requests.get(
            "http://localhost:11434/api/tags",
            timeout=2
        )

        return r.status_code == 200

    except Exception:

        return False


def preguntar_ia(prompt, modelo):

    try:

        respuesta = requests.post(
            OLLAMA_URL,
            json={
                "model": modelo,
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        if respuesta.status_code != 200:
            return "ERROR: Ollama respondió con código " + str(
                respuesta.status_code
            )

        data = respuesta.json()

        return data.get(
            "response",
            "La IA no devolvió respuesta."
        )

    except Exception as e:

        return (
            "MODELO LOCAL NO DISPONIBLE.\n\n"
            "Instala Ollama y descarga un modelo.\n\n"
            f"Detalle: {e}"
        )


# ==========================================================
# DIRECTOR OMEGA
# ==========================================================

def director_omega(
    objetivo,
    contexto,
    modelo,
    profundidad,
    atrevimiento
):

    prompt = f"""
Eres CEREBRO OMEGA, un laboratorio interdisciplinario.

OBJETIVO:
{objetivo}

CONTEXTO:
{contexto}

PROFUNDIDAD:
{profundidad}/100

ATREVIMIENTO:
{atrevimiento}/100

Debes trabajar como un equipo compuesto por:

1. DIRECTOR
2. CIENTÍFICO
3. FILÓSOFO
4. ANALISTA
5. CREADOR
6. CRÍTICO
7. OPTIMIZADOR

REGLAS:

- Separa hechos de hipótesis.
- Separa ciencia de metáforas espirituales.
- No presentes especulación como hecho.
- Busca conexiones interdisciplinarias.
- Propón experimentos verificables cuando sea posible.
- Busca alternativas.
- Critica tus propias conclusiones.
- No aceptes automáticamente la primera solución.

RESPONDE EN ESTA ESTRUCTURA:

[OBJETIVO]

[MAPA DEL PROBLEMA]

[CIENCIA]

[FILOSOFÍA]

[ESPIRITUALIDAD / SIMBOLISMO]

[HIPÓTESIS]

[CONTRAARGUMENTOS]

[EXPERIMENTOS]

[IDEAS NUEVAS]

[MEJOR SOLUCIÓN]

[SIGUIENTE EXPERIMENTO]
"""

    return preguntar_ia(
        prompt,
        modelo
    )


# ==========================================================
# MOTOR DE MUTACIÓN
# ==========================================================

def mutar_idea(idea, cantidad=10):

    mutaciones = [
        "invertir el supuesto principal",
        "eliminar una restricción",
        "añadir una restricción extrema",
        "combinar dos disciplinas",
        "buscar una explicación alternativa",
        "reducir el problema al mínimo",
        "imaginar el problema a escala planetaria",
        "imaginarlo a escala microscópica",
        "buscar una solución completamente distinta",
        "convertirlo en un experimento computacional"
    ]

    resultados = []

    for i in range(cantidad):

        cambio = random.choice(
            mutaciones
        )

        resultados.append(
            f"VARIANTE {i+1}\n"
            f"Idea: {idea}\n"
            f"Mutación: {cambio}\n"
        )

    return "\n\n".join(
        resultados
    )


# ==========================================================
# SIMULADOR EVOLUTIVO
# ==========================================================

def evolucion_simulada(
    generaciones,
    poblacion,
    seleccion,
    mutacion
):

    frecuencia = 0.5

    datos = []

    for generacion in range(
        generaciones
    ):

        fitness_a = 1.0

        fitness_b = (
            1.0 +
            seleccion
        )

        frecuencia = (
            frecuencia * fitness_a
        ) / (
            frecuencia * fitness_a
            +
            (1-frequency) * fitness_b
        )

        frecuencia += (
            mutacion *
            (1-frequency)
        )

        frecuencia -= (
            mutacion *
            0.25 *
            frecuencia
        )

        frecuencia = max(
            0,
            min(
                1,
                frecuencia
            )
        )

        datos.append(
            {
                "Generación":
                    generacion + 1,

                "Frecuencia":
                    frecuencia
            }
        )

    return datos


# ==========================================================
# GENERADOR DE AUDIO PROCEDURAL
# ==========================================================

SAMPLE_RATE = 44100


def nota_midi(nota):

    return 440 * (
        2 ** (
            (nota - 69) / 12
        )
    )


def onda(
    frecuencia,
    duracion,
    volumen=0.15
):

    cantidad = int(
        SAMPLE_RATE * duracion
    )

    t = (
        list(
            range(cantidad)
        )
    )

    datos = []

    for i in t:

        tiempo = (
            i / SAMPLE_RATE
        )

        envolvente = min(
            1,
            tiempo * 20
        )

        salida = (
            math.sin(
                2 *
                math.pi *
                frecuencia *
                tiempo
            )
            *
            volumen
            *
            envolvente
        )

        datos.append(
            salida
        )

    return datos


def crear_instrumental(
    bpm,
    compases=16
):

    beat = 60 / bpm

    duracion = (
        beat *
        4 *
        compases
    )

    cantidad = int(
        SAMPLE_RATE *
        duracion
    )

    audio = [
        0.0
    ] * cantidad

    progresion = [
        60,
        55,
        57,
        53
    ]

    for compas in range(
        compases
    ):

        raiz = progresion[
            compas % 4
        ]

        inicio = int(
            compas *
            beat *
            4 *
            SAMPLE_RATE
        )

        for nota in [
            raiz,
            raiz + 4,
            raiz + 7
        ]:

            sonido = onda(
                nota_midi(nota),
                beat * 3.5,
                0.035
            )

            for i, valor in enumerate(
                sonido
            ):

                posicion = (
                    inicio + i
                )

                if posicion < cantidad:

                    audio[
                        posicion
                    ] += valor

        # Bajo

        bajo = onda(
            nota_midi(
                raiz - 12
            ),
            beat * 0.8,
            0.10
        )

        for repeticion in [
            0,
            2
        ]:

            inicio_bajo = (
                inicio
                +
                int(
                    repeticion *
                    beat *
                    SAMPLE_RATE
                )
            )

            for i, valor in enumerate(
                bajo
            ):

                posicion = (
                    inicio_bajo + i
                )

                if posicion < cantidad:

                    audio[
                        posicion
                    ] += valor

    # Normalización

    maximo = max(
        abs(x)
        for x in audio
    ) or 1

    audio = [
        x / maximo * 0.85
        for x in audio
    ]

    # WAV

    memoria = io.BytesIO()

    with wave.open(
        memoria,
        "wb"
    ) as archivo:

        archivo.setnchannels(1)

        archivo.setsampwidth(2)

        archivo.setframerate(
            SAMPLE_RATE
        )

        datos = bytearray()

        for x in audio:

            entero = int(
                max(
                    -1,
                    min(
                        1,
                        x
                    )
                )
                * 32767
            )

            datos += entero.to_bytes(
                2,
                byteorder="little",
                signed=True
            )

        archivo.writeframes(
            datos
        )

    return memoria.getvalue()


# ==========================================================
# PROMPT MUSICAL
# ==========================================================

def prompt_musical(
    titulo,
    genero,
    tema,
    bpm,
    intensidad
):

    return f"""
CREATE A PROFESSIONAL {genero.upper()} SONG.

TITLE:
{titulo}

THEME:
{tema}

TEMPO:
{bpm} BPM

INTENSITY:
{intensidad}/100

STRUCTURE:

INTRO
VERSE 1
PRE-CHORUS
CHORUS
VERSE 2
BRIDGE
FINAL CHORUS
OUTRO

PRODUCTION:

Professional drums.
Deep controlled bass.
Clear harmonic foundation.
Strong emotional dynamics.
Modern arrangement.
Wide stereo image.
Powerful transitions.
Memorable chorus.
Professional vocal space.

The arrangement must evolve progressively
instead of staying at one energy level.
"""


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚙️ OMEGA CONTROL")

modelo = st.sidebar.selectbox(
    "🤖 Modelo local",
    MODELOS
)

profundidad = st.sidebar.slider(
    "🧠 Profundidad",
    1,
    100,
    95
)

atrevimiento = st.sidebar.slider(
    "🚀 Exploración",
    1,
    100,
    95
)

if ollama_disponible():

    st.sidebar.success(
        "🟢 CEREBRO LOCAL ACTIVO"
    )

else:

    st.sidebar.warning(
        "🟡 CEREBRO LOCAL NO DETECTADO"
    )


# ==========================================================
# INTERFAZ
# ==========================================================

st.markdown(
    '<div class="omega-title">'
    '🧠 CEREBRO OMEGA'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="omega-subtitle">'
    'Laboratorio interdisciplinario experimental'
    '</div>',
    unsafe_allow_html=True
)


tabs = st.tabs(
    [
        "🌌 OMEGA",
        "🧬 EVOLUCIÓN",
        "💥 MUTACIÓN",
        "🎵 MÚSICA",
        "🔬 LABORATORIO",
        "💾 MEMORIA"
    ]
)


# ==========================================================
# OMEGA
# ==========================================================

with tabs[0]:

    st.header(
        "🌌 Director OMEGA"
    )

    objetivo = st.text_area(
        "¿Qué quieres descubrir, crear o resolver?",
        "Crear una canción worship completamente nueva que conecte fe, evolución, conciencia y existencia."
    )

    contexto = st.text_area(
        "Contexto adicional",
        "Quiero explorar ciencia, biología, genética, evolución, filosofía, teología y simbolismo."
    )

    if st.button(
        "🚀 ACTIVAR OMEGA",
        use_container_width=True
    ):

        with st.spinner(
            "OMEGA está razonando..."
        ):

            respuesta = director_omega(
                objetivo,
                contexto,
                modelo,
                profundidad,
                atrevimiento
            )

        st.session_state.respuesta = respuesta

        guardar_memoria(
            "exploracion",
            respuesta
        )

    if st.session_state.respuesta:

        st.text_area(
            "Resultado",
            st.session_state.respuesta,
            height=700
        )


# ==========================================================
# EVOLUCIÓN
# ==========================================================

with tabs[1]:

    st.header(
        "🧬 Laboratorio Evolutivo"
    )

    generaciones = st.slider(
        "Generaciones",
        10,
        500,
        100
    )

    poblacion = st.slider(
        "Población",
        20,
        5000,
        500
    )

    seleccion = st.slider(
        "Ventaja selectiva",
        0.001,
        0.5,
        0.05
    )

    mutacion = st.slider(
        "Mutación",
        0.0,
        0.2,
        0.02
    )

    if st.button(
        "🧬 EJECUTAR SIMULACIÓN"
    ):

        datos = evolucion_simulada(
            generaciones,
            poblacion,
            seleccion,
            mutacion
        )

        st.session_state.experimentos.append(
            {
                "tipo":
                    "evolución",

                "fecha":
                    datetime.now().isoformat(),

                "datos":
                    datos
            }
        )

        st.line_chart(
            [
                x["Frecuencia"]
                for x in datos
            ]
        )

        st.success(
            "Simulación terminada."
        )


# ==========================================================
# MUTACIÓN
# ==========================================================

with tabs[2]:

    st.header(
        "💥 Generador de posibilidades"
    )

    idea = st.text_area(
        "Idea",
        "Una IA que genere canciones completas."
    )

    cantidad = st.slider(
        "Número de variantes",
        2,
        50,
        10
    )

    if st.button(
        "💥 MUTAR IDEA"
    ):

        resultado = mutar_idea(
            idea,
            cantidad
        )

        st.text_area(
            "Variantes",
            resultado,
            height=600
        )


# ==========================================================
# MÚSICA
# ==========================================================

with tabs[3]:

    st.header(
        "🎵 Estudio Musical"
    )

    titulo = st.text_input(
        "Título",
        "Un Verdadero Adorador"
    )

    genero = st.selectbox(
        "Género",
        [
            "Worship",
            "Rap",
            "Trap",
            "Hip Hop",
            "Dembow",
            "Cinemático"
        ]
    )

    tema = st.text_area(
        "Tema",
        "Volver a Dios después de tocar fondo."
    )

    bpm = st.slider(
        "BPM",
        50,
        180,
        76
    )

    intensidad = st.slider(
        "Intensidad",
        1,
        100,
        90
    )

    if st.button(
        "🎵 CREAR MOTOR MUSICAL",
        use_container_width=True
    ):

        prompt = prompt_musical(
            titulo,
            genero,
            tema,
            bpm,
            intensidad
        )

        st.session_state.ultimo_prompt = prompt

        audio = crear_instrumental(
            bpm
        )

        st.session_state.audio = audio

        st.text_area(
            "Prompt maestro",
            prompt,
            height=350
        )

    if st.session_state.audio:

        st.audio(
            st.session_state.audio,
            format="audio/wav"
        )

        st.download_button(
            "⬇️ DESCARGAR INSTRUMENTAL WAV",
            st.session_state.audio,
            file_name=
                limpiar_nombre(
                    titulo
                ) + ".wav",
            mime="audio/wav"
        )


# ==========================================================
# LABORATORIO
# ==========================================================

with tabs[4]:

    st.header(
        "🔬 Laboratorio de hipótesis"
    )

    pregunta = st.text_area(
        "Pregunta",
        "¿Cómo podría estudiarse el origen de la complejidad?"
    )

    if st.button(
        "🔬 GENERAR EXPERIMENTO"
    ):

        prompt = f"""
Diseña un experimento intelectual/computacional
para investigar:

{pregunta}

Incluye:

1. Hipótesis.
2. Variables.
3. Datos necesarios.
4. Método.
5. Predicciones.
6. Falsación.
7. Limitaciones.
8. Alternativas.
9. Qué resultado apoyaría la hipótesis.
10. Qué resultado la debilitaría.

No inventes evidencia.
"""

        resultado = preguntar_ia(
            prompt,
            modelo
        )

        guardar_memoria(
            "experimento",
            resultado
        )

        st.text_area(
            "Diseño experimental",
            resultado,
            height=650
        )


# ==========================================================
# MEMORIA
# ==========================================================

with tabs[5]:

    st.header(
        "💾 Memoria OMEGA"
    )

    st.metric(
        "Registros",
        len(
            st.session_state.memoria
        )
    )

    memoria_json = json.dumps(
        st.session_state.memoria,
        ensure_ascii=False,
        indent=2
    )

    st.download_button(
        "💾 EXPORTAR MEMORIA",
        memoria_json,
        file_name="omega_memoria.json",
        mime="application/json"
    )

    if st.session_state.memoria:

        for i, registro in enumerate(
            reversed(
                st.session_state.memoria
            )
        ):

            with st.expander(
                f"{i+1}. {registro['tipo']}"
            ):

                st.write(
                    registro["fecha"]
                )

                st.write(
                    registro["contenido"]
                )


#t ==========================================================
# PIE
# ==========================================================

st.divider()

st.caption(
    "🧠 CEREBRO OMEGA v2 — "
    "Lenguaje • Ciencia • Biología • Evolución • "
    "Filosofía • Teología • Simbolismo • Música"
        )
