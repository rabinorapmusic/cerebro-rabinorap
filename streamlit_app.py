# ============================================================
# 🧠 CEREBRO OMEGA ∞
# ============================================================
# Director multi-IA
#
# OMEGA:
#   recibe → analiza → delega → compara → critica
#   → sintetiza → decide → recuerda → vuelve a trabajar
#
# No necesita core/.
# Los módulos existentes permanecen independientes.
# ============================================================

import os
import json
import re
import importlib
from datetime import datetime

import requests
import streamlit as st


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(
    BASE_DIR,
    "omega_data"
)

MEMORY_FILE = os.path.join(
    DATA_DIR,
    "memoria.json"
)

EXPERIENCE_FILE = os.path.join(
    DATA_DIR,
    "experiencias.json"
)

os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================
# API
# ============================================================

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
)

MODEL = os.getenv(
    "OMEGA_MODEL",
    "gemini-2.5-flash"
)

API_URL = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/"
    + MODEL
    + ":generateContent"
)


# ============================================================
# DISEÑO
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(0,255,130,.10),
            transparent 35%
        ),
        radial-gradient(
            circle at 50% 110%,
            rgba(0,255,130,.06),
            transparent 40%
        ),
        #020805;

    color: #d5ffe4;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

h1, h2, h3 {
    font-family:
        "Courier New",
        monospace !important;

    color: #00ff88 !important;
}

h1 {
    text-align: center;

    letter-spacing: 3px;

    text-shadow:
        0 0 8px #00ff88,
        0 0 22px rgba(0,255,136,.8);
}

.omega-title {
    text-align: center;

    font-family:
        "Courier New",
        monospace;

    font-size: 42px;

    font-weight: bold;

    letter-spacing: 4px;

    color: #eafff1;

    margin-top: 10px;

    text-shadow:
        0 0 8px rgba(255,255,255,.25);
}

.omega-infinity {
    color: #00ff88;

    font-size: 62px;

    text-shadow:
        0 0 8px #00ff88,
        0 0 22px #00ff88,
        0 0 50px rgba(0,255,136,.7);
}

.omega-line {
    height: 1px;

    margin: 18px 0 25px 0;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00ff88,
            transparent
        );

    box-shadow:
        0 0 12px #00ff88;
}

.omega-panel {
    background:
        rgba(0,20,10,.72);

    border:
        1px solid rgba(0,255,136,.25);

    border-radius: 15px;

    padding: 18px;

    box-shadow:
        inset 0 0 25px
        rgba(0,255,136,.025),

        0 0 20px
        rgba(0,255,136,.06);
}

.omega-active {
    text-align: center;

    color: #00ff88;

    font-family:
        "Courier New",
        monospace;

    letter-spacing: 3px;

    text-shadow:
        0 0 10px #00ff88;
}

[data-testid="stMetric"] {
    background:
        rgba(0,25,12,.75);

    border:
        1px solid rgba(0,255,136,.25);

    border-radius: 12px;
}

[data-testid="stMetricValue"] {
    color: #00ff88 !important;

    text-shadow:
        0 0 8px #00ff88;

    font-family:
        "Courier New",
        monospace;
}

textarea {
    background:
        #010b05 !important;

    color:
        #baffd0 !important;

    border:
        1px solid rgba(0,255,136,.45) !important;

    border-radius:
        12px !important;

    font-family:
        "Courier New",
        monospace !important;
}

textarea:focus {
    border:
        1px solid #00ff88 !important;

    box-shadow:
        0 0 20px
        rgba(0,255,136,.25) !important;
}

.stButton > button {
    background:
        linear-gradient(
            90deg,
            #002d15,
            #005c2d,
            #002d15
        ) !important;

    color:
        #00ff88 !important;

    border:
        1px solid #00ff88 !important;

    border-radius:
        10px !important;

    font-family:
        "Courier New",
        monospace !important;

    font-weight:
        bold !important;

    letter-spacing:
        1px;

    box-shadow:
        0 0 12px
        rgba(0,255,136,.15);
}

.stButton > button:hover {
    background:
        #00ff88 !important;

    color:
        #001208 !important;

    box-shadow:
        0 0 25px
        rgba(0,255,136,.7);
}

[data-testid="stExpander"] {
    background:
        rgba(0,18,9,.70);

    border:
        1px solid
        rgba(0,255,136,.20);

    border-radius:
        12px;
}

hr {
    border:
        none !important;

    height:
        1px !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00ff88,
            transparent
        ) !important;
}

code {
    color:
        #00ff88 !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# CABECERA
# ============================================================

st.markdown(
    """
<div class="omega-title">
    🧠 CEREBRO OMEGA
    <span class="omega-infinity">∞</span>
</div>

<div class="omega-line"></div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# JSON
# ============================================================

def cargar_json(path, default):

    try:

        if not os.path.exists(path):
            return default

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except Exception:
        return default


def guardar_json(path, data):

    try:

        temporal = path + ".tmp"

        with open(
            temporal,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                data,
                archivo,
                ensure_ascii=False,
                indent=2,
            )

        os.replace(
            temporal,
            path
        )

        return True

    except Exception:
        return False


# ============================================================
# MEMORIA
# ============================================================

def cargar_memoria():
    return cargar_json(
        MEMORY_FILE,
        []
    )


def guardar_memoria(item):

    memoria = cargar_memoria()

    memoria.append(item)

    if len(memoria) > 5000:
        memoria = memoria[-4500:]

    guardar_json(
        MEMORY_FILE,
        memoria
    )


def guardar_recuerdo(
    contenido,
    tipo="conocimiento",
    importancia=5
):

    memoria = cargar_memoria()

    nuevo = {
        "id": len(memoria) + 1,
        "fecha": datetime.now().isoformat(),
        "tipo": tipo,
        "importancia": importancia,
        "contenido": contenido,
    }

    memoria.append(nuevo)

    if len(memoria) > 5000:

        importantes = sorted(
            memoria,
            key=lambda x: (
                x.get(
                    "importancia",
                    0
                ),
                x.get(
                    "id",
                    0
                )
            ),
            reverse=True,
        )

        memoria = importantes[:4500]

    guardar_json(
        MEMORY_FILE,
        memoria
    )


# ============================================================
# EXPERIENCIAS
# ============================================================

def cargar_experiencias():

    return cargar_json(
        EXPERIENCE_FILE,
        []
    )


def guardar_experiencia(
    orden,
    resultado,
    ciclo
):

    experiencias = cargar_experiencias()

    experiencias.append(
        {
            "id": len(experiencias) + 1,
            "fecha": datetime.now().isoformat(),
            "ciclo": ciclo,
            "orden": orden,
            "resultado": resultado,
        }
    )

    if len(experiencias) > 3000:
        experiencias = experiencias[-2500:]

    guardar_json(
        EXPERIENCE_FILE,
        experiencias
    )


# ============================================================
# MEMORIA RELEVANTE
# ============================================================

def buscar_memoria(texto, limite=12):

    memoria = cargar_memoria()

    if not memoria:
        return []

    palabras = set(
        palabra.lower()
        for palabra in re.findall(
            r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+",
            texto
        )
        if len(palabra) >= 4
    )

    resultados = []

    for item in memoria:

        contenido = str(
            item.get(
                "contenido",
                ""
            )
        )

        contenido_lower = contenido.lower()

        coincidencias = sum(
            1
            for palabra in palabras
            if palabra in contenido_lower
        )

        if coincidencias:

            puntuacion = (
                coincidencias * 10
                + item.get(
                    "importancia",
                    0
                )
            )

            resultados.append(
                (
                    puntuacion,
                    item
                )
            )

    resultados.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        item
        for _, item in resultados[:limite]
    ]


def memoria_como_texto(texto):

    recuerdos = buscar_memoria(
        texto
    )

    if not recuerdos:
        return "SIN RECUERDOS RELEVANTES."

    partes = []

    for recuerdo in recuerdos:

        partes.append(
            f"- {recuerdo.get('contenido', '')}"
        )

    return "\n".join(partes)


# ============================================================
# IA REAL
# ============================================================

def llamar_ia(
    rol,
    tarea,
    contexto=""
):

    if not GOOGLE_API_KEY:

        return {
            "ok": False,
            "texto": (
                "GOOGLE_API_KEY no está configurada."
            )
        }

    instrucciones = f"""
Eres una IA especializada que trabaja DENTRO de
CEREBRO OMEGA ∞.

ROL:
{rol}

TAREA:
{tarea}

CONTEXTO:
{contexto}

REGLAS:
- Haz el trabajo solicitado.
- No describas lo que deberías hacer.
- No digas simplemente que vas a investigar.
- Entrega directamente el resultado de tu trabajo.
- No inventes información.
- Distingue hechos, inferencias e hipótesis.
- Si no tienes suficiente información, indícalo.
- Tu resultado será utilizado por otra IA.
"""

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": instrucciones
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.35,
            "topP": 0.9,
            "maxOutputTokens": 5000,
        }
    }

    try:

        respuesta = requests.post(
            API_URL,
            params={
                "key": GOOGLE_API_KEY
            },
            json=payload,
            timeout=120
        )

        if respuesta.status_code != 200:

            return {
                "ok": False,
                "texto": (
                    "Error de IA: "
                    + str(
                        respuesta.status_code
                    )
                    + "\n"
                    + respuesta.text[:1000]
                )
            }

        datos = respuesta.json()

        candidatos = datos.get(
            "candidates",
            []
        )

        if not candidatos:

            return {
                "ok": False,
                "texto": "La IA no produjo una respuesta."
            }

        partes = (
            candidatos[0]
            .get("content", {})
            .get("parts", [])
        )

        texto = "\n".join(
            parte.get(
                "text",
                ""
            )
            for parte in partes
        ).strip()

        if not texto:

            return {
                "ok": False,
                "texto": "La IA devolvió una respuesta vacía."
            }

        return {
            "ok": True,
            "texto": texto
        }

    except Exception as error:

        return {
            "ok": False,
            "texto": f"Error de conexión: {error}"
        }


# ============================================================
# ROLES REALES
# ============================================================

ROL_DIRECTOR = """
Diriges el trabajo completo.

Analiza la misión y determina:
- qué debe resolverse,
- qué información hace falta,
- qué especialistas deben intervenir,
- qué preguntas deben contestarse.

No entregues una lista de instrucciones vacía.
Realiza el análisis inicial.
"""

ROL_INVESTIGADOR = """
Eres el investigador.

Analiza la misión utilizando el conocimiento disponible.
Encuentra hechos, relaciones, antecedentes, posibilidades
y preguntas sin resolver.

Produce contenido útil y concreto.
"""

ROL_MEMORIA = """
Eres el especialista de memoria.

Compara la misión con los recuerdos proporcionados.
Extrae conexiones relevantes.
Detecta conocimientos anteriores que puedan cambiar
el análisis actual.
"""

ROL_RAZONADOR = """
Eres el razonador.

Combina la investigación y la memoria.
Construye deducciones y explicaciones.
Separa claramente hechos de hipótesis.
Busca relaciones que no sean evidentes.
"""

ROL_CRITICO = """
Eres el crítico.

Ataca las conclusiones del razonador.
Busca errores, contradicciones, información faltante,
suposiciones débiles y explicaciones alternativas.

Tu misión es intentar encontrar dónde podría estar equivocado.
"""

ROL_SINTESIS = """
Eres el sintetizador.

Combina todos los resultados.
Resuelve contradicciones cuando la evidencia lo permita.
Conserva las incertidumbres importantes.

Produce una conclusión estructurada.
"""

ROL_DECISOR = """
Eres el decisor final.

Utiliza toda la evidencia recibida.
Determina la respuesta más sólida disponible.

Entrega:
1. conclusión,
2. evidencia principal,
3. incertidumbres,
4. alternativas,
5. siguiente acción recomendada.

No inventes certeza.
"""


# ============================================================
# MOTOR CENTRAL OMEGA
# ============================================================

def ejecutar_omega(mision):

    if "ciclos" not in st.session_state:
        st.session_state.ciclos = 0

    st.session_state.ciclos += 1

    ciclo = st.session_state.ciclos

    # --------------------------------------------------------
    # MEMORIA
    # --------------------------------------------------------

    contexto_memoria = memoria_como_texto(
        mision
    )

    # --------------------------------------------------------
    # DIRECTOR
    # --------------------------------------------------------

    director = llamar_ia(
        ROL_DIRECTOR,
        mision,
        contexto_memoria
    )

    if not director["ok"]:
        return director

    # --------------------------------------------------------
    # INVESTIGADOR
    # --------------------------------------------------------

    investigador = llamar_ia(
        ROL_INVESTIGADOR,
        mision,
        director["texto"]
    )

    if not investigador["ok"]:
        return investigador

    # --------------------------------------------------------
    # MEMORIA
    # --------------------------------------------------------

    memoria = llamar_ia(
        ROL_MEMORIA,
        mision,
        contexto_memoria
        + "\n\nDIRECTOR:\n"
        + director["texto"]
    )

    if not memoria["ok"]:
        return memoria

    # --------------------------------------------------------
    # RAZONAMIENTO
    # --------------------------------------------------------

    razonador = llamar_ia(
        ROL_RAZONADOR,
        mision,
        (
            "DIRECTOR:\n"
            + director["texto"]
            + "\n\nINVESTIGADOR:\n"
            + investigador["texto"]
            + "\n\nMEMORIA:\n"
            + memoria["texto"]
        )
    )

    if not razonador["ok"]:
        return razonador

    # --------------------------------------------------------
    # CRÍTICA
    # --------------------------------------------------------

    critico = llamar_ia(
        ROL_CRITICO,
        mision,
        (
            "INVESTIGACIÓN:\n"
            + investigador["texto"]
            + "\n\nRAZONAMIENTO:\n"
            + razonador["texto"]
        )
    )

    if not critico["ok"]:
        return critico

    # --------------------------------------------------------
    # SÍNTESIS
    # --------------------------------------------------------

    sintesis = llamar_ia(
        ROL_SINTESIS,
        mision,
        (
            "DIRECTOR:\n"
            + director["texto"]
            + "\n\nINVESTIGADOR:\n"
            + investigador["texto"]
            + "\n\nMEMORIA:\n"
            + memoria["texto"]
            + "\n\nRAZONADOR:\n"
            + razonador["texto"]
            + "\n\nCRÍTICO:\n"
            + critico["texto"]
        )
    )

    if not sintesis["ok"]:
        return sintesis

    # --------------------------------------------------------
    # DECISIÓN
    # --------------------------------------------------------

    decisor = llamar_ia(
        ROL_DECISOR,
        mision,
        sintesis["texto"]
        + "\n\nCRÍTICA:\n"
        + critico["texto"]
    )

    if not decisor["ok"]:
        return decisor

    resultado = decisor["texto"]

    # --------------------------------------------------------
    # APRENDIZAJE REAL
    # --------------------------------------------------------

    guardar_recuerdo(
        (
            "MISIÓN:\n"
            + mision
            + "\n\nRESULTADO:\n"
            + resultado
        ),
        tipo="experiencia",
        importancia=8
    )

    guardar_experiencia(
        mision,
        resultado,
        ciclo
    )

    return {
        "ok": True,
        "ciclo": ciclo,
        "director": director["texto"],
        "investigador": investigador["texto"],
        "memoria": memoria["texto"],
        "razonador": razonador["texto"],
        "critico": critico["texto"],
        "sintesis": sintesis["texto"],
        "resultado": resultado,
    }


# ============================================================
# ESTADO
# ============================================================

if "ciclos" not in st.session_state:
    st.session_state.ciclos = 0

if "resultado_actual" not in st.session_state:
    st.session_state.resultado_actual = None

memoria_actual = cargar_memoria()
experiencias_actuales = cargar_experiencias()


# ============================================================
# INDICADORES
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "ESTADO",
        "🟢 ACTIVO"
    )

with c2:
    st.metric(
        "CONOCIMIENTO",
        len(memoria_actual)
    )

with c3:
    st.metric(
        "EXPERIENCIAS",
        len(experiencias_actuales)
    )

with c4:
    st.metric(
        "CICLOS ∞",
        st.session_state.ciclos
    )


# ============================================================
# CENTRO DE PENSAMIENTO
# ============================================================

st.markdown(
    '<div class="omega-line"></div>',
    unsafe_allow_html=True
)

st.header(
    "🧠 CENTRO DE PENSAMIENTO"
)

mision = st.text_area(
    "Dale una misión a CEREBRO OMEGA:",
    height=150,
    placeholder=(
        "Escribe aquí lo que quieres que CEREBRO OMEGA haga."
    )
)


if st.button(
    "⚡ EJECUTAR CICLO",
    type="primary",
    use_container_width=True
):

    if not GOOGLE_API_KEY:

        st.error(
            "CEREBRO OMEGA no tiene conectada la IA."
        )

        st.info(
            "Configura GOOGLE_API_KEY en los Secrets "
            "de tu aplicación."
        )

    elif not mision.strip():

        st.warning(
            "Escribe una misión."
        )

    else:

        with st.status(
            "🧠 CEREBRO OMEGA está trabajando...",
            expanded=True
        ) as estado:

            st.write(
                "Procesando misión..."
            )

            resultado = ejecutar_omega(
                mision.strip()
            )

            if resultado.get("ok"):

                estado.update(
                    label="🧠 CEREBRO OMEGA completó el ciclo",
                    state="complete",
                    expanded=False
                )

            else:

                estado.update(
                    label="CEREBRO OMEGA encontró un error",
                    state="error",
                    expanded=True
                )

        st.session_state.resultado_actual = resultado


# ============================================================
# RESULTADO
# ============================================================

resultado = st.session_state.resultado_actual

if resultado:

    if resultado.get("ok"):

        st.markdown(
            '<div class="omega-line"></div>',
            unsafe_allow_html=True
        )

        st.header(
            "♾️ RESULTADO"
        )

        st.markdown(
            resultado["resultado"]
        )

        st.caption(
            f"Ciclo {resultado['ciclo']}"
        )

        st.markdown(
            '<div class="omega-line"></div>',
            unsafe_allow_html=True
        )

        st.header(
            "🧠 PROCESO DE CEREBRO OMEGA"
        )

        with st.expander(
            "DIRECTOR"
        ):
            st.write(
                resultado["director"]
            )

        with st.expander(
            "INVESTIGACIÓN"
        ):
            st.write(
                resultado["investigador"]
            )

        with st.expander(
            "MEMORIA"
        ):
            st.write(
                resultado["memoria"]
            )

        with st.expander(
            "RAZONAMIENTO"
        ):
            st.write(
                resultado["razonador"]
            )

        with st.expander(
            "CRÍTICA"
        ):
            st.write(
                resultado["critico"]
            )

        with st.expander(
            "SÍNTESIS"
        ):
            st.write(
                resultado["sintesis"]
            )

    else:

        st.error(
            resultado.get(
                "texto",
                "Error desconocido."
            )
        )


# ============================================================
# MEMORIA
# ============================================================

st.markdown(
    '<div class="omega-line"></div>',
    unsafe_allow_html=True
)

st.header(
    "💾 MEMORIA"
)

if memoria_actual:

    for item in reversed(
        memoria_actual[-15:]
    ):

        with st.expander(
            f"#{item.get('id')} · "
            f"{item.get('tipo')} · "
            f"{item.get('fecha')}"
        ):

            st.write(
                item.get(
                    "contenido",
                    ""
                )
            )

else:

    st.info(
        "La memoria está vacía."
    )


# ============================================================
# EXPERIENCIAS
# ============================================================

st.header(
    "🧬 EXPERIENCIAS"
)

if experiencias_actuales:

    for item in reversed(
        experiencias_actuales[-10:]
    ):

        with st.expander(
            f"Ciclo {item.get('ciclo')} · "
            f"{item.get('fecha')}"
        ):

            st.write(
                "**Misión**"
            )

            st.write(
                item.get(
                    "orden",
                    ""
                )
            )

            st.write(
                "**Resultado**"
            )

            st.write(
                item.get(
                    "resultado",
                    ""
                )
            )

else:

    st.info(
        "Todavía no hay experiencias."
    )


# ============================================================
# DIAGNÓSTICO
# ============================================================

st.header(
    "🔍 DIAGNÓSTICO"
)

if GOOGLE_API_KEY:

    st.success(
        f"IA conectada · modelo {MODEL}"
    )

else:

    st.error(
        "IA desconectada"
    )


# ============================================================
# MÓDULOS EXISTENTES
# ============================================================

st.header(
    "⚙️ ARQUITECTURA"
)

modules_dir = os.path.join(
    BASE_DIR,
    "modules"
)

if os.path.isdir(modules_dir):

    archivos = sorted(
        archivo
        for archivo in os.listdir(modules_dir)
        if archivo.endswith(".py")
        and not archivo.startswith("_")
    )

    if archivos:

        for archivo in archivos:

            nombre = archivo[:-3]

            try:

                modulo = importlib.import_module(
                    f"modules.{nombre}"
                )

                st.success(
                    f"🟢 {nombre} — CARGADO"
                )

            except Exception as error:

                st.error(
                    f"🔴 {nombre} — ERROR: {error}"
                )

    else:

        st.info(
            "No hay módulos adicionales."
        )

else:

    st.info(
        "La carpeta modules/ todavía no existe."
    )


# ============================================================
# PIE
# ============================================================

st.markdown(
    '<div class="omega-line"></div>',
    unsafe_allow_html=True
)

st.markdown(
    """
<div style="
text-align:center;
font-family:monospace;
color:#00ff88;
font-size:20px;
text-shadow:0 0 10px #00ff88;
">
🧠 CEREBRO OMEGA
<span style="
color:#00ff88;
font-size:30px;
text-shadow:
0 0 8px #00ff88,
0 0 20px #00ff88,
0 0 40px #00ff88;
">∞</span>
</div>
""",
    unsafe_allow_html=True
)
