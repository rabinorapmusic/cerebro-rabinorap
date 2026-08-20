# streamlit_app.py
"""
╔══════════════════════════════════════════════════════════════╗
║                    CEREBRO OMEGA ∞                         ║
║                 CENTRO DE LIDERAZGO                        ║
╠══════════════════════════════════════════════════════════════╣
║ Aprende → Recuerda → Razona → Coordina → Evoluciona       ║
╚══════════════════════════════════════════════════════════════╝

Este archivo es el ORQUESTADOR principal.

No reemplaza los módulos.
No depende de un core externo.
Carga y coordina los módulos disponibles dentro de /modules.
"""

import streamlit as st
import os
import json
import importlib
import inspect
import traceback
from datetime import datetime


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA ∞",
    page_icon="🧠",
    layout="wide",
)


NOMBRE = "CEREBRO OMEGA ∞"
VERSION = "OMEGA LEADERSHIP 1.0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, "modules")
DATA_DIR = os.path.join(BASE_DIR, "omega_data")

MEMORIA_FILE = os.path.join(DATA_DIR, "memoria_omega.json")
EXPERIENCIAS_FILE = os.path.join(DATA_DIR, "experiencias_omega.json")
ESTADO_FILE = os.path.join(DATA_DIR, "estado_omega.json")


# ============================================================
# PREPARAR DIRECTORIOS
# ============================================================

os.makedirs(DATA_DIR, exist_ok=True)


# ============================================================
# UTILIDADES JSON
# ============================================================

def cargar_json(ruta, defecto):
    try:
        if not os.path.exists(ruta):
            return defecto

        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return defecto


def guardar_json(ruta, datos):
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(
                datos,
                f,
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
    return cargar_json(MEMORIA_FILE, [])


def guardar_memoria(memoria):
    return guardar_json(MEMORIA_FILE, memoria)


def aprender(texto, tipo="conocimiento"):
    memoria = cargar_memoria()

    entrada = {
        "id": len(memoria) + 1,
        "fecha": datetime.now().isoformat(),
        "tipo": tipo,
        "contenido": texto,
    }

    memoria.append(entrada)

    guardar_memoria(memoria)

    return entrada


# ============================================================
# EXPERIENCIAS
# ============================================================

def cargar_experiencias():
    return cargar_json(EXPERIENCIAS_FILE, [])


def registrar_experiencia(orden, resultado, modulo=None):
    experiencias = cargar_experiencias()

    experiencia = {
        "id": len(experiencias) + 1,
        "fecha": datetime.now().isoformat(),
        "orden": orden,
        "resultado": resultado,
        "modulo": modulo,
    }

    experiencias.append(experiencia)

    guardar_json(EXPERIENCIAS_FILE, experiencias)

    return experiencia


# ============================================================
# ESTADO DEL CEREBRO
# ============================================================

def cargar_estado():
    defecto = {
        "activo": True,
        "ciclos": 0,
        "ultima_orden": "",
        "ultimo_resultado": "",
        "ultima_actualizacion": None,
    }

    estado = cargar_json(ESTADO_FILE, defecto)

    for clave, valor in defecto.items():
        if clave not in estado:
            estado[clave] = valor

    return estado


def guardar_estado(estado):
    return guardar_json(ESTADO_FILE, estado)


# ============================================================
# DETECCIÓN DE MÓDULOS
# ============================================================

def descubrir_modulos():
    """
    Busca automáticamente archivos .py dentro de modules/.

    No obliga a que todos los módulos tengan el mismo nombre.
    """

    encontrados = []

    if not os.path.isdir(MODULES_DIR):
        return encontrados

    for archivo in os.listdir(MODULES_DIR):

        if not archivo.endswith(".py"):
            continue

        if archivo.startswith("_"):
            continue

        nombre = archivo[:-3]

        encontrados.append(nombre)

    return sorted(encontrados)


# ============================================================
# CARGADOR DE MÓDULOS
# ============================================================

def cargar_modulo(nombre):
    try:

        modulo = importlib.import_module(
            f"modules.{nombre}"
        )

        return {
            "nombre": nombre,
            "estado": "OK",
            "modulo": modulo,
            "error": None,
        }

    except Exception as e:

        return {
            "nombre": nombre,
            "estado": "ERROR",
            "modulo": None,
            "error": str(e),
        }


def cargar_todos_los_modulos():

    resultados = []

    nombres = descubrir_modulos()

    for nombre in nombres:
        resultados.append(
            cargar_modulo(nombre)
        )

    return resultados


# ============================================================
# BUSCAR CAPACIDADES
# ============================================================

def obtener_capacidades(modulo):

    capacidades = []

    try:

        for nombre, objeto in inspect.getmembers(modulo):

            if nombre.startswith("_"):
                continue

            if inspect.isfunction(objeto):
                capacidades.append(nombre)

            elif inspect.isclass(objeto):
                capacidades.append(nombre)

    except Exception:
        pass

    return capacidades


# ============================================================
# EJECUTOR INTELIGENTE
# ============================================================

def ejecutar_en_modulos(orden, modulos):

    resultados = []

    texto = orden.lower()

    for info in modulos:

        if info["estado"] != "OK":
            continue

        modulo = info["modulo"]
        nombre = info["nombre"]

        # ----------------------------------------------------
        # Intentar funciones comunes
        # ----------------------------------------------------

        candidatos = [
            "procesar",
            "ejecutar",
            "responder",
            "pensar",
            "analizar",
            "resolver",
            "alimentar",
            "consultar",
        ]

        for funcion_nombre in candidatos:

            funcion = getattr(
                modulo,
                funcion_nombre,
                None
            )

            if not callable(funcion):
                continue

            try:

                firma = inspect.signature(funcion)

                parametros = list(
                    firma.parameters.values()
                )

                if len(parametros) == 0:

                    resultado = funcion()

                else:

                    resultado = funcion(orden)

                if resultado is not None:

                    resultados.append({
                        "modulo": nombre,
                        "funcion": funcion_nombre,
                        "resultado": str(resultado),
                    })
