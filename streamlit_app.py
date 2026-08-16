import streamlit as st
import json
from datetime import datetime

# ============================================================
# 🧠 CEREBRO RABINO PRO
# Generador creativo para música, letras y conceptos
# ============================================================

st.set_page_config(
    page_title="CEREBRO RABINO PRO",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 5px;
}
.subtitle {
    text-align: center;
    opacity: 0.75;
    margin-bottom: 25px;
}
.box {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,.25);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# TÍTULO
# ============================================================

st.markdown(
    '<div class="main-title">🧠 CEREBRO RABINO PRO</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Motor creativo para música, conceptos, letras y producción</div>',
    unsafe_allow_html=True
)

# ============================================================
# FUNCIONES
# ============================================================

def generar_concepto(titulo, genero, tema, intensidad, bpm, mood, objetivo):

    estructura = {
        "Intro": "Entrada corta y poderosa que presenta el concepto.",
        "Verso 1": "Presenta el conflicto, historia o mensaje.",
        "Pre-Coro": "Aumenta la tensión emocional.",
        "Coro": "Frase principal fácil de recordar.",
        "Verso 2": "Profundiza el mensaje.",
        "Puente": "Cambio emocional o revelación.",
        "Coro Final": "Máxima intensidad y repetición del mensaje."
    }

    concepto = f"""
🧠 CONCEPTO CENTRAL
━━━━━━━━━━━━━━━━━━━━

Título: {titulo}
Género: {genero}
Tema: {tema}
Intensidad: {intensidad}/100
BPM: {bpm}
Mood: {mood}
Objetivo: {objetivo}

🎯 IDEA PRINCIPAL
La canción debe desarrollar el tema "{tema}" desde una perspectiva
fuerte, memorable y emocional, utilizando imágenes, contrastes,
frases contundentes y un coro fácil de recordar.

🔥 DIRECCIÓN ARTÍSTICA
• Intro: crear curiosidad inmediatamente.
• Versos: contar la historia y desarrollar el mensaje.
• Coro: concentrar la idea principal.
• Puente: elevar la emoción.
• Final: dejar una frase memorable.

🎼 ESTRUCTURA
"""

    for parte, descripcion in estructura.items():
        concepto += f"\n{parte}: {descripcion}"

    concepto += f"""

⚡ INTENSIDAD
Nivel: {intensidad}/100

La producción debe sentirse:
• Energética
• Cinemática
• Emocional
• Dinámica
• Profesional

🎧 PROMPT DE PRODUCCIÓN

{generar_prompt(titulo, genero, tema, intensidad, bpm, mood)}

"""

    return concepto


def generar_prompt(titulo, genero, tema, intensidad, bpm, mood):

    return f"""
Professional {genero} production, {bpm} BPM,
{mood} atmosphere, powerful emotional dynamics,
modern professional mix, strong drums, deep bass,
clear vocal space, cinematic transitions,
dynamic arrangement, memorable chorus,
high-impact intro, powerful bridge,
radio-ready production.

Song title: {titulo}
Main theme: {tema}
Intensity: {intensidad}/100.

Create a professional arrangement with clear sections,
strong emotional progression and a memorable climax.
"""


def generar_estructura(genero):

    estructuras = {
        "Worship": [
            "Intro",
            "Verso 1",
            "Pre-Coro",
            "Coro",
            "Verso 2",
            "Puente",
            "Coro Final",
            "Outro"
        ],
        "Rap": [
            "Intro",
            "Verso 1",
            "Coro",
            "Verso 2",
            "Puente",
            "Verso 3",
            "Coro Final"
        ],
        "Trap": [
            "Intro",
            "Hook",
            "Verso 1",
            "Hook",
            "Verso 2",
            "Bridge",
            "Hook Final"
        ],
        "Dembow": [
            "Intro",
            "Coro",
            "Verso",
            "Coro",
            "Break",
            "Coro Final"
        ],
        "Hip Hop": [
            "Intro",
            "Verso 1",
            "Hook",
            "Verso 2",
            "Bridge",
            "Verso 3",
            "Hook Final"
        ]
    }

    return estructuras.get(genero, estructuras["Rap"])


def bpm_recomendado(genero):

    valores = {
        "Worship": "68–82 BPM",
        "Rap": "82–96 BPM",
        "Trap": "130–150 BPM",
        "Dembow": "100–115 BPM",
        "Hip Hop": "85–100 BPM"
    }

    return valores.get(genero, "90–100 BPM")


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ CONFIGURACIÓN")

genero = st.sidebar.selectbox(
    "🎵 Género",
    [
        "Worship",
        "Rap",
        "Trap",
        "Dembow",
        "Hip Hop"
    ]
)

titulo = st.sidebar.text_input(
    "🏷️ Título",
    "Un Verdadero Adorador"
)

tema = st.sidebar.text_area(
    "🎯 Tema principal",
    "Una persona que adora a Dios de corazón y no solamente por apariencia."
)

mood = st.sidebar.selectbox(
    "🎭 Mood",
    [
        "Espiritual",
        "Épico",
        "Emocional",
        "Oscuro",
        "Esperanzador",
        "Triunfal",
        "Introspectivo",
        "Agresivo"
    ]
)

intensidad = st.sidebar.slider(
    "🔥 Intensidad",
    1,
    100,
    85
)

bpm_default = {
    "Worship": 76,
    "Rap": 90,
    "Trap": 140,
    "Dembow": 108,
    "Hip Hop": 92
}

bpm = st.sidebar.number_input(
    "🥁 BPM",
    min_value=50,
    max_value=200,
    value=bpm_default[genero]
)

objetivo = st.sidebar.selectbox(
    "🎯 Objetivo",
    [
        "Impactar emocionalmente",
        "Crear un himno",
        "Viralizar",
        "Predicar un mensaje",
        "Motivar",
        "Contar una historia",
        "Crear una canción comercial"
    ]
)

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧠 CEREBRO",
    "🎼 ESTRUCTURA",
    "🔥 INTENSIDAD",
    "🎧 PROMPT",
    "💾 PROYECTO"
])

# ============================================================
# TAB 1
# ============================================================

with tab1:

    st.header("🧠 Generador de Conceptos")

    st.write(
        "Configura la canción y deja que CEREBRO construya "
        "la dirección creativa."
    )

    if st.button(
        "🚀 ACTIVAR CEREBRO",
        use_container_width=True
    ):

        resultado = generar_concepto(
            titulo,
            genero,
            tema,
            intensidad,
            bpm,
            mood,
            objetivo
        )

        st.session_state["resultado"] = resultado

    if "resultado" in st.session_state:

        st.text_area(
            "Resultado",
            st.session_state["resultado"],
            height=600
        )

        st.download_button(
            "⬇️ Descargar concepto",
            st.session_state["resultado"],
            file_name=f"{titulo.replace(' ', '_')}_concepto.txt",
            mime="text/plain"
        )


# ============================================================
# TAB 2
# ============================================================

with tab2:

    st.header("🎼 Arquitectura Musical")

    st.info(
        f"BPM recomendado para {genero}: "
        f"{bpm_recomendado(genero)}"
    )

    estructura = generar_estructura(genero)

    for i, parte in enumerate(estructura, 1):

        st.markdown(
            f"### {i}. {parte}"
        )

        if parte == "Intro":
            st.write(
                "Crear identidad sonora y captar atención desde los primeros segundos."
            )

        elif "Coro" in parte or "Hook" in parte:
            st.write(
                "Parte más memorable. Debe contener la frase central de la canción."
            )

        elif "Verso" in parte:
            st.write(
                "Desarrollar historia, mensaje, imágenes y rimas."
            )

        elif "Puente" in parte or "Bridge" in parte:
            st.write(
                "Cambiar la energía y preparar el momento de mayor impacto."
            )

        else:
            st.write(
                "Conectar musicalmente las diferentes secciones."
            )


# ============================================================
# TAB 3
# ============================================================

with tab3:

    st.header("🔥 Control de Intensidad")

    nivel = intensidad

    if nivel <= 25:
        descripcion = "🌱 Suave / íntima"

    elif nivel <= 50:
        descripcion = "🎵 Moderada"

    elif nivel <= 75:
        descripcion = "🔥 Potente"

    elif nivel <= 90:
        descripcion = "🚀 Muy potente"

    else:
        descripcion = "💥 Máxima intensidad"

    st.metric(
        "INTENSIDAD",
        f"{nivel}/100",
        descripcion
    )

    st.progress(nivel / 100)

    st.write("### Dirección")

    if nivel <= 40:
        st.write(
            "Usar instrumentos suaves, espacio vocal y dinámica controlada."
        )

    elif nivel <= 70:
        st.write(
            "Combinar partes íntimas con momentos de crecimiento."
        )

    elif nivel <= 90:
        st.write(
            "Baterías fuertes, bajos definidos, coros grandes y "
            "transiciones marcadas."
        )

    else:
        st.write(
            "Máxima energía: drums grandes, bajos profundos, "
            "capas instrumentales, coros masivos y climax cinematográfico."
        )


# ============================================================
# TAB 4
# ============================================================

with tab4:

    st.header("🎧 Prompt Profesional")

    prompt = generar_prompt(
        titulo,
        genero,
        tema,
        intensidad,
        bpm,
        mood
    )

    st.text_area(
        "Prompt",
        prompt,
        height=400
    )

    st.download_button(
        "⬇️ Descargar Prompt",
        prompt,
        file_name=f"{titulo.replace(' ', '_')}_prompt.txt",
        mime="text/plain"
    )


# ============================================================
# TAB 5
# ============================================================

with tab5:

    st.header("💾 Guardar Proyecto")

    proyecto = {
        "titulo": titulo,
        "genero": genero,
        "tema": tema,
        "mood": mood,
        "intensidad": intensidad,
        "bpm": bpm,
        "objetivo": objetivo,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    st.json(proyecto)

    archivo = json.dumps(
        proyecto,
        ensure_ascii=False,
        indent=4
    )

    st.download_button(
        "💾 GUARDAR PROYECTO",
        archivo,
        file_name=f"{titulo.replace(' ', '_')}_proyecto.json",
        mime="application/json",
        use_container_width=True
    )


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "🧠 CEREBRO RABINO PRO — Motor creativo musical"
)

st.caption(
    "Diseñado para desarrollar conceptos, estructuras y prompts "
    "para música profesional."
)
