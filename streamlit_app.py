import streamlit as st
import json
import os
import importlib
from datetime import datetime


# ============================================================
# CEREBRO OMEGA ∞
# LIDERAZGO CENTRAL
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide",
)


# ============================================================
# IDENTIDAD
# ============================================================

NOMBRE = "CEREBRO OMEGA ∞"
VERSION = "LIDERAZGO 1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "omega_data")

MEMORIA_FILE = os.path.join(DATA_DIR, "memoria_omega.json")
EXPERIENCIAS_FILE = os.path.join(DATA_DIR, "experiencias_omega.json")
ESTADO_FILE = os.path.join(DATA_DIR, "estado_omega.json")

os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================
# JSON SEGURO
# ============================================================

def leer_json(ruta, defecto):

    try:

        if not os.path.exists(ruta):
            return defecto

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(archivo)

        return datos

    except Exception:

        return defecto


def guardar_json(ruta, datos):

    try:

        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                datos,
                archivo,
                ensure_ascii=False,
                indent=2,
                default=str
            )

        return True

    except Exception:

        return False


# ============================================================
# MEMORIA
# ============================================================

def cargar_memoria():

    memoria = leer_json(
        MEMORIA_FILE,
        []
    )

    if not isinstance(memoria, list):
        memoria = []

    return memoria


def guardar_memoria(memoria):

    return guardar_json(
        MEMORIA_FILE,
        memoria
    )


def aprender(contenido, tipo="conocimiento"):

    memoria = cargar_memoria()

    nueva_memoria = {
        "id": len(memoria) + 1,
        "tipo": tipo,
        "contenido": str(contenido),
        "fecha": datetime.now().isoformat()
    }

    memoria.append(nueva_memoria)

    guardar_memoria(memoria)

    return nueva_memoria


# ============================================================
# EXPERIENCIAS
# ============================================================

def cargar_experiencias():

    experiencias = leer_json(
        EXPERIENCIAS_FILE,
        []
    )

    if not isinstance(experiencias, list):
        experiencias = []

    return experiencias


def registrar_experiencia(
    orden,
    resultado,
    origen="CEREBRO OMEGA"
):

    experiencias = cargar_experiencias()

    experiencia = {
        "id": len(experiencias) + 1,
        "fecha": datetime.now().isoformat(),
        "orden": str(orden),
        "resultado": str(resultado),
        "origen": origen
    }

    experiencias.append(experiencia)

    guardar_json(
        EXPERIENCIAS_FILE,
        experiencias
    )

    return experiencia


# ============================================================
# ESTADO
# ============================================================

def cargar_estado():

    estado = leer_json(
        ESTADO_FILE,
        {}
    )

    if not isinstance(estado, dict):
        estado = {}

    valores = {
        "activo": True,
        "ciclos": 0,
        "ultima_orden": "",
        "ultimo_resultado": "",
        "ultima_actualizacion": ""
    }

    for clave, valor in valores.items():

        if clave not in estado:
            estado[clave] = valor

    return estado


def guardar_estado(estado):

    guardar_json(
        ESTADO_FILE,
        estado
    )


# ============================================================
# SISTEMA DE MÓDULOS
# ============================================================

def buscar_archivos_modulos():

    ruta = os.path.join(
        BASE_DIR,
        "modules"
    )

    if not os.path.isdir(ruta):

        return []

    archivos = []

    for nombre in os.listdir(ruta):

        if (
            nombre.endswith(".py")
            and not nombre.startswith("_")
        ):

            archivos.append(
                nombre[:-3]
            )

    return sorted(archivos)


# ============================================================
# CARGAR UN MÓDULO SIN ROMPER EL CEREBRO
# ============================================================

def cargar_modulo(nombre):

    resultado = {
        "nombre": nombre,
        "activo": False,
        "modulo": None,
        "error": None
    }

    try:

        modulo = importlib.import_module(
            "modules." + nombre
        )

        resultado["modulo"] = modulo
        resultado["activo"] = True

    except Exception as error:

        resultado["error"] = (
            type(error).__name__
            + ": "
            + str(error)
        )

    return resultado


# ============================================================
# CARGAR TODOS LOS MÓDULOS
# ============================================================

def cargar_sistema_modular():

    sistema = []

    nombres = buscar_archivos_modulos()

    for nombre in nombres:

        sistema.append(
            cargar_modulo(nombre)
        )

    return sistema


# ============================================================
# ALIMENTADOR OMEGA
#
# IMPORTACIÓN SEGURA
#
# NO SE EJECUTA AUTOMÁTICAMENTE.
# NO ESCRIBE EN MEMORIA.
# ============================================================

def obtener_alimentador():

    try:

        modulo = importlib.import_module(
            "modules.alimentador"
        )

        clase = getattr(
            modulo,
            "AlimentadorOmega",
            None
        )

        if clase is None:

            return None, (
                "Existe modules.alimentador "
                "pero no se encontró "
                "AlimentadorOmega."
            )

        try:

            objeto = clase()

        except Exception as error:

            return None, (
                "AlimentadorOmega existe, "
                "pero necesita una configuración "
                "que este liderazgo no puede "
                "adivinar todavía. "
                f"{type(error).__name__}: {error}"
            )

        return objeto, None

    except Exception as error:

        return None, (
            f"{type(error).__name__}: {error}"
        )


# ============================================================
# RECORDAR
# ============================================================

def buscar_recuerdos(orden):

    memoria = cargar_memoria()

    if not memoria:
        return []

    palabras = [
        palabra.lower()
        for palabra in orden.split()
        if len(palabra) >= 4
    ]

    encontrados = []

    for recuerdo in memoria:

        contenido = str(
            recuerdo.get(
                "contenido",
                ""
            )
        ).lower()

        puntos = 0

        for palabra in palabras:

            if palabra in contenido:
                puntos += 1

        if puntos > 0:

            encontrados.append(
                (
                    puntos,
                    recuerdo
                )
            )

    encontrados.sort(
        key=lambda elemento: elemento[0],
        reverse=True
    )

    return [
        recuerdo
        for puntos, recuerdo
        in encontrados[:10]
    ]


# ============================================================
# CICLO DE CEREBRO OMEGA
# ============================================================

def ejecutar_ciclo(orden):

    estado = cargar_estado()

    estado["ciclos"] += 1
    estado["ultima_orden"] = orden
    estado["ultima_actualizacion"] = (
        datetime.now().isoformat()
    )

    # --------------------------------------------------------
    # FASE 1 — RECORDAR
    # --------------------------------------------------------

    recuerdos = buscar_recuerdos(
        orden
    )

    # --------------------------------------------------------
    # FASE 2 — ANALIZAR
    # --------------------------------------------------------

    sistema = cargar_sistema_modular()

    modulos_activos = [
        modulo
        for modulo in sistema
        if modulo["activo"]
    ]

    modulos_fallidos = [
        modulo
        for modulo in sistema
        if not modulo["activo"]
    ]

    # --------------------------------------------------------
    # FASE 3 — GENERAR ESTADO
    # --------------------------------------------------------

    resultado = {
        "orden": orden,
        "fecha": datetime.now().isoformat(),
        "ciclo": estado["ciclos"],
        "recuerdos": recuerdos,
        "modulos_activos": [
            modulo["nombre"]
            for modulo in modulos_activos
        ],
        "modulos_fallidos": [
            {
                "nombre": modulo["nombre"],
                "error": modulo["error"]
            }
            for modulo in modulos_fallidos
        ]
    }

    # --------------------------------------------------------
    # FASE 4 — APRENDER
    # --------------------------------------------------------

    aprender(
        f"Orden recibida por CEREBRO OMEGA: {orden}",
        "experiencia"
    )

    registrar_experiencia(
        orden=orden,
        resultado=(
            "Ciclo "
            + str(estado["ciclos"])
            + " ejecutado. "
            + str(len(modulos_activos))
            + " módulos activos."
        ),
        origen="LIDERAZGO OMEGA"
    )

    # --------------------------------------------------------
    # FASE 5 — ESTADO
    # --------------------------------------------------------

    estado["ultimo_resultado"] = (
        "Ciclo ejecutado correctamente."
    )

    guardar_estado(
        estado
    )

    return resultado


# ============================================================
# INTERFAZ
# ============================================================

st.title("🧠 CEREBRO OMEGA ∞")

st.markdown(
    """
### APRENDER → RECORDAR → RAZONAR → EVOLUCIONAR → ∞

**Liderazgo central del sistema.**
"""
)


# ============================================================
# ESTADO SUPERIOR
# ============================================================

estado = cargar_estado()
memoria = cargar_memoria()
experiencias = cargar_experiencias()
sistema = cargar_sistema_modular()


activos = sum(
    1
    for modulo in sistema
    if modulo["activo"]
)

fallidos = sum(
    1
    for modulo in sistema
    if not modulo["activo"]
)


c1, c2, c3, c4 = st.columns(4)

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
        "EXPERIENCIAS",
        len(experiencias)
    )

with c4:

    st.metric(
        "CICLOS ∞",
        estado["ciclos"]
    )


st.divider()


# ============================================================
# CENTRO DE PENSAMIENTO
# ============================================================

st.subheader(
    "🧠 CENTRO DE PENSAMIENTO"
)

orden = st.text_area(
    "Dale una orden a CEREBRO OMEGA:",
    placeholder=(
        "Ejemplo: aprende esto, recuerda esto, "
        "analiza esta idea..."
    ),
    height=120
)


if st.button(
    "⚡ EJECUTAR CICLO",
    use_container_width=True
):

    if not orden.strip():

        st.warning(
            "Escribe una orden primero."
        )

    else:

        resultado = ejecutar_ciclo(
            orden.strip()
        )

        st.success(
            "Ciclo de CEREBRO OMEGA completado."
        )

        st.write(
            "### 🧠 Resultado del liderazgo"
        )

        st.write(
            "Orden:",
            resultado["orden"]
        )

        st.write(
            "Ciclo:",
            resultado["ciclo"]
        )

        st.write(
            "Módulos activos:",
            len(
                resultado[
                    "modulos_activos"
                ]
            )
        )

        if resultado["recuerdos"]:

            st.write(
                "### 📚 Recuerdos relacionados"
            )

            for recuerdo in resultado[
                "recuerdos"
            ]:

                st.info(
                    recuerdo.get(
                        "contenido",
                        ""
                    )
                )


# ============================================================
# ALIMENTADOR
# ============================================================

st.divider()

st.subheader(
    "📡 ALIMENTADOR OMEGA"
)

alimentador, error_alimentador = (
    obtener_alimentador()
)


if alimentador is not None:

    st.success(
        "AlimentadorOmega conectado."
    )

    st.caption(
        "El alimentador permanece independiente "
        "y no escribe directamente en la memoria."
    )

else:

    st.warning(
        "Alimentador no conectado."
    )

    if error_alimentador:

        st.code(
            error_alimentador
        )


# ============================================================
# MÓDULOS
# ============================================================

st.divider()

st.subheader(
    "⚙️ ARQUITECTURA MODULAR"
)

if not sistema:

    st.info(
        "No hay módulos detectados todavía."
    )

else:

    for modulo in sistema:

        nombre = modulo["nombre"]

        if modulo["activo"]:

            st.success(
                f"🟢 {nombre} — CARGADO"
            )

        else:

            with st.expander(
                f"🔴 {nombre} — ERROR"
            ):

                st.error(
                    modulo["error"]
                )


# ============================================================
# MEMORIA
# ============================================================

st.divider()

st.subheader(
    "💾 MEMORIA"
)

if memoria:

    for recuerdo in reversed(
        memoria[-20:]
    ):

        fecha = recuerdo.get(
            "fecha",
            ""
        )

        tipo = recuerdo.get(
            "tipo",
            "memoria"
        )

        contenido = recuerdo.get(
            "contenido",
            ""
        )

        with st.expander(
            f"{tipo} — {fecha}"
        ):

            st.write(
                contenido
            )

else:

    st.info(
        "La memoria está vacía."
    )


# ============================================================
# EXPERIENCIAS
# ============================================================

st.divider()

st.subheader(
    "🧬 EXPERIENCIAS DEL CEREBRO"
)

if experiencias:

    for experiencia in reversed(
        experiencias[-10:]
    ):

        with st.expander(
            "Ciclo #"
            + str(
                experiencia.get(
                    "id",
                    ""
                )
            )
        ):

            st.write(
                "**Orden:**"
            )

            st.write(
                experiencia.get(
                    "orden",
                    ""
                )
            )

            st.write(
                "**Resultado:**"
            )

            st.write(
                experiencia.get(
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

st.divider()

st.subheader(
    "🔍 DIAGNÓSTICO"
)

d1, d2, d3 = st.columns(3)

with d1:

    st.metric(
        "MÓDULOS DETECTADOS",
        len(sistema)
    )

with d2:

    st.metric(
        "MÓDULOS ACTIVOS",
        activos
    )

with d3:

    st.metric(
        "MÓDULOS CON ERROR",
        fallidos
    )


# ============================================================
# CONTROLES
# ============================================================

st.divider()

st.subheader(
    "🎛️ CONTROL"
)

if st.button(
    "🔄 RECARGAR CEREBRO",
    use_container_width=True
):

    st.rerun()


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    f"{NOMBRE} | {VERSION}"
)

st.caption(
    "Streamlit es la interfaz. "
    "El liderazgo coordina. "
    "Los módulos aportan capacidades. "
    "La memoria permanece separada."
)
