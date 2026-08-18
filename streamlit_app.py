import streamlit as st
import json
import re
import urllib.parse
import urllib.request
import random
from pathlib import Path
from datetime import datetime, timezone

# ============================================================
# 🧠 CEREBRO OMEGA ♾️
# UN SOLO ARCHIVO — ORGANISMO MODULAR
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
            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
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
# MOTOR DE CONOCIMIENTO
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

    def learn(
        self,
        topic,
        information,
        source="omega"
    ):

        try:

            self.knowledge.setdefault(
                "learned",
                {}
            )

            self.knowledge["learned"][topic] = {
                "information": information,
                "source": source,
                "time": now()
            }

            save_json(
                KNOWLEDGE_FILE,
                self.knowledge
            )

            return {
                "success": True,
                "topic": topic
            }

        except Exception as error:

            self.status = "DEGRADED"

            return {
                "success": False,
                "error": str(error)
            }

    def search(self, query):

        try:

            query = query.lower().strip()

            results = []

            for topic, item in self.knowledge.get(
                "learned",
                {}
            ).items():

                text = json.dumps(
                    item,
                    ensure_ascii=False
                ).lower()

                if (
                    query in topic.lower()
                    or query in text
                ):

                    results.append({
                        "topic": topic,
                        "information":
                            item.get(
                                "information",
                                ""
                            )
                    })

            return results

        except Exception:

            self.status = "DEGRADED"

            return []

    def status_report(self):

        return {
            "status": self.status,
            "facts": len(
                self.knowledge.get(
                    "facts",
                    {}
                )
            ),
            "learned": len(
                self.knowledge.get(
                    "learned",
                    {}
                )
            )
        }


# ============================================================
# ⚡ ELECTRÓN
# MOTOR DE EJECUCIÓN
# ============================================================

class Electron:

    def __init__(self):

        self.status = "ACTIVE"
        self.executions = 0
        self.last_action = None
        self.last_result = None

    def execute(
        self,
        action,
        payload=None
    ):

        try:

            self.executions += 1
            self.last_action = action

            self.last_result = {
                "success": True,
                "action": action,
                "payload": payload,
                "execution":
                    self.executions
            }

            return self.last_result

        except Exception as error:

            self.status = "DEGRADED"

            return {
                "success": False,
                "error": str(error)
            }

    def status_report(self):

        return {
            "status": self.status,
            "executions": self.executions,
            "last_action":
                self.last_action
        }


# ============================================================
# 🌀 NEUTRÓN
# MOTOR DE MEMORIA
# ============================================================

class Neutron:

    def __init__(self):

        self.status = "ACTIVE"

        self.memory = load_json(
            MEMORY_FILE,
            []
        )

    def remember(
        self,
        event,
        result
    ):

        try:

            record = {
                "time": now(),
                "event": event,
                "result": result
            }

            self.memory.append(record)

            self.memory = self.memory[-2000:]

            save_json(
                MEMORY_FILE,
                self.memory
            )

            return {
                "success": True,
                "record": record
            }

        except Exception as error:

            self.status = "DEGRADED"

            return {
                "success": False,
                "error": str(error)
            }

    def recall(
        self,
        query=None,
        limit=10
    ):

        try:

            if not query:
                return self.memory[-limit:]

            query = query.lower()

            matches = []

            for item in reversed(
                self.memory
            ):

                text = json.dumps(
                    item,
                    ensure_ascii=False
                ).lower()

                if query in text:

                    matches.append(item)

                if len(matches) >= limit:
                    break

            return matches

        except Exception:

            self.status = "DEGRADED"

            return []

    def status_report(self):

        return {
            "status": self.status,
            "memories":
                len(self.memory)
        }


# ============================================================
# 🌐 LANGUAGE ENGINE
# ============================================================

class LanguageEngine:

    def __init__(self):

        self.status = "READY"

        try:
            self.endpoint = st.secrets.get(
                "LIBRETRANSLATE_URL",
                "https://libretranslate.com/translate"
            )
        except Exception:
            self.endpoint = (
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

                self.status = "READY"

                return {
                    "success": True,
                    "text": translated
                }

            return {
                "success": False,
                "error":
                    "El motor no devolvió traducción."
            }

        except Exception as error:

            self.status = "DEGRADED"

            return {
                "success": False,
                "error": str(error)
            }


# ============================================================
# 📖 BIBLE ENGINE
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
                    "error":
                        "Pasaje no encontrado."
                }

            text = " ".join(
                v.get("text", "")
                for v in verses
            )

            return {
                "success": True,
                "reference": reference,
                "text": text,
                "translation":
                    data.get(
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
# 🎵 MOTOR MUSICAL
# ============================================================

class MusicEngine:

    def __init__(self):

        self.status = "ACTIVE"

        self.keys = [
            "C Mayor",
            "D Mayor",
            "E Mayor",
            "G Mayor",
            "A Mayor",
            "C Menor",
            "D Menor",
            "E Menor"
        ]

        self.progressions = [
            "I - V - vi - IV",
            "vi - IV - I - V",
            "I - vi - IV - V",
            "IV - I - V - vi"
        ]

    def create_plan(
        self,
        bpm=72
    ):

        return {
            "BPM": bpm,
            "Tonalidad":
                random.choice(self.keys),
            "Progresión":
                random.choice(
                    self.progressions
                )
        }


# ============================================================
# ♾️ MOTOR EVOLUTIVO
# ============================================================

class EvolutionEngine:

    def __init__(self):

        self.status = "ACTIVE"
        self.cycles = []

    def possibility(
        self,
        objective,
        bpm
    ):

        ideas = [

            "Crear una atmósfera íntima de adoración",

            "Construir un coro congregacional poderoso",

            "Desarrollar una melodía contemplativa",

            "Crear una progresión emocional ascendente",

            "Combinar adoración íntima con expansión épica",

            "Crear una estructura sencilla y memorable",

            "Desarrollar una letra centrada en la presencia de Dios",

            "Crear una interpretación profunda y espiritual"
        ]

        return {
            "idea":
                random.choice(ideas),

            "BPM":
                bpm,

            "score":
                round(
                    random.uniform(
                        0.55,
                        0.99
                    ),
                    2
                ),

            "objective":
                objective
        }

    def evolve(
        self,
        objective,
        bpm=72,
        possibilities=8,
        cycles=4
    ):

        history = []

        for cycle_number in range(
            1,
            cycles + 1
        ):

            generated = [
                self.possibility(
                    objective,
                    bpm
                )
                for _ in range(
                    possibilities
                )
            ]

            generated.sort(
                key=lambda x:
                    x["score"],
                reverse=True
            )

            selected = generated[:4]

            average = round(
                sum(
                    item["score"]
                    for item in generated
                )
                /
                len(generated),
                2
            )

            history.append({
                "cycle":
                    cycle_number,

                "generated":
                    generated,

                "selected":
                    selected,

                "average":
                    average,

                "maximum":
                    generated[0]["score"],

                "minimum":
                    generated[-1]["score"]
            })

        self.cycles = history

        return history


# ============================================================
# 🔎 INTENT ENGINE
# ============================================================

class IntentEngine:

    def detect(self, text):

        clean = text.lower().strip()

        if (
            "biblia" in clean
            or "versículo" in clean
            or "versiculo" in clean
            or "pasaje bíblico" in clean
            or "pasaje biblico" in clean
            or re.search(
                r"\b(juan|mateo|marcos|lucas|salmos|filipenses)\s+\d+",
                clean
            )
        ):

            return "BIBLE"

        if any(
            word in clean
            for word in [
                "traduce",
                "traducir",
                "traducción",
                "traduccion"
            ]
        ):

            return "TRANSLATE"

        if any(
            word in clean
            for word in [
                "recuerda",
                "recuerdas",
                "memoria"
            ]
        ):

            return "MEMORY"

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

            return "STATUS"

        if any(
            word in clean
            for word in [
                "aprende",
                "aprendizaje",
                "guarda esto"
            ]
        ):

            return "LEARN"

        if any(
            word in clean
            for word in [
                "canción",
                "cancion",
                "worship",
                "música",
                "musica",
                "beat"
            ]
        ):

            return "MUSIC"

        return "CHAT"


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

            information = "\n".join(
                f"• {item['topic']}: "
                f"{item['information']}"
                for item in knowledge
            )

            return (
                "⚛️ PROTÓN encontró conocimiento:\n\n"
                + information
            )

        if memories:

            return (
                "🌀 NEUTRÓN encontró "
                "recuerdos relacionados."
            )

        return (
            "🧠 Omega recibió la orden: "
            + question
            + "\n\n"
            "No tengo todavía conocimiento "
            "suficiente para responderla con precisión."
        )


# ============================================================
# 🔊 VOICE BRIDGE
# NO usa st.components.v2.html()
# ============================================================

def voice_bridge(text):

    safe_text = json.dumps(
        str(text),
        ensure_ascii=False
    )

    component = f"""
    <div style="
        padding:14px;
        border-radius:14px;
        border:1px solid rgba(128,128,128,.35);
        text-align:center;
        font-family:sans-serif;
    ">

        <button id="omega-speak"
            style="
                width:100%;
                padding:13px;
                border-radius:10px;
                border:0;
                cursor:pointer;
                font-size:18px;
            ">
            🔊 HABLAR — CEREBRO OMEGA
        </button>

        <button id="omega-stop"
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

        <div id="omega-voice"
            style="
                margin-top:9px;
                font-size:13px;
                opacity:.75;
            ">
            🔊 VOICE: STANDBY
        </div>
    </div>

    <script>

    const omegaText = {safe_text};

    function getVoice() {{

        const voices =
            window.speechSynthesis.getVoices();

        const spanish =
            voices.filter(
                voice =>
                    voice.lang &&
                    voice.lang
                        .toLowerCase()
                        .startsWith("es")
            );

        if (!spanish.length)
            return null;

        const hints = [
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
                hints.some(
                    hint =>
                        name.includes(hint)
                )
            ) {{
                return voice;
            }}
        }}

        return spanish[0];
    }}

    function speakOmega() {{

        const status =
            document.getElementById(
                "omega-voice"
            );

        if (
            !window.speechSynthesis ||
            !window.SpeechSynthesisUtterance
        ) {{

            status.innerText =
                "❌ VOICE: navegador no compatible";

            return;
        }}

        window.speechSynthesis.cancel();

        const utterance =
            new SpeechSynthesisUtterance(
                omegaText
            );

        const voice = getVoice();

        if (voice) {{
            utterance.voice = voice;
            utterance.lang = voice.lang;
        }} else {{
            utterance.lang = "es-ES";
        }}

        utterance.rate = 0.92;

        // Voz más grave.
        utterance.pitch = 0.72;

        utterance.volume = 1.0;

        utterance.onstart = () => {{

            status.innerText =
                "🎙️ VOICE: OMEGA HABLANDO";
        }};

        utterance.onend = () => {{

            status.innerText =
                "✅ VOICE: LISTO";
        }};

        utterance.onerror = event => {{

            status.innerText =
                "⚠️ VOICE: " +
                event.error;
        }};

        window.speechSynthesis.speak(
            utterance
        );
    }}

    document
        .getElementById(
            "omega-speak"
        )
        .onclick = speakOmega;

    document
        .getElementById(
            "omega-stop"
        )
        .onclick = () => {{

            window.speechSynthesis.cancel();

            document
                .getElementById(
                    "omega-voice"
                )
                .innerText =
                "⏹️ VOICE: DETENIDA";
        }};

    </script>
    """

    # IMPORTANTE:
    # Esta es la corrección del AttributeError.
    st.html(component)


# ============================================================
# 🧠 CEREBRO OMEGA
# COORDINADOR
# ============================================================

class CerebroOmega:

    def __init__(self):

        self.proton = Proton()

        self.electron = Electron()

        self.neutron = Neutron()

        self.language = LanguageEngine()

        self.bible = BibleEngine()

        self.music = MusicEngine()

        self.evolution = EvolutionEngine()

        self.intent = IntentEngine()

        self.reason = ReasonEngine()

        self.cycles = 0

    def execute(
        self,
        user_input
    ):

        self.cycles += 1

        # ⚡ ELECTRÓN recibe TODA orden.
        electron_result = \
            self.electron.execute(
                "PROCESS_INPUT",
                user_input
            )

        if not electron_result["success"]:

            # El fallo de Electrón no mata
            # los demás módulos.
            pass

        action = self.intent.detect(
            user_input
        )

        # ====================================================
        # 📖 BIBLIA
        # ====================================================

        if action == "BIBLE":

            reference = \
                extract_bible_reference(
                    user_input
                )

            if not reference:

                return {
                    "text":
                    "Dime el pasaje. "
                    "Ejemplo: Juan 3:16."
                }

            result = \
                self.bible.get_passage(
                    reference
                )

            if result["success"]:

                response = (
                    f"📖 {result['reference']}\n\n"
                    f"{result['text']}"
                )

                self.neutron.remember(
                    user_input,
                    response
                )

                return {
                    "text": response
                }

            return {
                "text":
                "No pude obtener el pasaje: "
                + result["error"]
            }

        # ====================================================
        # 🌐 TRADUCCIÓN
        # ====================================================

        if action == "TRANSLATE":

            target = detect_language(
                user_input
            )

            text = \
                extract_translation_text(
                    user_input
                )

            if not text:

                return {
                    "text":
                    "Dime qué texto quieres "
                    "traducir y el idioma."
                }

            result = \
                self.language.translate(
                    text,
                    target=target
                )

            if result["success"]:

                response = result["text"]

                self.neutron.remember(
                    user_input,
                    response
                )

                return {
                    "text": response
                }

            return {
                "text":
                "⚠️ Traducción no disponible: "
                + result["error"]
            }

        # ====================================================
        # 💾 MEMORIA
        # ====================================================

        if action == "MEMORY":

            memories = \
                self.neutron.recall(
                    None,
                    10
                )

            if not memories:

                return {
                    "text":
                    "🌀 Neutrón todavía no tiene "
                    "recuerdos."
                }

            return {
                "text":
                json.dumps(
                    memories,
                    ensure_ascii=False,
                    indent=2
                )
            }

        # ====================================================
        # 🩺 ESTADO
        # ====================================================

        if action == "STATUS":

            return {
                "text":
                json.dumps(
                    self.status(),
                    ensure_ascii=False,
                    indent=2
                )
            }

        # ====================================================
        # 🧬 APRENDIZAJE
        # ====================================================

        if action == "LEARN":

            topic, information = \
                extract_learning(
                    user_input
                )

            if not topic:

                return {
                    "text":
                    "Usa:\n"
                    "aprende [tema]: [información]"
                }

            result = self.proton.learn(
                topic,
                information
            )

            if result["success"]:

                self.neutron.remember(
                    user_input,
                    "Aprendido: " + topic
                )

                return {
                    "text":
                    f"⚛️ Protón aprendió: "
                    f"{topic}"
                }

            return {
                "text":
                "Protón tuvo un error: "
                + result["error"]
            }

        # ====================================================
        # 🎵 MÚSICA / EVOLUCIÓN
        # ====================================================

        if action == "MUSIC":

            bpm = extract_bpm(
                user_input
            )

            history = \
                self.evolution.evolve(
                    user_input,
                    bpm=bpm,
                    possibilities=8,
                    cycles=4
                )

            plan = \
                self.music.create_plan(
                    bpm
                )

            response = \
                build_music_response(
                    user_input,
                    history,
                    plan,
                    bpm
                )

            self.neutron.remember(
                user_input,
                response
            )

            return {
                "text": response
            }

        # ====================================================
        # 🧠 CHAT + PROTÓN + NEUTRÓN
        # ====================================================

        knowledge = \
            self.proton.search(
                user_input
            )

        memories = \
            self.neutron.recall(
                user_input,
                5
            )

        response = \
            self.reason.reason(
                user_input,
                knowledge,
                memories
            )

        self.neutron.remember(
            user_input,
            response
        )

        return {
            "text": response
        }

    def status(self):

        return {

            "🧠 CEREBRO":
                "ONLINE",

            "⚛️ PROTÓN":
                self.proton.status_report(),

            "⚡ ELECTRÓN":
                self.electron.status_report(),

            "🌀 NEUTRÓN":
                self.neutron.status_report(),

            "🌐 LANGUAGE":
                self.language.status,

            "📖 BIBLE":
                self.bible.status,

            "🎵 MUSIC":
                self.music.status,

            "♾️ EVOLUTION":
                self.evolution.status,

            "🌀 CICLOS":
                self.cycles
        }


# ============================================================
# 🔧 PARSERS
# ============================================================

def extract_bible_reference(text):

    pattern = r"""
        (
            genesis|exodo|éxodo|
            mateo|marcos|lucas|juan|
            hechos|romanos|
            salmos?|proverbios|
            isaías|isaias|
            jeremías|jeremias|
            filipenses|santiago|
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

    return (
        f"{match.group(1)} "
        f"{match.group(2)}"
    )


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
        r"(?:aprende|guarda esto)\s+(.+?):\s*(.+)",
        text,
        re.IGNORECASE
    )

    if not match:

        return None, None

    return (
        match.group(1).strip(),
        match.group(2).strip()
    )


def extract_bpm(text):

    match = re.search(
        r"(\d{2,3})\s*bpm",
        text.lower()
    )

    if match:

        return max(
            40,
            min(
                int(match.group(1)),
                220
            )
        )

    return 72


# ============================================================
# 🎵 RESPUESTA EVOLUTIVA
# ============================================================

def build_music_response(
    objective,
    history,
    plan,
    bpm
):

    output = []

    output.append(
        "🧠 CEREBRO OMEGA ♾️"
    )

    output.append(
        "Generador evolutivo de posibilidades"
    )

    output.append("")

    output.append(
        f"🎯 Objetivo\n{objective}"
    )

    output.append("")

    output.append(
        "♾️ Posibilidades por ciclo: 8"
    )

    output.append(
        "🌀 Ciclos evolutivos: 4"
    )

    output.append("")

    for cycle in history:

        output.append(
            f"🌀 CICLO {cycle['cycle']}"
        )

        output.append(
            f"♾️ Generadas: "
            f"{len(cycle['generated'])}"
        )

        output.append(
            f"🏆 Seleccionadas: "
            f"{len(cycle['selected'])}"
        )

        output.append(
            f"📊 Promedio: "
            f"{cycle['average']}"
        )

        output.append(
            f"📈 Máximo: "
            f"{cycle['maximum']}"
        )

        output.append(
            f"📉 Mínimo: "
            f"{cycle['minimum']}"
        )

        output.append("")

        for index, item in enumerate(
            cycle["selected"],
            1
        ):

            output.append(
                f"{index}. "
                f"{item['idea']} | "
                f"{item['BPM']} BPM | "
                f"⭐ {item['score']}"
            )

        output.append("")

    output.append(
        "🎵 MOTOR MUSICAL"
    )

    output.append(
        f"BPM: {plan['BPM']}"
    )

    output.append(
        f"Tonalidad: "
        f"{plan['Tonalidad']}"
    )

    output.append(
        f"Progresión: "
        f"{plan['Progresión']}"
    )

    output.append("")

    output.append(
        "🔒 REGLA DEL CICLO:"
    )

    output.append(
        f"El BPM solicitado ({bpm}) "
        "se mantiene durante la evolución."
    )

    return "\n".join(output)


# ============================================================
# 🚀 INICIALIZACIÓN
# ============================================================

if "omega" not in st.session_state:

    st.session_state.omega = \
        CerebroOmega()

if "last_response" not in st.session_state:

    st.session_state.last_response = ""


omega = st.session_state.omega


# ============================================================
# 🖥️ INTERFAZ
# ============================================================

st.title(
    "🧠 CEREBRO OMEGA ♾️"
)

st.caption(
    "⚛️ Conocimiento • ⚡ Ejecución • "
    "🌀 Memoria • 🎵 Evolución • 🔊 Voz"
)


# ============================================================
# ESTADO DE LOS MOTORES
# ============================================================

status = omega.status()

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.metric(
        "🧠 CEREBRO",
        status["🧠 CEREBRO"]
    )

with c2:
    st.metric(
        "⚛️ PROTÓN",
        status["⚛️ PROTÓN"]["status"]
    )

with c3:
    st.metric(
        "⚡ ELECTRÓN",
        status["⚡ ELECTRÓN"]["status"]
    )

with c4:
    st.metric(
        "🌀 NEUTRÓN",
        status["🌀 NEUTRÓN"]["status"]
    )

with c5:
    st.metric(
        "🎵 MÚSICA",
        status["🎵 MUSIC"]
    )

with c6:
    st.metric(
        "🔊 VOICE",
        "READY"
    )


# ============================================================
# ENTRADA
# ============================================================

st.subheader(
    "🎯 Dale una orden a CEREBRO OMEGA"
)

user_input = st.text_area(
    "Entrada",
    placeholder=(
        "Escribe una orden...\n\n"
        "Ejemplo:\n"
        "Escribe una canción worship cristiana 72bpm\n\n"
        "O:\n"
        "Léeme Juan 3:16\n\n"
        "O:\n"
        "Traduce Dios es amor al inglés"
    ),
    height=160,
    label_visibility="collapsed"
)


if st.button(
    "🧠 EJECUTAR ORDEN",
    type="primary",
    use_container_width=True
):

    if user_input.strip():

        with st.spinner(
            "⚡ Electrón ejecutando • "
            "⚛️ Protón procesando • "
            "🌀 Neutrón recordando..."
        ):

            try:

                result = omega.execute(
                    user_input
                )

                st.session_state.last_response = \
                    result["text"]

            except Exception as error:

                st.session_state.last_response = (
                    "⚠️ CEREBRO detectó un error "
                    "sin apagar los módulos.\n\n"
                    f"{type(error).__name__}: "
                    f"{error}"
                )


# ============================================================
# RESPUESTA
# ============================================================

if st.session_state.last_response:

    st.divider()

    st.subheader(
        "🧠 RESPUESTA DE OMEGA"
    )

    st.write(
        st.session_state.last_response
    )

    st.subheader(
        "🔊 VOICE BRIDGE"
    )

    try:

        voice_bridge(
            st.session_state.last_response
        )

    except Exception:

        st.warning(
            "🔊 Voice está en STANDBY. "
            "Los motores cognitivos continúan activos."
        )


# ============================================================
# DIAGNÓSTICO
# ============================================================

with st.expander(
    "🩺 DIAGNÓSTICO COMPLETO"
):

    st.json(
        omega.status()
    )


# ============================================================
# HISTORIAL EVOLUTIVO
# ============================================================

if omega.evolution.cycles:

    with st.expander(
        "♾️ CICLOS EVOLUTIVOS"
    ):

        for cycle in \
            omega.evolution.cycles:

            st.markdown(
                f"### 🌀 CICLO "
                f"{cycle['cycle']}"
            )

            st.write(
                f"Generadas: "
                f"{len(cycle['generated'])}"
            )

            st.write(
                f"Seleccionadas: "
                f"{len(cycle['selected'])}"
            )

            st.write(
                f"Promedio: "
                f"{cycle['average']}"
            )

            for item in \
                cycle["selected"]:

                st.write(
                    f"🧬 {item['idea']} — "
                    f"{item['BPM']} BPM — "
                    f"⭐ {item['score']}"
                )
