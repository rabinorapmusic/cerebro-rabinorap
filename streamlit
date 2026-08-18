import streamlit as st
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

# ============================================================
# 🧠 CEREBRO OMEGA — ORGANISMO COMPLETO
# Un solo archivo
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA",
    page_icon="🧠",
    layout="wide"
)

DATA = Path("omega_data")
DATA.mkdir(exist_ok=True)

MEMORY_FILE = DATA / "memory.json"
KNOWLEDGE_FILE = DATA / "knowledge.json"


# ============================================================
# UTILIDADES
# ============================================================

def now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


def save_json(path, data):
    try:
        path.write_text(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )
        return True
    except Exception:
        return False


# ============================================================
# ⚛️ PROTÓN
# CONOCIMIENTO
# ============================================================

class Proton:

    def __init__(self):
        self.status = "ACTIVE"

        self.knowledge = load_json(
            KNOWLEDGE_FILE,
            {
                "facts": {},
                "learned": {}
            }
        )

    def learn(self, topic, information, source="omega"):

        self.knowledge["learned"][topic] = {
            "information": information,
            "source": source,
            "time": now()
        }

        save_json(
            KNOWLEDGE_FILE,
            self.knowledge
        )

        return True

    def search(self, query):

        query = query.lower()
        results = []

        raw = json.dumps(
            self.knowledge,
            ensure_ascii=False
        ).lower()

        if query in raw:

            results.append(
                "Existe información relacionada "
                "en la memoria de conocimiento."
            )

        return results

    def status_report(self):

        return {
            "status": self.status,
            "facts": len(
                self.knowledge["facts"]
            ),
            "learned": len(
                self.knowledge["learned"]
            )
        }


# ============================================================
# 🌀 NEUTRÓN
# MEMORIA
# ============================================================

class Neutron:

    def __init__(self):

        self.status = "ACTIVE"

        self.memory = load_json(
            MEMORY_FILE,
            []
        )

    def remember(self, event, result):

        record = {
            "time": now(),
            "event": event,
            "result": result
        }

        self.memory.append(record)

        # Evitar crecimiento infinito.
        self.memory = self.memory[-2000:]

        save_json(
            MEMORY_FILE,
            self.memory
        )

        return record

    def recall(self, query=None, limit=10):

        if not query:
            return self.memory[-limit:]

        query = query.lower()

        matches = []

        for item in reversed(self.memory):

            if query in json.dumps(
                item,
                ensure_ascii=False
            ).lower():

                matches.append(item)

            if len(matches) >= limit:
                break

        return matches

    def status_report(self):

        return {
            "status": self.status,
            "memories": len(self.memory)
        }


# ============================================================
# 🌐 LANGUAGE ENGINE
# Traducción real mediante servicio HTTP configurable.
# ============================================================

class LanguageEngine:

    def __init__(self):

        self.status = "READY"

        # Endpoint compatible con LibreTranslate.
        self.endpoint = st.secrets.get(
            "LIBRETRANSLATE_URL",
            "https://libretranslate.com/translate"
        )

    def translate(
        self,
        text,
        source="auto",
        target="en"
    ):

        try:

            data = urllib.parse.urlencode({
                "q": text,
                "source": source,
                "target": target,
                "format": "text"
            }).encode()

            request = urllib.request.Request(
                self.endpoint,
                data=data,
                headers={
                    "Content-Type":
                    "application/x-www-form-urlencoded"
                }
            )

            with urllib.request.urlopen(
                request,
                timeout=15
            ) as response:

                result = json.loads(
                    response.read().decode()
                )

            translated = result.get(
                "translatedText"
            )

            if translated:
                return {
                    "success": True,
                    "text": translated
                }

            return {
                "success": False,
                "error": "El motor no devolvió traducción."
            }

        except Exception as error:

            self.status = "DEGRADED"

            return {
                "success": False,
                "error": str(error)
            }


# ============================================================
# 📖 BIBLE ENGINE
# Recuperación real de pasajes.
# ============================================================

class BibleEngine:

    API = "https://bible-api.com/"

    def __init__(self):

        self.status = "READY"

    def get_passage(
        self,
        reference
    ):

        try:

            encoded = urllib.parse.quote(
                reference
            )

            url = self.API + encoded

            with urllib.request.urlopen(
                url,
                timeout=15
            ) as response:

                data = json.loads(
                    response.read().decode()
                )

            verses = data.get(
                "verses",
                []
            )

            if not verses:

                return {
                    "success": False,
                    "error": "Pasaje no encontrado."
                }

            text = " ".join(
                v.get("text", "")
                for v in verses
            )

            return {
                "success": True,
                "reference": reference,
                "text": text,
                "translation": data.get(
                    "translation_name",
                    "WEB"
                )
            }

        except Exception as error:

            self.status = "DEGRADED"

            return {
                "success": False,
                "error": str(error)
            }


# ============================================================
# 🔎 INTENT ENGINE
# Entiende órdenes humanas.
# ============================================================

class IntentEngine:

    def detect(self, text):

        clean = text.lower().strip()

        # BIBLIA
        if (
            "biblia" in clean
            or "versículo" in clean
            or "versiculo" in clean
            or "pasaje bíblico" in clean
            or "pasaje biblico" in clean
        ):

            return {
                "intent": "BIBLE",
                "raw": text
            }

        # TRADUCCIÓN
        if any(
            word in clean
            for word in [
                "traduce",
                "traducir",
                "traducción",
                "traduccion"
            ]
        ):

            return {
                "intent": "TRANSLATE",
                "raw": text
            }

        # MEMORIA
        if any(
            word in clean
            for word in [
                "recuerda",
                "recuerdas",
                "memoria",
                "recuerda que"
            ]
        ):

            return {
                "intent": "MEMORY",
                "raw": text
            }

        # ESTADO
        if any(
            word in clean
            for word in [
                "estado",
                "diagnóstico",
                "diagnostico",
                "cómo estás",
                "como estas"
            ]
        ):

            return {
                "intent": "STATUS",
                "raw": text
            }

        # APRENDER
        if any(
            word in clean
            for word in [
                "aprende",
                "aprendizaje",
                "guarda esto"
            ]
        ):

            return {
                "intent": "LEARN",
                "raw": text
            }

        # GENERAL
        return {
            "intent": "CHAT",
            "raw": text
        }


# ============================================================
# 🧠 REASON ENGINE
# ============================================================

class ReasonEngine:

    def reason(
        self,
        question,
        knowledge,
        memories
    ):

        if knowledge:
            return (
                "Tengo información relacionada con "
                "tu consulta."
            )

        if memories:
            return (
                "Encontré experiencias relacionadas "
                "en mi memoria."
            )

        return (
            "Necesito una fuente de conocimiento "
            "para responder eso con seguridad."
        )


# ============================================================
# 🔊 VOICE BRIDGE
# Web Speech API
# ============================================================

def voice_bridge(text):

    safe_text = json.dumps(
        text,
        ensure_ascii=False
    )

    component = f"""
    <div style="
        padding:12px;
        border-radius:14px;
        border:1px solid rgba(128,128,128,.35);
        text-align:center;
        font-family:sans-serif;
    ">

        <button id="speak"
            style="
                width:100%;
                padding:12px;
                border-radius:10px;
                border:0;
                cursor:pointer;
                font-size:18px;
            ">
            🔊 HABLAR
        </button>

        <button id="stop"
            style="
                width:100%;
                padding:10px;
                margin-top:7px;
                border-radius:10px;
                border:0;
                cursor:pointer;
            ">
            ⏹️ DETENER
        </button>

        <div id="voice"
            style="
                margin-top:8px;
                font-size:13px;
                opacity:.75;
            ">
            CEREBRO OMEGA — VOICE BRIDGE
        </div>
    </div>

    <script>

    const text = {safe_text};

    function findMaleSpanishVoice() {{

        const voices =
            window.speechSynthesis.getVoices();

        const spanish =
            voices.filter(v =>
                v.lang &&
                v.lang.toLowerCase().startsWith("es")
            );

        if (!spanish.length)
            return null;

        const maleHints = [
            "male",
            "masculino",
            "man",
            "hombre",
            "jorge",
            "carlos",
            "diego",
            "juan",
            "miguel"
        ];

        for (const voice of spanish) {{

            const name =
                voice.name.toLowerCase();

            if (
                maleHints.some(
                    hint => name.includes(hint)
                )
            ) {{
                return voice;
            }}
        }}

        return spanish[0];
    }}

    function speakOmega() {{

        if (!window.speechSynthesis) {{

            document.getElementById("voice").innerText =
                "Este navegador no ofrece SpeechSynthesis.";

            return;
        }}

        window.speechSynthesis.cancel();

        const utterance =
            new SpeechSynthesisUtterance(text);

        utterance.lang = "es-ES";
        utterance.rate = 0.92;
        utterance.pitch = 0.72;
        utterance.volume = 1.0;

        const voice =
            findMaleSpanishVoice();

        if (voice)
            utterance.voice = voice;

        utterance.onstart = () => {{
            document.getElementById("voice").innerText =
                "🎙️ CEREBRO OMEGA HABLANDO";
        }};

        utterance.onend = () => {{
            document.getElementById("voice").innerText =
                "✅ CEREBRO OMEGA TERMINÓ";
        }};

        utterance.onerror = (event) => {{
            document.getElementById("voice").innerText =
                "⚠️ Voz: " + event.error;
        }};

        window.speechSynthesis.speak(
            utterance
        );
    }}

    document.getElementById("speak")
        .onclick = speakOmega;

    document.getElementById("stop")
        .onclick = () => {{
            window.speechSynthesis.cancel();

            document.getElementById("voice").innerText =
                "⏹️ VOZ DETENIDA";
        }};

    window.speechSynthesis.onvoiceschanged = () => {{
        findMaleSpanishVoice();
    }};

    </script>
    """

    st.components.v2.html(
        component,
        height=150
    )


# ============================================================
# 🧠 OMEGA KERNEL
# ============================================================

class CerebroOmega:

    def __init__(self):

        self.proton = Proton()
        self.neutron = Neutron()
        self.language = LanguageEngine()
        self.bible = BibleEngine()
        self.intent = IntentEngine()
        self.reason = ReasonEngine()

        self.cycles = 0

    def execute(self, user_input):

        self.cycles += 1

        intent = self.intent.detect(
            user_input
        )

        action = intent["intent"]

        # ----------------------------------------------------
        # BIBLIA
        # ----------------------------------------------------

        if action == "BIBLE":

            reference = extract_bible_reference(
                user_input
            )

            if not reference:

                return {
                    "text":
                    "Dime el libro y capítulo. "
                    "Por ejemplo: Juan 3:16."
                }

            result = self.bible.get_passage(
                reference
            )

            if result["success"]:

                text = (
                    f"{result['reference']}. "
                    f"{result['text']}"
                )

                self.neutron.remember(
                    user_input,
                    text
                )

                return {
                    "text": text,
                    "type": "BIBLE"
                }

            return {
                "text":
                "No pude recuperar ese pasaje: "
                + result["error"]
            }

        # ----------------------------------------------------
        # TRADUCCIÓN
        # ----------------------------------------------------

        if action == "TRANSLATE":

            target = detect_language(
                user_input
            )

            text = extract_translation_text(
                user_input
            )

            if not text:

                return {
                    "text":
                    "Escribe qué quieres traducir "
                    "y a qué idioma."
                }

            result = self.language.translate(
                text,
                target=target
            )

            if result["success"]:

                self.neutron.remember(
                    user_input,
                    result["text"]
                )

                return {
                    "text":
                    result["text"],
                    "type":
                    "TRANSLATION"
                }

            return {
                "text":
                "El motor de traducción no respondió: "
                + result["error"]
            }

        # ----------------------------------------------------
        # MEMORIA
        # ----------------------------------------------------

        if action == "MEMORY":

            memories = self.neutron.recall(
                user_input,
                5
            )

            if memories:

                return {
                    "text":
                    json.dumps(
                        memories,
                        ensure_ascii=False,
                        indent=2
                    )
                }

            return {
                "text":
                "No encontré recuerdos relacionados."
            }

        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        if action == "STATUS":

            return {
                "text":
                json.dumps(
                    self.status(),
                    ensure_ascii=False,
                    indent=2
                )
            }

        # ----------------------------------------------------
        # APRENDER
        # ----------------------------------------------------

        if action == "LEARN":

            topic, information = \
                extract_learning(
                    user_input
                )

            if topic and information:

                self.proton.learn(
                    topic,
                    information
                )

                return {
                    "text":
                    f"Aprendido y guardado: {topic}"
                }

            return {
                "text":
                "Usa: aprende [tema]: [información]"
            }

        # ----------------------------------------------------
        # CHAT / CONOCIMIENTO LOCAL
        # ----------------------------------------------------

        knowledge = self.proton.search(
            user_input
        )

        memories = self.neutron.recall(
            user_input,
            5
        )

        response = self.reason.reason(
            user_input,
            knowledge,
            memories
        )

        self.neutron.remember(
            user_input,
            response
        )

        return {
            "text": response,
            "type": "CHAT"
        }

    def status(self):

        return {

            "CEREBRO":
                "ONLINE",

            "PROTON":
                self.proton.status_report(),

            "ELECTRON":
                "ACTIVE",

            "NEUTRON":
                self.neutron.status_report(),

            "LANGUAGE":
                self.language.status,

            "BIBLE":
                self.bible.status,

            "CYCLES":
                self.cycles
        }


# ============================================================
# 🧩 PARSERS
# ============================================================

def extract_bible_reference(text):

    pattern = r"""
        (
            genesis|
            éxodo|exodo|
            levítico|levitico|
            números|numeros|
            deuteronomio|
            josué|josue|
            jueces|
            rut|
            1\s*samuel|
            2\s*samuel|
            1\s*reyes|
            2\s*reyes|
            salmos?|
            proverbios|
            eclesiastés|eclesiastes|
            isaías|isaias|
            jeremías|jeremias|
            mateo|
            marcos|
            lucas|
            juan|
            hechos|
            romanos|
            corintios|
            gálatas|galatas|
            efesios|
            filipenses|
            colosenses|
            hebreos|
            santiago|
            apocalipsis
        )
        \s+
        (\d+(?::\d+(?:-\d+)?)?)
    """

    match = re.search(
        pattern,
        text.lower(),
        re.VERBOSE
    )

    if not match:
        return None

    return f"{match.group(1)} {match.group(2)}"


def detect_language(text):

    text = text.lower()

    languages = {

        "inglés": "en",
        "ingles": "en",

        "francés": "fr",
        "frances": "fr",

        "portugués": "pt",
        "portugues": "pt",

        "italiano": "it",

        "alemán": "de",
        "aleman": "de",

        "español": "es",
        "espanol": "es",

        "japonés": "ja",
        "japones": "ja",

        "chino": "zh",

        "coreano": "ko"
    }

    for name, code in languages.items():

        if name in text:
            return code

    return "en"


def extract_translation_text(text):

    patterns = [
        r"traduce\s+(.+?)\s+al\s+",
        r"traducir\s+(.+?)\s+al\s+",
        r"traducción\s+(.+?)\s+al\s+",
        r"traduccion\s+(.+?)\s+al\s+"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None


def extract_learning(text):

    match = re.search(
        r"aprende\s+(.+?):\s*(.+)",
        text,
        re.IGNORECASE
    )

    if not match:
        return None, None

    return (
        match.group(1).strip(),
        match.group(2).strip()
    )


# ============================================================
# 🚀 INTERFAZ
# ============================================================

if "omega" not in st.session_state:

    st.session_state.omega = CerebroOmega()

omega = st.session_state.omega


st.title("🧠 CEREBRO OMEGA")
st.caption(
    "Organismo modular • conocimiento • memoria • idiomas • Biblia • voz"
)


# ============================================================
# PANEL
# ============================================================

col1, col2, col3, col4 = st.columns(4)

status = omega.status()

with col1:
    st.metric(
        "🧠 CEREBRO",
        status["CEREBRO"]
    )

with col2:
    st.metric(
        "⚛️ PROTÓN",
        status["PROTON"]["status"]
    )

with col3:
    st.metric(
        "🌀 NEUTRÓN",
        status["NEUTRON"]["memories"]
    )

with col4:
    st.metric(
        "🔄 CICLOS",
        status["CYCLES"]
    )


# ============================================================
# ENTRADA
# ============================================================

user_input = st.text_area(
    "Habla con CEREBRO OMEGA",
    placeholder=(
        "Ejemplos:\n"
        "• Omega, léeme Juan 3:16\n"
        "• Traduce esto al inglés: Dios es amor\n"
        "• Aprende música: la música comunica emociones\n"
        "• ¿Qué recuerdas de Juan 3:16?\n"
        "• Muéstrame tu estado"
    ),
    height=150
)


if st.button(
    "🧠 EJECUTAR",
    type="primary",
    use_container_width=True
):

    if user_input.strip():

        with st.spinner(
            "CEREBRO OMEGA procesando..."
        ):

            result = omega.execute(
                user_input
            )

        st.session_state.last_response = \
            result["text"]


# ============================================================
# RESPUESTA
# ============================================================

if "last_response" in st.session_state:

    st.subheader(
        "🧠 Respuesta de CEREBRO OMEGA"
    )

    st.write(
        st.session_state.last_response
    )

    st.subheader(
        "🎙️ Voice Bridge"
    )

    voice_bridge(
        st.session_state.last_response
    )


# ============================================================
# DIAGNÓSTICO
# ============================================================

with st.expander(
    "🩺 Diagnóstico del organismo"
):

    st.json(
        omega.status()
    )
