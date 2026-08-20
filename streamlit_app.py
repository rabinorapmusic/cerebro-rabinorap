import os
import json
import re
import html
import requests
import streamlit as st
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

# ============================================================
# 🧠 CEREBRO OMEGA ∞
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide",
)

BASE = Path(__file__).parent
DATA = BASE / "omega_data"
DATA.mkdir(exist_ok=True)

MEMORY_FILE = DATA / "memoria.json"
EXPERIENCE_FILE = DATA / "experiencias.json"

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(0,255,136,.13),
            transparent 35%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(0,255,136,.05),
            transparent 40%
        ),
        #010604;

    color:#d9ffe6;
}

header,
footer,
#MainMenu {
    visibility:hidden;
}

.omega-title {
    text-align:center;
    font-family:monospace;
    font-size:43px;
    font-weight:bold;
    letter-spacing:4px;
    color:#eafff1;
}

.infinity {
    color:#00ff88;
    font-size:72px;
    text-shadow:
        0 0 8px #00ff88,
        0 0 20px #00ff88,
        0 0 45px #00ff88,
        0 0 80px rgba(0,255,136,.65);
}

.line {
    height:1px;
    margin:20px 0;
    background:
        linear-gradient(
            90deg,
            transparent,
            #00ff88,
            transparent
        );
    box-shadow:0 0 12px #00ff88;
}

.panel {
    background:rgba(0,20,10,.72);
    border:1px solid rgba(0,255,136,.25);
    border-radius:15px;
    padding:20px;
}

.stButton>button {
    background:#002e17 !important;
    color:#00ff88 !important;
    border:1px solid #00ff88 !important;
    border-radius:10px !important;
    font-family:monospace !important;
    font-weight:bold !important;
}

.stButton>button:hover {
    background:#00ff88 !important;
    color:#001307 !important;
    box-shadow:
        0 0 18px #00ff88,
        0 0 40px rgba(0,255,136,.7);
}

textarea {
    background:#010b05 !important;
    color:#caffd9 !important;
    border:1px solid rgba(0,255,136,.4) !important;
}

[data-testid="stMetric"] {
    background:rgba(0,25,12,.7);
    border:1px solid rgba(0,255,136,.2);
    border-radius:12px;
}

[data-testid="stMetricValue"] {
    color:#00ff88 !important;
    text-shadow:0 0 10px #00ff88;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# IDENTIDAD
# ============================================================

st.markdown("""
<div class="omega-title">
    🧠 CEREBRO OMEGA
    <span class="infinity">∞</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="line"></div>', unsafe_allow_html=True)

# ============================================================
# CONFIGURACIÓN DE IA
# ============================================================

def secreto(nombre):
    try:
        valor = st.secrets.get(nombre)
        if valor:
            return str(valor)
    except Exception:
        pass

    return os.getenv(nombre, "")


HF_TOKEN = secreto("HF_TOKEN")
GROQ_API_KEY = secreto("GROQ_API_KEY")

HF_MODEL = secreto("HF_MODEL") or "openai/gpt-oss-120b:fastest"
GROQ_MODEL = secreto("GROQ_MODEL") or "openai/gpt-oss-20b"

# ============================================================
# ARCHIVOS
# ============================================================

def cargar(path, defecto):

    try:

        if not path.exists():
            return defecto

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:
        return defecto


def guardar(path, datos):

    temporal = path.with_suffix(".tmp")

    with open(
        temporal,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=2
        )

    temporal.replace(path)


def obtener_memoria():
    return cargar(
        MEMORY_FILE,
        []
    )


def obtener_experiencias():
    return cargar(
        EXPERIENCE_FILE,
        []
    )

# ============================================================
# MEMORIA
# ============================================================

def memoria_relevante(texto, limite=12):

    memoria = obtener_memoria()

    palabras = {
        p.lower()
        for p in re.findall(
            r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+",
            texto
        )
        if len(p) >= 4
    }

    resultados = []

    for item in memoria:

        contenido = str(
            item.get(
                "contenido",
                ""
            )
        )

        bajo = contenido.lower()

        puntos = sum(
            1
            for palabra in palabras
            if palabra in bajo
        )

        if puntos:

            resultados.append(
                (
                    puntos,
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


def aprender(mision, resultado):

    memoria = obtener_memoria()

    memoria.append({
        "fecha": datetime.now().isoformat(),
        "tipo": "aprendizaje",
        "contenido":
            "MISIÓN:\n"
            + mision
            + "\n\nRESULTADO:\n"
            + resultado
    })

    if len(memoria) > 3000:
        memoria = memoria[-2500:]

    guardar(
        MEMORY_FILE,
        memoria
    )


def registrar_experiencia(
    mision,
    resultado,
    ciclo
):

    experiencias = obtener_experiencias()

    experiencias.append({
        "fecha": datetime.now().isoformat(),
        "ciclo": ciclo,
        "orden": mision,
        "resultado": resultado
    })

    if len(experiencias) > 2000:
        experiencias = experiencias[-1800:]

    guardar(
        EXPERIENCE_FILE,
        experiencias
    )

# ============================================================
# INVESTIGACIÓN WEB REAL
# ============================================================

def investigar_web(consulta):

    resultados = []

    # --------------------------------------------------------
    # WIKIPEDIA
    # --------------------------------------------------------

    try:

        url = (
            "https://es.wikipedia.org/w/api.php"
        )

        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": consulta,
            "gsrlimit": 5,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "format": "json",
        }

        r = requests.get(
            url,
            params=params,
            timeout=15,
            headers={
                "User-Agent":
                    "CerebroOmega/1.0"
            }
        )

        if r.ok:

            data = r.json()

            paginas = (
                data
                .get("query", {})
                .get("pages", {})
            )

            for pagina in paginas.values():

                titulo = pagina.get(
                    "title",
                    ""
                )

                texto = pagina.get(
                    "extract",
                    ""
                )

                if texto:

                    resultados.append({
                        "fuente": "Wikipedia",
                        "titulo": titulo,
                        "texto": texto[:3500]
                    })

    except Exception:
        pass

    # --------------------------------------------------------
    # DUCKDUCKGO
    # --------------------------------------------------------

    try:

        url = (
            "https://html.duckduckgo.com/html/"
        )

        r = requests.post(
            url,
            data={
                "q": consulta
            },
            timeout=15,
            headers={
                "User-Agent":
                    "Mozilla/5.0"
            }
        )

        if r.ok:

            texto = re.sub(
                r"<[^>]+>",
                " ",
                r.text
            )

            texto = html.unescape(
                texto
            )

            texto = re.sub(
                r"\s+",
                " ",
                texto
            )

            resultados.append({
                "fuente": "DuckDuckGo",
                "titulo": consulta,
                "texto": texto[:5000]
            })

    except Exception:
        pass

    return resultados

# ============================================================
# HUGGING FACE
# ============================================================

def ia_huggingface(
    system,
    user
):

    if not HF_TOKEN:
        return None

    try:

        from huggingface_hub import InferenceClient

        client = InferenceClient(
            api_key=HF_TOKEN
        )

        respuesta = client.chat.completions.create(
            model=HF_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": user
                }
            ],
            temperature=0.35,
            max_tokens=5000,
        )

        return (
            respuesta
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        return None

# ============================================================
# GROQ
# ============================================================

def ia_groq(
    system,
    user
):

    if not GROQ_API_KEY:
        return None

    try:

        from openai import OpenAI

        client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=
                "https://api.groq.com/openai/v1"
        )

        respuesta = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": user
                }
            ],
            temperature=0.35,
            max_tokens=5000,
        )

        return (
            respuesta
            .choices[0]
            .message
            .content
        )

    except Exception:
        return None

# ============================================================
# MOTOR IA
# ============================================================

def pensar(
    system,
    user
):

    respuesta = ia_huggingface(
        system,
        user
    )

    if respuesta:
        return respuesta, "HUGGING FACE"

    respuesta = ia_groq(
        system,
        user
    )

    if respuesta:
        return respuesta, "GROQ"

    return None, None

# ============================================================
# MISIÓN OMEGA
# ============================================================

def ejecutar_omega(mision):

    recuerdos = memoria_relevante(
        mision
    )

    memoria_texto = "\n".join(
        item.get(
            "contenido",
            ""
        )
        for item in recuerdos
    )

    if not memoria_texto:
        memoria_texto = "No existen recuerdos relevantes."

    # --------------------------------------------------------
    # INVESTIGACIÓN
    # --------------------------------------------------------

    fuentes = investigar_web(
        mision
    )

    investigacion_texto = "\n\n".join(
        (
            f"FUENTE: {x['fuente']}\n"
            f"{x['titulo']}\n"
            f"{x['texto']}"
        )
        for x in fuentes
    )

    if not investigacion_texto:

        investigacion_texto = (
            "No se obtuvieron fuentes web."
        )

    # --------------------------------------------------------
    # DIRECTOR
    # --------------------------------------------------------

    director, proveedor = pensar(

        """
Eres el director de CEREBRO OMEGA ∞.

Tu trabajo no es explicar cómo trabajar.
Tu trabajo es trabajar.

Analiza la misión, identifica el problema
y determina qué información realmente importa.

No inventes datos.
""",

        f"""
MISIÓN:

{mision}

MEMORIA:

{memoria_texto}

INVESTIGACIÓN DISPONIBLE:

{investigacion_texto}
"""
    )

    if not director:
        return None, "No hay ningún proveedor de IA disponible."

    # --------------------------------------------------------
    # RAZONAMIENTO
    # --------------------------------------------------------

    razonamiento, _ = pensar(

        """
Eres el razonador de CEREBRO OMEGA ∞.

Utiliza los datos recibidos.
Relaciona hechos.
Haz inferencias.
Detecta patrones.
Separa hechos de hipótesis.

No repitas información inútil.
Razonamiento real.
""",

        f"""
MISIÓN:

{mision}

DIRECTOR:

{director}

FUENTES:

{investigacion_texto}

MEMORIA:

{memoria_texto}
"""
    )

    if not razonamiento:
        return None, "Falló el razonamiento."

    # --------------------------------------------------------
    # CRÍTICO
    # --------------------------------------------------------

    critica, _ = pensar(

        """
Eres el crítico de CEREBRO OMEGA ∞.

Intenta demostrar que la conclusión es incorrecta.

Busca:
- errores
- contradicciones
- datos insuficientes
- falsas suposiciones
- explicaciones alternativas

No seas complaciente.
""",

        f"""
MISIÓN:

{mision}

RAZONAMIENTO:

{razonamiento}

FUENTES:

{investigacion_texto}
"""
    )

    if not critica:
        return None, "Falló la crítica."

    # --------------------------------------------------------
    # SÍNTESIS
    # --------------------------------------------------------

    sintesis, _ = pensar(

        """
Eres el sintetizador de CEREBRO OMEGA ∞.

Integra la información.
Corrige los errores señalados.
No ocultes incertidumbres.

Produce la mejor conclusión posible.
""",

        f"""
MISIÓN:

{mision}

DIRECTOR:

{director}

RAZONAMIENTO:

{razonamiento}

CRÍTICA:

{critica}

INVESTIGACIÓN:

{investigacion_texto}
"""
    )

    if not sintesis:
        return None, "Falló la síntesis."

    # --------------------------------------------------------
    # DECISIÓN FINAL
    # --------------------------------------------------------

    decision, _ = pensar(

        """
Eres la inteligencia decisora de
CEREBRO OMEGA ∞.

Produce el resultado final.

Debes entregar una respuesta útil,
concreta y razonada.

Distingue:
HECHOS
INFERENCIAS
INCERTIDUMBRES

No inventes certeza.
""",

        f"""
MISIÓN:

{mision}

SÍNTESIS:

{sintesis}

CRÍTICA:

{critica}
"""
    )

    if not decision:
        return None, "Falló la decisión final."

    # --------------------------------------------------------
    # APRENDIZAJE
    # --------------------------------------------------------

    ciclo = len(
        obtener_experiencias()
    ) + 1

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
        "proveedor": proveedor,
        "fuentes": fuentes,
        "director": director,
        "razonamiento": razonamiento,
        "critica": critica,
        "sintesis": sintesis,
        "decision": decision,
    }, None

# ============================================================
# ESTADO
# ============================================================

mem = obtener_memoria()
exp = obtener_experiencias()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "ESTADO",
        "🟢 ACTIVO"
    )

with c2:
    st.metric(
        "CONOCIMIENTO",
        len(mem)
    )

with c3:
    st.metric(
        "EXPERIENCIAS",
        len(exp)
    )

with c4:
    st.metric(
        "CICLOS ∞",
        len(exp)
    )

# ============================================================
# CENTRO DE PENSAMIENTO
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
    height=160,
    placeholder=(
        "Escribe aquí la misión..."
    )
)

if st.button(
    "⚡ EJECUTAR CICLO",
    use_container_width=True
):

    if not mision.strip():

        st.warning(
            "Escribe una misión."
        )

    elif not HF_TOKEN and not GROQ_API_KEY:

        st.error(
            "CEREBRO OMEGA no tiene conectado ningún "
            "proveedor de IA."
        )

        st.info(
            "Añade HF_TOKEN o GROQ_API_KEY "
            "en Secrets."
        )

    else:

        with st.status(
            "🧠 CEREBRO OMEGA ∞",
            expanded=True
        ) as estado:

            resultado, error = ejecutar_omega(
                mision.strip()
            )

            if error:

                estado.update(
                    label="Error",
                    state="error"
                )

                st.error(error)

            else:

                estado.update(
                    label="Ciclo completado",
                    state="complete"
                )

        if resultado:

            st.markdown(
                '<div class="line"></div>',
                unsafe_allow_html=True
            )

            st.subheader(
                "♾️ RESULTADO"
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

            st.caption(
                "Proveedor de IA: "
                + resultado["proveedor"]
            )

            # ------------------------------------------------
            # FUENTES
            # ------------------------------------------------

            if resultado["fuentes"]:

                with st.expander(
                    "INVESTIGACIÓN"
                ):

                    for fuente in resultado["fuentes"]:

                        st.markdown(
                            f"**{fuente['fuente']} — "
                            f"{fuente['titulo']}**"
                        )

                        st.write(
                            fuente["texto"]
                        )

            with st.expander(
                "DIRECTOR"
            ):
                st.write(
                    resultado["director"]
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

st.subheader(
    "💾 MEMORIA"
)

mem = obtener_memoria()

if not mem:

    st.write(
        "La memoria está vacía."
    )

else:

    for item in reversed(
        mem[-15:]
    ):

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

exp = obtener_experiencias()

if not exp:

    st.write(
        "Todavía no hay experiencias."
    )

else:

    for item in reversed(
        exp[-10:]
    ):

        with st.expander(
            "Ciclo "
            + str(
                item.get(
                    "ciclo",
                    "?"
                )
            )
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
# ALIMENTADOR
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

    AlimentadorOmega()

    st.success(
        "AlimentadorOmega conectado."
    )

except Exception as error:

    st.warning(
        "AlimentadorOmega no disponible: "
        + str(error)
    )

# ============================================================
# DIAGNÓSTICO
# ============================================================

st.subheader(
    "🔍 DIAGNÓSTICO"
)

if HF_TOKEN:

    st.success(
        "🟢 HUGGING FACE CONECTADO"
    )

elif GROQ_API_KEY:

    st.success(
        "🟢 GROQ CONECTADO"
    )

else:

    st.error(
        "🔴 IA DESCONECTADA"
    )

st.caption(
    "CEREBRO OMEGA ∞"
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
color:#eafff1;
">
🧠 CEREBRO OMEGA
<span style="
color:#00ff88;
font-size:52px;
text-shadow:
0 0 8px #00ff88,
0 0 25px #00ff88,
0 0 50px #00ff88;
">∞</span>
</div>
""", unsafe_allow_html=True)
