import streamlit as st
import json
import traceback
import importlib
from datetime import datetime


# ============================================================
# CEREBRO OMEGA ∞
# STREAMLIT = INTERFAZ
# CORE = CEREBRO
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CARGA DEL CORE
# ============================================================

@st.cache_resource
def cargar_cerebro():

    errores = []

    candidatos = [
        ("core.core", "CerebroCore"),
        ("core", "CerebroCore"),
    ]

    for modulo_nombre, clase_nombre in candidatos:

        try:

            modulo = importlib.import_module(
                modulo_nombre
            )

            clase = getattr(
                modulo,
                clase_nombre
            )

            cerebro = clase()

            return cerebro, errores

        except Exception as e:

            errores.append({
                "modulo": modulo_nombre,
                "error": str(e)
            })

    return None, errores


cerebro, errores_core = cargar_cerebro()


# ============================================================
# FUNCIONES DE APOYO
# ============================================================

def convertir_json(obj):

    try:

        json.dumps(
            obj,
            ensure_ascii=False
        )

        return obj

    except Exception:

        return str(obj)


def detectar_metodos(obj):

    if obj is None:
        return []

    metodos = []

    for nombre in dir(obj):

        if nombre.startswith("_"):
            continue

        try:

            atributo = getattr(
                obj,
                nombre
            )

            if callable(atributo):

                metodos.append(nombre)

        except Exception:
            pass

    return metodos


# ============================================================
# EJECUTOR DEL CEREBRO
# ============================================================

def ejecutar_cerebro(orden):

    if cerebro is None:

        return {
            "ok": False,
            "error": (
                "CEREBRO OMEGA no pudo cargar el CORE."
            ),
            "diagnostico": errores_core
        }


    # ========================================================
    # MÉTODOS PREFERIDOS
    # ========================================================

    metodos_preferidos = [

        "ejecutar",

        "procesar",

        "pensar",

        "responder",

        "run",

        "execute",

        "process",

        "think",

        "handle",

    ]


    disponibles = detectar_metodos(
        cerebro
    )


    # ========================================================
    # BUSCAR MÉTODO DEL CORE
    # ========================================================

    metodo_encontrado = None

    for nombre in metodos_preferidos:

        if nombre in disponibles:

            metodo_encontrado = nombre

            break


    # ========================================================
    # SI NO ENCUENTRA MÉTODO
    # ========================================================

    if metodo_encontrado is None:

        return {

            "ok": False,

            "error": (
                "El CORE fue cargado, pero no tiene "
                "un método de ejecución reconocido."
            ),

            "metodos_disponibles":
                disponibles,

        }


    # ========================================================
    # EJECUTAR
    # ========================================================

    try:

        funcion = getattr(
            cerebro,
            metodo_encontrado
        )


        resultado = funcion(
            orden
        )


        return {

            "ok": True,

            "metodo":
                metodo_encontrado,

            "resultado":
                convertir_json(resultado),

        }


    except Exception as error:

        return {

            "ok": False,

            "metodo":
                metodo_encontrado,

            "error":
                str(error),

            "traceback":
                traceback.format_exc(),

        }


# ============================================================
# IDENTIDAD
# ============================================================

st.title(
    "🧠 CEREBRO OMEGA ∞"
)

st.caption(
    "APRENDER → RECORDAR → RAZONAR → "
    "EVOLUCIONAR → ∞"
)

st.divider()


# ============================================================
# ESTADO DEL CORE
# ============================================================

if cerebro is not None:

    st.success(
        "🟢 CORE DE CEREBRO OMEGA CONECTADO"
    )

else:

    st.error(
        "🔴 CORE NO CONECTADO"
    )


# ============================================================
# ESTADO GENERAL
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "ESTADO",
        "🟢 ACTIVO"
        if cerebro
        else "🔴 ERROR"
    )


with col2:

    st.metric(
        "CORE",
        "CONECTADO"
        if cerebro
        else "NO"
    )


with col3:

    if cerebro:

        cantidad = len(
            detectar_metodos(
                cerebro
            )
        )

    else:

        cantidad = 0

    st.metric(
        "MÉTODOS CORE",
        cantidad
    )


with col4:

    st.metric(
        "HORA",
        datetime.now().strftime(
            "%H:%M:%S"
        )
    )


# ============================================================
# CENTRO DE PENSAMIENTO
# ============================================================

st.divider()

st.subheader(
    "🧠 CENTRO DE PENSAMIENTO"
)


orden = st.text_area(

    "Dale una orden a CEREBRO OMEGA:",

    placeholder=(
        "Ejemplo:\n"
        "Investiga la inteligencia artificial "
        "y analiza posibles escenarios futuros."
    ),

    height=140
)


if st.button(
    "⚡ EJECUTAR CEREBRO OMEGA",
    use_container_width=True
):

    if not orden.strip():

        st.warning(
            "Escribe una orden."
        )

    else:

        with st.spinner(
            "🧠 CEREBRO OMEGA está pensando..."
        ):

            resultado = ejecutar_cerebro(
                orden.strip()
            )


        st.session_state[
            "ultimo_resultado"
        ] = resultado


# ============================================================
# RESULTADO
# ============================================================

if "ultimo_resultado" in st.session_state:

    resultado = st.session_state[
        "ultimo_resultado"
    ]

    st.divider()

    st.subheader(
        "🧠 RESPUESTA DE CEREBRO OMEGA"
    )


    if resultado.get("ok"):

        st.success(
            "Ciclo ejecutado correctamente."
        )

        respuesta = resultado.get(
            "resultado"
        )

        if isinstance(
            respuesta,
            (dict, list)
        ):

            st.json(
                respuesta
            )

        else:

            st.write(
                respuesta
            )

    else:

        st.error(
            resultado.get(
                "error",
                "Error desconocido."
            )
        )


# ============================================================
# DIAGNÓSTICO DEL CORE
# ============================================================

with st.expander(
    "🔬 DIAGNÓSTICO DEL CORE"
):

    if cerebro is not None:

        st.write(
            "### Métodos encontrados"
        )

        st.code(
            "\n".join(
                detectar_metodos(
                    cerebro
                )
            )
        )

    else:

        st.json(
            errores_core
        )


# ============================================================
# MÓDULOS CARGADOS POR EL CORE
# ============================================================

with st.expander(
    "🧩 INFORMACIÓN DEL CORE"
):

    if cerebro is not None:

        atributos = {}

        for nombre in dir(cerebro):

            if nombre.startswith("_"):
                continue

            try:

                valor = getattr(
                    cerebro,
                    nombre
                )

                if isinstance(
                    valor,
                    (
                        str,
                        int,
                        float,
                        bool,
                        list,
                        dict,
                    )
                ):

                    atributos[nombre] = valor

            except Exception:
                pass

        st.json(
            convertir_json(
                atributos
            )
        )


# ============================================================
# MEMORIA VISUAL
# ============================================================

with st.expander(
    "💾 INFORMACIÓN DE MEMORIA"
):

    posibles_memorias = [

        "memoria_omega.json",

        "memoria.json",

        "memory.json",

    ]

    encontrada = None

    for archivo in posibles_memorias:

        try:

            with open(
                archivo,
                "r",
                encoding="utf-8"
            ) as f:

                encontrada = json.load(f)

                break

        except Exception:
            continue


    if encontrada is not None:

        st.json(
            encontrada
        )

    else:

        st.info(
            "No se encontró una memoria "
            "JSON en la raíz del proyecto."
        )


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "🧠 CEREBRO OMEGA ∞ | "
    "Streamlit funciona como interfaz. "
    "El procesamiento pertenece al CORE."
)
