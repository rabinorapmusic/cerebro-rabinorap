import streamlit as st
import json
import re
import ast
import operator
from pathlib import Path
from datetime import datetime

# ============================================================
# 🧠 CEREBRO OMEGA ∞
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide"
)

ARCHIVO = Path("omega_memoria.json")

# ============================================================
# DISEÑO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at center,
            rgba(0,255,130,.08),
            transparent 45%
        ),
        #010604;
    color:#d9ffe5;
}

header,
footer,
#MainMenu {
    visibility:hidden;
}

.omega {
    text-align:center;
    font-family:monospace;
    font-size:42px;
    font-weight:bold;
    letter-spacing:4px;
}

.infinity {
    color:#00ff88;
    font-size:72px;
    text-shadow:
        0 0 8px #00ff88,
        0 0 25px #00ff88,
        0 0 55px #00ff88;
}

.line {
    height:1px;
    margin:22px 0;
    background:linear-gradient(
        90deg,
        transparent,
        #00ff88,
        transparent
    );
}

.stButton>button {
    background:#002d16 !important;
    color:#00ff88 !important;
    border:1px solid #00ff88 !important;
    border-radius:10px !important;
    font-family:monospace !important;
}

.stButton>button:hover {
    background:#00ff88 !important;
    color:#001208 !important;
    box-shadow:0 0 25px #00ff88;
}

textarea {
    background:#010b05 !important;
    color:#caffd9 !important;
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
# MEMORIA
# ============================================================

def cargar_memoria():

    if not ARCHIVO.exists():
        return []

    try:
        with open(
            ARCHIVO,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except Exception:
        return []


def guardar_memoria(datos):

    with open(
        ARCHIVO,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            datos,
            f,
            ensure_ascii=False,
            indent=2
        )


def aprender(texto):

    datos = cargar_memoria()

    datos.append({
        "fecha": datetime.now().isoformat(),
        "contenido": texto
    })

    guardar_memoria(datos)


def buscar_recuerdo(palabras):

    datos = cargar_memoria()

    resultados = []

    for item in datos:

        contenido = item["contenido"].lower()

        puntos = 0

        for palabra in palabras:

            if palabra in contenido:
                puntos += 1

        if puntos:
            resultados.append(
                (puntos, item)
            )

    resultados.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        item
        for _, item in resultados[:5]
    ]

# ============================================================
# CALCULADORA SEGURA
# ============================================================

OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}


def calcular_nodo(nodo):

    if isinstance(
        nodo,
        ast.Constant
    ):

        if isinstance(
            nodo.value,
            (int, float)
        ):
            return nodo.value

        raise ValueError()

    if isinstance(
        nodo,
        ast.UnaryOp
    ):

        valor = calcular_nodo(
            nodo.operand
        )

        if isinstance(
            nodo.op,
            ast.USub
        ):
            return -valor

        if isinstance(
            nodo.op,
            ast.UAdd
        ):
            return valor

        raise ValueError()

    if isinstance(
        nodo,
        ast.BinOp
    ):

        izquierda = calcular_nodo(
            nodo.left
        )

        derecha = calcular_nodo(
            nodo.right
        )

        operador = OPERADORES.get(
            type(nodo.op)
        )

        if not operador:
            raise ValueError()

        return operador(
            izquierda,
            derecha
        )

    raise ValueError()


def calcular(expresion):

    expresion = expresion.replace(
        "^",
        "**"
    )

    arbol = ast.parse(
        expresion,
        mode="eval"
    )

    return calcular_nodo(
        arbol.body
    )

# ============================================================
# MOTOR OMEGA
# ============================================================

def ejecutar(mision):

    texto = mision.strip()

    bajo = texto.lower()

    # --------------------------------------------------------
    # MEMORIA
    # --------------------------------------------------------

    if (
        bajo.startswith("recuerda ")
        or bajo.startswith("recuerda:")
        or bajo.startswith("aprende ")
        or bajo.startswith("aprende:")
    ):

        contenido = re.sub(
            r"^(recuerda|aprende)\s*:?\s*",
            "",
            texto,
            flags=re.I
        )

        aprender(contenido)

        return (
            "He guardado en la memoria:\n\n"
            + contenido
        )

    # --------------------------------------------------------
    # BUSCAR MEMORIA
    # --------------------------------------------------------

    if (
        "qué recuerdas" in bajo
        or "que recuerdas" in bajo
        or "busca en tu memoria" in bajo
    ):

        palabras = [
            p.lower()
            for p in re.findall(
                r"[a-záéíóúñ0-9]+",
                bajo
            )
            if len(p) > 3
        ]

        recuerdos = buscar_recuerdo(
            palabras
        )

        if not recuerdos:
            return (
                "No encontré recuerdos "
                "relacionados."
            )

        return "\n\n".join(
            "• " + x["contenido"]
            for x in recuerdos
        )

    # --------------------------------------------------------
    # CALCULADORA
    # --------------------------------------------------------

    candidato = re.sub(
        r"^(calcula|calcular|cuánto es|cuanto es)\s*",
        "",
        texto,
        flags=re.I
    )

    if re.fullmatch(
        r"[0-9+\-*/().%^ \t]+",
        candidato
    ):

        try:

            resultado = calcular(
                candidato
            )

            return (
                f"Resultado: **{resultado}**"
            )

        except Exception:
            pass

    # --------------------------------------------------------
    # HORA
    # --------------------------------------------------------

    if (
        "qué hora" in bajo
        or "que hora" in bajo
    ):

        return (
            "Hora del sistema: "
            + datetime.now().strftime(
                "%H:%M:%S"
            )
        )

    # --------------------------------------------------------
    # FECHA
    # --------------------------------------------------------

    if (
        "qué fecha" in bajo
        or "que fecha" in bajo
        or "qué día" in bajo
        or "que dia" in bajo
    ):

        return (
            "Fecha del sistema: "
            + datetime.now().strftime(
                "%d/%m/%Y"
            )
        )

    # --------------------------------------------------------
    # ANÁLISIS BÁSICO
    # --------------------------------------------------------

    palabras = re.findall(
        r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+",
        texto
    )

    palabras_limpias = [
        p.lower()
        for p in palabras
        if len(p) > 3
    ]

    recuerdos = buscar_recuerdo(
        palabras_limpias
    )

    respuesta = (
        "He procesado tu orden.\n\n"
        f"**Misión recibida:**\n{texto}\n\n"
    )

    if recuerdos:

        respuesta += (
            "**Recuerdos relacionados:**\n"
        )

        for item in recuerdos:

            respuesta += (
                "• "
                + item["contenido"]
                + "\n"
            )

    else:

        respuesta += (
            "**Memoria relacionada:** "
            "no encontré información previa.\n"
        )

    respuesta += (
        "\n**Estado:** "
        "CEREBRO OMEGA ha completado "
        "el ciclo de procesamiento."
    )

    return respuesta

# ============================================================
# ESTADÍSTICAS
# ============================================================

memoria = cargar_memoria()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "ESTADO",
        "🟢 ACTIVO"
    )

with c2:
    st.metric(
        "CONOCIMIENTO",
        len(memoria)
    )

with c3:
    st.metric(
        "CICLOS ∞",
        st.session_state.get(
            "ciclos",
            0
        )
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

orden = st.text_area(
    "Dale una orden a CEREBRO OMEGA:",
    height=140,
    placeholder=(
        "Ejemplos:\n"
        "Recuerda que mi proyecto se llama CEREBRO OMEGA\n"
        "¿Qué recuerdas de mi proyecto?\n"
        "Calcula 25 * 37\n"
        "Analiza esta idea..."
    )
)

if st.button(
    "⚡ EJECUTAR CICLO",
    use_container_width=True
):

    if orden.strip():

        st.session_state.ciclos = (
            st.session_state.get(
                "ciclos",
                0
            ) + 1
        )

        with st.spinner(
            "🧠 CEREBRO OMEGA ∞"
        ):

            respuesta = ejecutar(
                orden
            )

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        st.markdown(
            respuesta
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.warning(
            "Escribe una orden."
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

memoria = cargar_memoria()

if memoria:

    for item in reversed(
        memoria[-10:]
    ):

        st.write(
            "• "
            + item["contenido"]
        )

else:

    st.write(
        "La memoria está vacía."
    )

# ============================================================
# CONTROL
# ============================================================

st.markdown(
    '<div class="line"></div>',
    unsafe_allow_html=True
)

if st.button(
    "🗑️ BORRAR MEMORIA",
    use_container_width=True
):

    if ARCHIVO.exists():
        ARCHIVO.unlink()

    st.rerun()
