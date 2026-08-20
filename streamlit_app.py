import streamlit as st
import importlib
import inspect
import json
import traceback
from datetime import datetime


# ============================================================
# 🧠 CEREBRO OMEGA ∞
# STREAMLIT = INTERFAZ
# ORQUESTADOR = CENTRO DE COORDINACIÓN
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

ORQUESTADOR_MODULO = "modules.orquestador_omega"


# ============================================================
# CARGAR ORQUESTADOR
# ============================================================

@st.cache_resource
def cargar_orquestador():

    diagnostico = {
        "modulo": ORQUESTADOR_MODULO,
        "cargado": False,
        "clases": [],
        "metodos": [],
        "error": None
    }

    try:

        modulo = importlib.import_module(
            ORQUESTADOR_MODULO
        )

        diagnostico["cargado"] = True

        clases = []

        for nombre, objeto in inspect.getmembers(
            modulo,
            inspect.isclass
        ):

            if objeto.__module__ == modulo.__name__:

                clases.append(nombre)

        diagnostico["clases"] = clases

        # ----------------------------------------------------
        # Buscar una clase razonable
        # ----------------------------------------------------

        clase = None

        nombres_preferidos = [
            "OrquestadorOmega",
            "Orquestador",
            "OmegaOrquestador"
        ]

        for nombre in nombres_preferidos:

            if hasattr(modulo, nombre):

                posible = getattr(
                    modulo,
                    nombre
                )

                if inspect.isclass(posible):

                    clase = posible
                    break

        # ----------------------------------------------------
        # Si no encontró una clase conocida,
        # usar la primera clase propia del módulo
        # ----------------------------------------------------

        if clase is None:

            for nombre in clases:

                posible = getattr(
                    modulo,
                    nombre
                )

                if inspect.isclass(posible):

                    clase = posible
                    break

        # ----------------------------------------------------
        # Si no hay clase
        # ----------------------------------------------------

        if clase is None:

            diagnostico["error"] = (
                "El módulo existe, pero no se encontró "
                "una clase de orquestador."
            )

            return None, diagnostico

        # ----------------------------------------------------
        # Crear instancia
        # ----------------------------------------------------

        instancia = clase()

        diagnostico["clase"] = clase.__name__

        diagnostico["metodos"] = [
            nombre
            for nombre in dir(instancia)
            if not nombre.startswith("_")
            and callable(
                getattr(instancia, nombre, None)
            )
        ]

        return instancia, diagnostico

    except Exception as error:

        diagnostico["error"] = str(error)

        diagnostico["traceback"] = (
            traceback.format_exc()
        )

        return None, diagnostico


orquestador, diagnostico = cargar_orquestador()


# ============================================================
# FUNCIÓN PARA EJECUTAR EL ORQUESTADOR
# ============================================================

def ejecutar_orquestador(
    orquestador,
    orden
):

    if orquestador is None:

        return {
            "ok": False,
            "error": (
                "El orquestador no está disponible."
            )
        }

    # --------------------------------------------------------
    # Métodos habituales
    # --------------------------------------------------------

    candidatos = [
        "ejecutar",
        "procesar",
        "orquestar",
        "resolver",
        "pensar",
        "analizar",
        "run",
        "execute",
        "process"
    ]

    disponibles = []

    for nombre in candidatos:

        funcion = getattr(
            orquestador,
            nombre,
            None
        )

        if callable(funcion):

            disponibles.append(
                (
                    nombre,
                    funcion
                )
            )

    # --------------------------------------------------------
    # Si no encuentra ninguno
    # --------------------------------------------------------

    if not disponibles:

        return {

            "ok": False,

            "error": (
                "El orquestador fue cargado, "
                "pero no se encontró un método "
                "de ejecución conocido."
            ),

            "metodos": [
                nombre
                for nombre in dir(orquestador)
                if not nombre.startswith("_")
                and callable(
                    getattr(
                        orquestador,
                        nombre,
                        None
                    )
                )
            ]
        }

    errores = []

    # --------------------------------------------------------
    # Probar métodos
    # --------------------------------------------------------

    for nombre, funcion in disponibles:

        try:

            firma = inspect.signature(
                funcion
            )

            parametros = list(
                firma.parameters.values()
            )

            obligatorios = [
                p
                for p in parametros
                if (
                    p.default
                    is inspect.Parameter.empty
                    and
                    p.kind
                    in (
                        inspect.Parameter.POSITIONAL_ONLY,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD
                    )
                )
            ]

            # ------------------------------------------------
            # Sin parámetros
            # ------------------------------------------------

            if len(obligatorios) == 0:

                resultado = funcion()

            # ------------------------------------------------
            # Un parámetro
            # ------------------------------------------------

            elif len(obligatorios) == 1:

                resultado = funcion(
                    orden
                )

            # ------------------------------------------------
            # Dos o más
            # ------------------------------------------------

            else:

                contexto = {
                    "entrada": orden,
                    "origen": "streamlit",
                    "fecha": datetime.now().isoformat()
                }

                resultado = funcion(
                    orden,
                    contexto
                )

            return {

                "ok": True,

                "metodo": nombre,

                "resultado": resultado

            }

        except Exception as error:

            errores.append({

                "metodo": nombre,

                "error": str(error)

            })

    return {

        "ok": False,

        "error": (
            "Se encontraron métodos de ejecución, "
            "pero ninguno pudo procesar la orden."
        ),

        "intentos": errores

    }


# ============================================================
# CONVERTIR RESULTADOS A FORMATO MOSTRABLE
# ============================================================

def mostrar_resultado(resultado):

    try:

        st.json(
            resultado
        )

        return

    except Exception:

        pass

    st.write(
        resultado
    )


# ============================================================
# CABECERA
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
# ESTADO
# ============================================================

a, b, c, d = st.columns(4)


with a:

    if orquestador:

        st.metric(
            "ORQUESTADOR",
            "🟢 ACTIVO"
        )

    else:

        st.metric(
            "ORQUESTADOR",
            "🔴 ERROR"
        )


with b:

    if diagnostico.get("clase"):

        st.metric(
            "CLASE",
            diagnostico["clase"]
        )

    else:

        st.metric(
            "CLASE",
            "NO"
        )


with c:

    st.metric(
        "MÉTODOS",
        len(
            diagnostico.get(
                "metodos",
                []
            )
        )
    )


with d:

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
        "Investiga la inteligencia artificial, "
        "analiza su historia y crea escenarios "
        "posibles para el futuro."
    ),

    height=150
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
            "🧠 CEREBRO OMEGA está procesando..."
        ):

            resultado = ejecutar_orquestador(
                orquestador,
                orden.strip()
            )

        st.session_state[
            "resultado_omega"
        ] = resultado


# ============================================================
# RESPUESTA
# ============================================================

if "resultado_omega" in st.session_state:

    resultado = st.session_state[
        "resultado_omega"
    ]

    st.divider()

    st.subheader(
        "🧠 RESPUESTA DE CEREBRO OMEGA"
    )

    if resultado.get("ok"):

        st.success(
            "Orden procesada correctamente."
        )

        st.caption(
            "Método utilizado: "
            f"{resultado.get('metodo')}"
        )

        mostrar_resultado(
            resultado.get(
                "resultado"
            )
        )

    else:

        st.error(
            resultado.get(
                "error",
                "Error desconocido."
            )
        )

        if resultado.get(
            "metodos"
        ):

            st.write(
                "Métodos encontrados:"
            )

            st.code(
                "\n".join(
                    resultado["metodos"]
                )
            )

        if resultado.get(
            "intentos"
        ):

            st.json(
                resultado["intentos"]
            )


# ============================================================
# DIAGNÓSTICO
# ============================================================

with st.expander(
    "🔬 DIAGNÓSTICO DEL ORQUESTADOR"
):

    st.json(
        diagnostico
    )


# ============================================================
# MÓDULOS DETECTABLES
# ============================================================

with st.expander(
    "🧩 MÓDULOS DE CEREBRO OMEGA"
):

    nombres = [
        "alimentador",
        "investigador_omega",
        "motor_temporal_omega",
        "ciclo_cognitivo_omega",
        "orquestador_omega"
    ]

    resultados_modulos = {}

    for nombre in nombres:

        try:

            modulo = importlib.import_module(
                "modules." + nombre
            )

            resultados_modulos[
                nombre
            ] = "🟢 CARGADO"

        except Exception as error:

            resultados_modulos[
                nombre
            ] = "🔴 ERROR: " + str(error)

    st.json(
        resultados_modulos
    )


# ============================================================
# MEMORIA
# ============================================================

with st.expander(
    "💾 MEMORIA"
):

    archivos = [
        "memoria_omega.json",
        "memoria.json",
        "experiencias_omega.json",
        "conocimiento_omega.json"
    ]

    encontrados = {}

    for archivo in archivos:

        try:

            with open(
                archivo,
                "r",
                encoding="utf-8"
            ) as f:

                encontrados[
                    archivo
                ] = json.load(f)

        except Exception:
            pass

    if encontrados:

        for nombre, datos in encontrados.items():

            st.write(
                f"### {nombre}"
            )

            st.json(
                datos
            )

    else:

        st.info(
            "No se encontraron archivos "
            "de memoria en la raíz."
        )


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "🧠 CEREBRO OMEGA ∞ | "
    "Streamlit = interfaz | "
    "Orquestador = coordinación"
)
