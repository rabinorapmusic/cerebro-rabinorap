import os
import json
import re
import requests
import streamlit as st
from datetime import datetime
from pathlib import Path

# ============================================================
# CEREBRO OMEGA ∞
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide",
)

BASE = Path(__file__).parent
DATA = BASE / "omega_data"
DATA.mkdir(exist_ok=True)

MEMORIA = DATA / "memoria.json"
EXPERIENCIAS = DATA / "experiencias.json"

# ============================================================
# INTERFAZ
# ============================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 50% 0%,
        rgba(0,255,120,.12), transparent 35%),
        #010604;
    color:#d9ffe5;
}

header, footer, #MainMenu {
    visibility:hidden;
}

.omega {
    text-align:center;
    font-family:monospace;
    font-size:42px;
    font-weight:bold;
    letter-spacing:4px;
    color:#eafff0;
    text-shadow:0 0 12px rgba(255,255,255,.25);
}

.infinity {
    color:#00ff88;
    font-size:70px;
    text-shadow:
        0 0 8px #00ff88,
        0 0 25px #00ff88,
        0 0 55px rgba(0,255,136,.8);
}

.line {
    height:1px;
    margin:20px 0;
    background:linear-gradient(
        90deg,
        transparent,
        #00ff88,
        transparent
    );
    box-shadow:0 0 12px #00ff88;
}

.panel {
    background:rgba(0,20,9,.7);
    border:1px solid rgba(0,255,136,.28);
    border-radius:14px;
    padding:18px;
}

[data-testid="stMetric"] {
    background:rgba(0,25,12,.7);
    border:1px solid rgba(0,255,136,.25);
    border-radius:12px;
}

[data-testid="stMetricValue"] {
    color:#00ff88 !important;
    text-shadow:0 0 10px #00ff88;
}

.stButton>button {
    background:#003519 !important;
    color:#00ff88 !important;
    border:1px solid #00ff88 !important;
    border-radius:10px !important;
    font-family:monospace !important;
    font-weight:bold !important;
}

.stButton>button:hover {
    background:#00ff88 !important;
    color:#001507 !important;
    box-shadow:
        0 0 15px #00ff88,
        0 0 35px rgba(0,255,136,.7);
}

textarea {
    background:#010b05 !important;
    color:#baffd0 !important;
    border:1px solid #008f4d !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="omega">
    🧠 CEREBRO OMEGA
    <span class="infinity">∞</span>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

# ============================================================
# ARCHIVOS
# ============================================================

def cargar_archivo(path, defecto):
    try:
        if not path.exists():
            return defecto

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return defecto


def guardar_archivo(path, datos):
    temporal = path.with_suffix(".tmp")

    with open(temporal, "w", encoding="utf-8") as f:
        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=2
        )

    temporal.replace(path)


def memoria():
    return cargar_archivo(MEMORIA, [])


def experiencias():
    return cargar_archivo(EXPERIENCIAS, [])

# ============================================================
# BÚSQUEDA DE MEMORIA
# ============================================================

def buscar_memoria(pregunta, limite=10):

    datos = memoria()

    palabras = {
        x.lower()
        for x in re.findall(
            r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+",
            pregunta
        )
        if len(x) >= 4
    }

    encontrados = []

    for item in datos:

        texto = str(item.get("contenido", "")).lower()

        puntos = sum(
            1 for palabra in palabras
            if palabra in texto
        )

        if puntos:
            encontrados.append(
                (puntos, item)
            )

    encontrados.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        x[1]
        for x in encontrados[:limite]
    ]


# ============================================================
# GUARDAR APRENDIZAJE
# ============================================================

def aprender(pregunta, respuesta):

    datos = memoria()

    datos.append({
        "fecha": datetime.now().isoformat(),
        "tipo": "experiencia",
        "contenido":
            f"ORDEN:\n{pregunta}\n\n"
            f"RESULTADO:\n{respuesta}"
    })

    if len(datos) > 3000:
        datos = datos[-2500:]

    guardar_archivo(
        MEMORIA,
        datos
    )


def registrar_experiencia(
    pregunta,
    respuesta,
    ciclo
):

    datos = experiencias()

    datos.append({
        "fecha": datetime.now().isoformat(),
        "ciclo": ciclo,
        "orden": pregunta,
        "resultado": respuesta
    })

    if len(datos) > 2000:
        datos = datos[-1800:]

    guardar_archivo(
        EXPERIENCIAS,
        datos
    )

# ============================================================
# IA
# ============================================================

def obtener_secreto(nombre):

    try:
        if nombre in st.secrets:
            return st.secrets[nombre]
    except Exception:
        pass

    return os.getenv(nombre, "")


API_KEY = obtener_secreto("GOOGLE_API_KEY")

MODELO = obtener_secreto(
    "OMEGA_MODEL"
) or "gemini-2.5-flash"


def llamar_ia(sistema, contenido):

    if not API_KEY:
        return None

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        f"{MODELO}:generateContent"
    )

    prompt = f"""
{sistema}

CEREBRO OMEGA ∞ está procesando esta misión:

{contenido}

No describas pasos futuros.
No digas simplemente qué deberías hacer.

HAZ EL TRABAJO.

Entrega información concreta, razonamiento,
conclusiones y resultados utilizables.
"""

    datos = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.35,
            "topP": 0.9,
            "maxOutputTokens": 6000
        }
    }

    try:

        r = requests.post(
            url,
            params={"key": API_KEY},
            json=datos,
            timeout=120
        )

        if r.status_code != 200:
            return (
                f"Error de IA {r.status_code}: "
                f"{r.text[:1000]}"
            )

        resultado = r.json()

        candidatos = resultado.get(
            "candidates",
            []
        )

        if not candidatos:
            return "La IA no produjo resultado."

        partes = candidatos[0] \
            .get("content", {}) \
            .get("parts", [])

        return "\n".join(
            p.get("text", "")
            for p in partes
        ).strip()

    except Exception as e:

        return f"Error de conexión: {e}"

# ============================================================
# CEREBRO OMEGA
# ============================================================

def ejecutar(mision):

    datos_memoria = buscar_memoria(
        mision
    )

    memoria_texto = "\n".join(
        x.get("contenido", "")
        for x in datos_memoria
    )

    if not memoria_texto:
        memoria_texto = "No existen recuerdos relevantes."

    # --------------------------------------------------------
    # 1. ANÁLISIS
    # --------------------------------------------------------

    analisis = llamar_ia(
        """
Analiza la misión.
Determina qué problema existe,
qué información importa y qué debe resolverse.
Haz el análisis directamente.
""",
        mision
        + "\n\nMEMORIA:\n"
        + memoria_texto
    )

    if not analisis:
        return None, "No hay IA conectada."

    # --------------------------------------------------------
    # 2. INVESTIGACIÓN / CONOCIMIENTO
    # --------------------------------------------------------

    investigacion = llamar_ia(
        """
Investiga intelectualmente el problema.
Utiliza el conocimiento que tienes.
Busca antecedentes, relaciones,
posibilidades y explicaciones.
Diferencia hechos de hipótesis.
""",
        mision
        + "\n\nANÁLISIS:\n"
        + analisis
    )

    if not investigacion:
        return None, "La investigación falló."

    # --------------------------------------------------------
    # 3. RAZONAMIENTO
    # --------------------------------------------------------

    razonamiento = llamar_ia(
        """
Razona sobre todos los datos.
Relaciona la información.
Encuentra consecuencias,
patrones y explicaciones.
No aceptes una conclusión
solamente porque parezca correcta.
""",
        mision
        + "\n\nANÁLISIS:\n"
        + analisis
        + "\n\nINVESTIGACIÓN:\n"
        + investigacion
        + "\n\nMEMORIA:\n"
        + memoria_texto
    )

    if not razonamiento:
        return None, "El razonamiento falló."

    # --------------------------------------------------------
    # 4. CRÍTICA
    # --------------------------------------------------------

    critica = llamar_ia(
        """
Intenta demostrar que el razonamiento
está equivocado.

Busca:
- contradicciones
- errores
- supuestos
- información faltante
- explicaciones alternativas

Sé agresivamente crítico.
""",
        razonamiento
    )

    if not critica:
        return None, "La crítica falló."

    # --------------------------------------------------------
    # 5. SÍNTESIS
    # --------------------------------------------------------

    sintesis = llamar_ia(
        """
Integra todos los resultados.
Corrige los errores detectados.
Separa hechos, inferencias
e incertidumbres.

Construye la mejor conclusión posible.
""",
        f"""
MISIÓN:
{mision}

ANÁLISIS:
{analisis}

INVESTIGACIÓN:
{investigacion}

RAZONAMIENTO:
{razonamiento}

CRÍTICA:
{critica}
"""
    )

    if not sintesis:
        return None, "La síntesis falló."

    # --------------------------------------------------------
    # 6. DECISIÓN
    # --------------------------------------------------------

    decision = llamar_ia(
        """
Produce la respuesta final.

Debe contener:
- conclusión
- razones principales
- incertidumbres
- alternativas importantes
- qué hacer después

No inventes certeza.
""",
        sintesis
    )

    if not decision:
        return None, "La decisión falló."

    # --------------------------------------------------------
    # 7. APRENDER
    # --------------------------------------------------------

    ciclo = len(experiencias()) + 1

    aprender(
        mision,
        decision
    )

    registrar_experiencia(
        mision,
        decision,
        ciclo
    )

    return {
        "ciclo": ciclo,
        "analisis": analisis,
        "investigacion": investigacion,
        "razonamiento": razonamiento,
        "critica": critica,
        "sintesis": sintesis,
        "decision": decision
    }, None

# ============================================================
# ESTADO
# ============================================================

mem = memoria()
exp = experiencias()

a, b, c, d = st.columns(4)

with a:
    st.metric("ESTADO", "🟢 ACTIVO")

with b:
    st.metric(
        "CONOCIMIENTO",
        len(mem)
    )

with c:
    st.metric(
        "EXPERIENCIAS",
        len(exp)
    )

with d:
    st.metric(
        "CICLOS ∞",
        len(exp)
    )

# ============================================================
# CENTRO
# ============================================================

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

st.subheader(
    "🧠 CENTRO DE PENSAMIENTO"
)

mision = st.text_area(
    "Dale una orden a CEREBRO OMEGA:",
    height=150,
    placeholder=(
        "Ejemplo: analiza una idea, "
        "resuelve un problema, "
        "estudia una situación..."
    )
)

if st.button(
    "⚡ EJECUTAR CICLO",
    use_container_width=True
):

    if not mision.strip():

        st.warning(
            "Escribe una orden."
        )

    elif not API_KEY:

        st.error(
            "CEREBRO OMEGA no tiene una IA conectada."
        )

        st.info(
            "Conecta GOOGLE_API_KEY en "
            "Streamlit → Manage app → Settings → Secrets."
        )

    else:

        with st.spinner(
            "🧠 CEREBRO OMEGA ∞"
        ):

            resultado, error = ejecutar(
                mision.strip()
            )

        if error:

            st.error(error)

        else:

            st.success(
                "Ciclo completado."
            )

            st.markdown(
                '<div class="panel">',
                unsafe_allow_html=True
            )

            st.markdown(
                resultado["decision"]
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            # ------------------------------------------------
            # PROCESAMIENTO REAL
            # ------------------------------------------------

            with st.expander(
                "ANÁLISIS"
            ):
                st.write(
                    resultado["analisis"]
                )

            with st.expander(
                "INVESTIGACIÓN"
            ):
                st.write(
                    resultado["investigacion"]
                )

            with st.expander(
                "RAZONAMIENTO"
            ):
                st.write(
                    resultado["razonamiento"]
                )

            with st.expander(
                "CRÍTICA"
            ):
                st.write(
                    resultado["critica"]
                )

            with st.expander(
                "SÍNTESIS"
            ):
                st.write(
                    resultado["sintesis"]
                )

# ============================================================
# MEMORIA
# ============================================================

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

st.subheader("💾 MEMORIA")

mem = memoria()

if not mem:

    st.write(
        "La memoria está vacía."
    )

else:

    for item in reversed(mem[-15:]):

        with st.expander(
            item.get(
                "fecha",
                "recuerdo"
            )
        ):

            st.write(
                item.get(
                    "contenido",
                    ""
                )
            )

# ============================================================
# EXPERIENCIAS
# ============================================================

st.subheader(
    "🧬 EXPERIENCIAS"
)

exp = experiencias()

if not exp:

    st.write(
        "Todavía no hay experiencias."
    )

else:

    for item in reversed(exp[-10:]):

        with st.expander(
            f"Ciclo {item.get('ciclo', '?')}"
        ):

            st.write(
                item.get(
                    "orden",
                    ""
                )
            )

            st.write(
                item.get(
                    "resultado",
                    ""
                )
            )

# ============================================================
# ALIMENTADOR OMEGA
# ============================================================

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

st.subheader(
    "📡 ALIMENTADOR OMEGA"
)

try:

    from modules.alimentador import AlimentadorOmega

    alimentador = AlimentadorOmega()

    st.success(
        "AlimentadorOmega conectado."
    )

except Exception as e:

    st.warning(
        f"AlimentadorOmega no disponible: {e}"
    )

# ============================================================
# DIAGNÓSTICO
# ============================================================

st.subheader(
    "🔍 DIAGNÓSTICO"
)

if API_KEY:

    st.success(
        "🟢 IA CONECTADA"
    )

else:

    st.error(
        "🔴 IA DESCONECTADA"
    )

modules = BASE / "modules"

if modules.exists():

    archivos = [
        x for x in modules.glob("*.py")
        if x.name != "__init__.py"
    ]

    st.write(
        f"Módulos detectados: {len(archivos)}"
    )

    for archivo in archivos:

        st.write(
            f"🟢 {archivo.stem}"
        )

# ============================================================
# FINAL
# ============================================================

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

st.markdown("""
<div style="
text-align:center;
font-family:monospace;
font-size:24px;
color:#eafff0;
">
🧠 CEREBRO OMEGA
<span style="
color:#00ff88;
font-size:45px;
text-shadow:
0 0 8px #00ff88,
0 0 25px #00ff88,
0 0 50px #00ff88;
">∞</span>
</div>
""", unsafe_allow_html=True)
