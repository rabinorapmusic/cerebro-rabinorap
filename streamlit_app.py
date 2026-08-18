import streamlit as st
import requests
import json
import re
import html
import hashlib
from pathlib import Path
from datetime import datetime, timezone

# ============================================================
# 🧠 CEREBRO OMEGA
# MONOLÍTICO — TODO EN UN SOLO streamlit_app.py
#
# Python = CORE / memoria / conocimiento / motores
# JavaScript = voz del navegador
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CONFIGURACIÓN
# ============================================================

APP_NAME = "CEREBRO OMEGA"
VERSION = "2.0.0"

BASE_DIR = Path(".")
MEMORY_FILE = BASE_DIR / "cerebro_memory.json"
KNOWLEDGE_FILE = BASE_DIR / "cerebro_knowledge.json"
CYCLES_FILE = BASE_DIR / "cerebro_cycles.json"

MAX_MEMORY = 100
MAX_KNOWLEDGE = 500
MAX_CYCLES = 200


# ============================================================
# UTILIDADES
# ============================================================

def now():
    return datetime.now(timezone.utc).isoformat()


def safe_text(value, limit=5000):
    if value is None:
        return ""

    value = str(value).strip()

    if len(value) > limit:
        value = value[:limit]

    return value


def clean_query(text):
    text = safe_text(text, 1000)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_id(text):
    return hashlib.sha256(
        f"{now()}::{text}".encode("utf-8")
    ).hexdigest()[:16]


# ============================================================
# PERSISTENCIA
# ============================================================

def load_json(path, default):
    try:
        if not path.exists():
            return default

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    except Exception:
        return default


def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )

        return True

    except Exception:
        return False


def load_memory():
    return load_json(MEMORY_FILE, [])


def save_memory(memory):
    memory = memory[-MAX_MEMORY:]
    return save_json(MEMORY_FILE, memory)


def load_knowledge():
    return load_json(KNOWLEDGE_FILE, [])


def save_knowledge(knowledge):
    knowledge = knowledge[-MAX_KNOWLEDGE:]
    return save_json(KNOWLEDGE_FILE, knowledge)


def load_cycles():
    return load_json(CYCLES_FILE, [])


def save_cycles(cycles):
    cycles = cycles[-MAX_CYCLES:]
    return save_json(CYCLES_FILE, cycles)


# ============================================================
# ESTADO DEL CEREBRO
# ============================================================

if "memory" not in st.session_state:
    st.session_state.memory = load_memory()

if "knowledge" not in st.session_state:
    st.session_state.knowledge = load_knowledge()

if "cycles" not in st.session_state:
    st.session_state.cycles = load_cycles()

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if "last_cycle" not in st.session_state:
    st.session_state.last_cycle = None


# ============================================================
# REGISTRY INTERNO
# ============================================================

ENGINE_REGISTRY = {
    "bible": "Motor Bíblico",
    "science": "Motor Científico",
    "knowledge": "Motor de Conocimiento",
    "memory": "Motor de Memoria",
    "reasoning": "Motor de Razonamiento",
    "music": "Motor Musical",
    "evolution": "Motor Evolutivo",
}


# ============================================================
# MOTOR DE BIBLIA
# ============================================================

def bible_engine(topic):
    topic = clean_query(topic)

    if not topic:
        return {
            "engine": "bible",
            "success": False,
            "text": "No se recibió un tema."
        }

    try:
        url = "https://bible-api.com/"

        params = {
            "q": topic,
            "translation": "rvr1960"
        }

        response = requests.get(
            url,
            params=params,
            timeout=6
        )

        if response.status_code != 200:
            raise Exception("API bíblica no disponible")

        data = response.json()

        reference = data.get(
            "reference",
            "Referencia desconocida"
        )

        text = data.get(
            "text",
            ""
        ).strip()

        if not text:
            raise Exception("Sin resultado")

        text = re.sub(r"\s+", " ", text)

        return {
            "engine": "bible",
            "success": True,
            "reference": reference,
            "text": text[:1500]
        }

    except Exception:
        return {
            "engine": "bible",
            "success": False,
            "reference": "",
            "text": "No fue posible consultar la fuente bíblica."
        }


# ============================================================
# MOTOR CIENTÍFICO
# ============================================================

def science_engine(topic):
    topic = clean_query(topic)

    if not topic:
        return {
            "engine": "science",
            "success": False,
            "text": "No se recibió un tema científico."
        }

    try:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

        params = {
            "db": "pubmed",
            "term": topic,
            "retmax": 5,
            "retmode": "json"
        }

        response = requests.get(
            url,
            params=params,
            timeout=6
        )

        if response.status_code != 200:
            raise Exception("PubMed no disponible")

        data = response.json()

        result = data.get(
            "esearchresult",
            {}
        )

        ids = result.get(
            "idlist",
            []
        )

        count = result.get(
            "count",
            "0"
        )

        return {
            "engine": "science",
            "success": True,
            "count": int(count),
            "ids": ids,
            "text": (
                f"PubMed reporta {count} resultados "
                f"para la consulta."
            )
        }

    except Exception:
        return {
            "engine": "science",
            "success": False,
            "count": 0,
            "ids": [],
            "text": "No fue posible consultar PubMed."
        }


# ============================================================
# MOTOR DE CONOCIMIENTO
# ============================================================

def knowledge_engine(topic):
    topic = clean_query(topic).lower()

    matches = []

    for item in st.session_state.knowledge:

        content = str(
            item.get("content", "")
        ).lower()

        title = str(
            item.get("title", "")
        ).lower()

        if (
            topic in content
            or topic in title
        ):
            matches.append(item)

    return {
        "engine": "knowledge",
        "success": True,
        "matches": matches[-10:],
        "count": len(matches)
    }


# ============================================================
# MOTOR DE MEMORIA
# ============================================================

def memory_engine(topic):
    topic = clean_query(topic).lower()

    matches = []

    for item in st.session_state.memory:

        command = str(
            item.get("command", "")
        ).lower()

        response = str(
            item.get("response", "")
        ).lower()

        if (
            topic in command
            or topic in response
        ):
            matches.append(item)

    return {
        "engine": "memory",
        "success": True,
        "matches": matches[-10:],
        "count": len(matches)
    }


# ============================================================
# MOTOR MUSICAL
# ============================================================

def music_engine(topic):
    text = topic.lower()

    musical_words = [
        "música",
        "musica",
        "canción",
        "cancion",
        "rap",
        "trap",
        "dembow",
        "beat",
        "ritmo",
        "melodía",
        "melodia",
        "letra",
        "suno",
        "hip hop",
    ]

    detected = any(
        word in text
        for word in musical_words
    )

    if not detected:
        return {
            "engine": "music",
            "success": False,
            "text": "No se detectó una orden musical."
        }

    return {
        "engine": "music",
        "success": True,
        "text": (
            "Orden musical detectada. "
            "CEREBRO puede preparar concepto, "
            "BPM, tonalidad, estructura y prompt."
        )
    }


# ============================================================
# DETECTOR DE INTENCIÓN
# ============================================================

def detect_engines(command):

    text = command.lower()

    selected = []

    bible_words = [
        "biblia",
        "versículo",
        "versiculo",
        "cristo",
        "jesús",
        "jesus",
        "dios",
        "salmo",
        "proverbios",
        "torah",
        "evangelio",
    ]

    science_words = [
        "ciencia",
        "científico",
        "cientifico",
        "estudio",
        "estudios",
        "pubmed",
        "investigación",
        "investigacion",
        "universo",
        "biología",
        "biologia",
        "física",
        "fisica",
        "medicina",
    ]

    music_words = [
        "rap",
        "trap",
        "dembow",
        "beat",
        "música",
        "musica",
        "canción",
        "cancion",
        "suno",
        "hip hop",
    ]

    if any(x in text for x in bible_words):
        selected.append("bible")

    if any(x in text for x in science_words):
        selected.append("science")

    if any(x in text for x in music_words):
        selected.append("music")

    selected.append("knowledge")
    selected.append("memory")
    selected.append("reasoning")

    return list(dict.fromkeys(selected))


# ============================================================
# MOTOR DE RAZONAMIENTO
# ============================================================

def reasoning_engine(command, results):

    pieces = []

    bible = results.get("bible")

    if bible and bible.get("success"):
        pieces.append(
            f"Fuente bíblica: "
            f"{bible.get('reference')} — "
            f"{bible.get('text')}"
        )

    science = results.get("science")

    if science and science.get("success"):
        pieces.append(
            f"Fuente científica: "
            f"{science.get('text')}"
        )

    knowledge = results.get("knowledge")

    if knowledge:
        count = knowledge.get("count", 0)

        if count:
            pieces.append(
                f"Conocimiento interno relacionado: "
                f"{count} registro(s)."
            )

    memory = results.get("memory")

    if memory:
        count = memory.get("count", 0)

        if count:
            pieces.append(
                f"Memoria relacionada: "
                f"{count} ciclo(s) anterior(es)."
            )

    music = results.get("music")

    if music and music.get("success"):
        pieces.append(
            music.get("text", "")
        )

    if not pieces:
        pieces.append(
            "No se encontraron fuentes especializadas."
        )

    answer = (
        "🧠 ANÁLISIS DE CEREBRO OMEGA\n\n"
        f"Orden: {command}\n\n"
        + "\n\n".join(pieces)
        + "\n\n"
        "Conclusión del ciclo: "
        "la información disponible fue recopilada "
        "y organizada por los motores internos. "
        "El resultado puede evolucionar cuando "
        "CEREBRO incorpore nuevo conocimiento."
    )

    return {
        "engine": "reasoning",
        "success": True,
        "text": answer
    }


# ============================================================
# MOTOR EVOLUTIVO
# ============================================================

def evolution_engine(command, results):

    successful = 0
    total = 0

    for name, result in results.items():

        if name == "reasoning":
            continue

        total += 1

        if isinstance(result, dict):
            if result.get("success"):
                successful += 1

    score = 0

    if total:
        score = round(
            (successful / total) * 100,
            2
        )

    if score >= 80:
        status = "CICLO FUERTE"

    elif score >= 50:
        status = "CICLO PARCIAL"

    else:
        status = "CICLO INCOMPLETO"

    return {
        "engine": "evolution",
        "success": True,
        "score": score,
        "status": status,
        "text": (
            f"Evaluación evolutiva: {status}. "
            f"Eficiencia del ciclo: {score}%."
        )
    }


# ============================================================
# GUARDAR CONOCIMIENTO
# ============================================================

def learn(title, content, source="CEREBRO OMEGA"):

    content = safe_text(content, 5000)

    if not content:
        return False

    item = {
        "id": make_id(title + content),
        "title": safe_text(title, 200),
        "content": content,
        "source": source,
        "created_at": now()
    }

    st.session_state.knowledge.append(item)

    st.session_state.knowledge = (
        st.session_state.knowledge[-MAX_KNOWLEDGE:]
    )

    return save_knowledge(
        st.session_state.knowledge
    )


# ============================================================
# GUARDAR MEMORIA
# ============================================================

def remember(command, response):

    item = {
        "id": make_id(command),
        "command": safe_text(command, 2000),
        "response": safe_text(response, 8000),
        "created_at": now()
    }

    st.session_state.memory.append(item)

    st.session_state.memory = (
        st.session_state.memory[-MAX_MEMORY:]
    )

    return save_memory(
        st.session_state.memory
    )


# ============================================================
# EJECUTOR DEL CEREBRO
# ============================================================

def execute_brain(command):

    command = clean_query(command)

    if not command:
        return None

    engines = detect_engines(command)

    results = {}

    # ----------------------------------------
    # EJECUTAR MOTORES
    # ----------------------------------------

    if "bible" in engines:
        results["bible"] = bible_engine(command)

    if "science" in engines:
        results["science"] = science_engine(command)

    if "music" in engines:
        results["music"] = music_engine(command)

    if "knowledge" in engines:
        results["knowledge"] = knowledge_engine(command)

    if "memory" in engines:
        results["memory"] = memory_engine(command)

    # ----------------------------------------
    # RAZONAMIENTO
    # ----------------------------------------

    results["reasoning"] = reasoning_engine(
        command,
        results
    )

    # ----------------------------------------
    # EVOLUCIÓN
    # ----------------------------------------

    results["evolution"] = evolution_engine(
        command,
        results
    )

    answer = results["reasoning"]["text"]

    evolution = results["evolution"]

    answer += (
        "\n\n♻️ EVOLUCIÓN\n"
        + evolution["text"]
    )

    # ----------------------------------------
    # CICLO
    # ----------------------------------------

    cycle = {
        "id": make_id(command),
        "timestamp": now(),
        "command": command,
        "engines": engines,
        "score": evolution["score"],
        "status": evolution["status"]
    }

    st.session_state.cycles.append(cycle)

    st.session_state.cycles = (
        st.session_state.cycles[-MAX_CYCLES:]
    )

    save_cycles(
        st.session_state.cycles
    )

    # ----------------------------------------
    # MEMORIA
    # ----------------------------------------

    remember(
        command,
        answer
    )

    # ----------------------------------------
    # APRENDIZAJE BÁSICO
    # ----------------------------------------

    learn(
        f"Resultado: {command}",
        answer,
        "Ciclo interno de CEREBRO OMEGA"
    )

    st.session_state.last_cycle = cycle

    return {
        "answer": answer,
        "results": results,
        "cycle": cycle
    }


# ============================================================
# JAVASCRIPT — VOZ
# ============================================================

def speak(text):

    text = safe_text(text, 10000)

    escaped = json.dumps(
        text,
        ensure_ascii=False
    )

    js = f"""
    <script>
    const texto = {escaped};

    function hablarCerebro() {{
        if (!window.speechSynthesis) {{
            alert("Este navegador no soporta voz.");
            return;
        }}

        window.speechSynthesis.cancel();

        const mensaje =
            new SpeechSynthesisUtterance(texto);

        mensaje.lang = "es-MX";
        mensaje.rate = 0.90;
        mensaje.pitch = 1.0;

        window.speechSynthesis.speak(mensaje);
    }}

    hablarCerebro();
    </script>
    """

    st.components.v1.html(
        js,
        height=1
    )


# ============================================================
# INTERFAZ
# ============================================================

st.markdown(
    """
    <style>

    .omega-title {
        text-align:center;
        font-size:42px;
        font-weight:900;
        margin-bottom:0;
    }

    .omega-subtitle {
        text-align:center;
        opacity:0.75;
        font-size:16px;
        margin-bottom:25px;
    }

    .omega-card {
        padding:20px;
        border-radius:18px;
        border:1px solid rgba(128,128,128,.25);
        margin-bottom:15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="omega-title">🧠 CEREBRO OMEGA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="omega-subtitle">'
    'CORE MONOLÍTICO • CONOCIMIENTO • MEMORIA • EVOLUCIÓN'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🧠 SISTEMA")

    st.write(
        f"**Versión:** {VERSION}"
    )

    st.divider()

    st.subheader("⚙️ Motores")

    for key, name in ENGINE_REGISTRY.items():
        st.write(
            f"• {name}"
        )

    st.divider()

    st.metric(
        "🧠 Memoria",
        len(st.session_state.memory)
    )

    st.metric(
        "📚 Conocimiento",
        len(st.session_state.knowledge)
    )

    st.metric(
        "♻️ Ciclos",
        len(st.session_state.cycles)
    )

    st.divider()

    if st.button(
        "🗑️ LIMPIAR MEMORIA",
        use_container_width=True
    ):

        st.session_state.memory = []

        save_memory([])

        st.success(
            "Memoria limpiada."
        )

    if st.button(
        "🧹 LIMPIAR CONOCIMIENTO",
        use_container_width=True
    ):

        st.session_state.knowledge = []

        save_knowledge([])

        st.success(
            "Conocimiento limpiado."
        )


# ============================================================
# ENTRADA
# ============================================================

st.subheader("🎯 ORDEN PARA CEREBRO")

command = st.text_area(
    "Escribe una orden:",
    placeholder=(
        "Ejemplo: analiza la relación entre "
        "Dios, la creación y la ciencia"
    ),
    height=130,
    label_visibility="collapsed"
)


col1, col2 = st.columns(
    [3, 1]
)

with col1:

    execute = st.button(
        "🚀 EJECUTAR CEREBRO",
        type="primary",
        use_container_width=True
    )

with col2:

    if st.button(
        "🧪 PRUEBA",
        use_container_width=True
    ):
        command = (
            "Analiza la relación entre "
            "Dios, creación y ciencia"
        )
        execute = True


# ============================================================
# EJECUCIÓN
# ============================================================

if execute:

    if not command.strip():

        st.warning(
            "Escribe una orden primero."
        )

    else:

        with st.spinner(
            "🧠 CEREBRO OMEGA procesando..."
        ):

            result = execute_brain(
                command
            )

        if result:

            st.session_state.last_response = (
                result["answer"]
            )

            st.success(
                "Ciclo completado."
            )


# ============================================================
# RESPUESTA
# ============================================================

if st.session_state.last_response:

    st.divider()

    st.subheader(
        "🧠 RESPUESTA DE CEREBRO OMEGA"
    )

    st.text_area(
        "Resultado",
        st.session_state.last_response,
        height=400,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔊 CEREBRO HABLA",
            use_container_width=True
        ):

            speak(
                st.session_state.last_response
            )

    with col2:

        if st.button(
            "💾 GUARDAR RESPUESTA",
            use_container_width=True
        ):

            ok = learn(
                "Respuesta guardada manualmente",
                st.session_state.last_response,
                "Usuario"
            )

            if ok:
                st.success(
                    "Guardado en conocimiento."
                )


# ============================================================
# DETALLES DEL ÚLTIMO CICLO
# ============================================================

if st.session_state.last_cycle:

    st.divider()

    st.subheader(
        "♻️ ÚLTIMO CICLO EVOLUTIVO"
    )

    cycle = st.session_state.last_cycle

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Estado",
            cycle["status"]
        )

    with c2:
        st.metric(
            "Eficiencia",
            f'{cycle["score"]}%'
        )

    with c3:
        st.metric(
            "Motores",
            len(cycle["engines"])
        )

    st.caption(
        "Motores utilizados:"
    )

    st.code(
        ", ".join(cycle["engines"])
    )


# ============================================================
# HISTORIAL
# ============================================================

st.divider()

st.subheader(
    "📜 HISTORIAL DE CICLOS"
)

if st.session_state.cycles:

    for cycle in reversed(
        st.session_state.cycles[-10:]
    ):

        with st.expander(
            f'♻️ {cycle["status"]} — '
            f'{cycle["score"]}% — '
            f'{cycle["command"][:80]}'
        ):

            st.write(
                "**Orden:**",
                cycle["command"]
            )

            st.write(
                "**Motores:**",
                ", ".join(
                    cycle["engines"]
                )
            )

            st.write(
                "**Fecha:**",
                cycle["timestamp"]
            )

else:

    st.info(
        "Todavía no existen ciclos."
    )


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "🧠 CEREBRO OMEGA "
    f"v{VERSION} — "
    "CORE monolítico con Python + JavaScript"
)
