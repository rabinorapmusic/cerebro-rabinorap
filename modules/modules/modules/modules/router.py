"""
CEREBRO ROUTER
Selecciona módulos según la tarea.
"""

from .registry import HUB


KEYWORDS = {

    "biologia": [
        "biología",
        "biologia",
        "célula",
        "celula",
        "organismo"
    ],

    "genetica": [
        "genética",
        "genetica",
        "ADN",
        "ARN",
        "genes",
        "mutación",
        "mutacion"
    ],

    "evolucion": [
        "evolución",
        "evolucion",
        "selección natural",
        "seleccion natural",
        "Darwin"
    ],

    "matematicas": [
        "matemática",
        "matematica",
        "calcula",
        "ecuación",
        "ecuacion",
        "número",
        "numero"
    ],

    "biblia": [
        "Biblia",
        "bíblico",
        "biblico",
        "Jesús",
        "Jesus",
        "Cristo",
        "Dios",
        "versículo",
        "versiculo"
    ],

    "musica": [
        "canción",
        "cancion",
        "rap",
        "trap",
        "dembow",
        "worship",
        "beat",
        "melodía",
        "melodia"
    ],

    "codigo": [
        "Python",
        "python",
        "código",
        "codigo",
        "programa",
        "Streamlit",
        "API"
    ],

    "web": [
        "buscar",
        "investiga",
        "internet",
        "actualidad",
        "fuente",
        "noticias"
    ]
}


def detect_modules(text):

    text_lower = text.lower()

    found = []

    for module_name, keywords in KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in text_lower:

                module = HUB.get(module_name)

                if module and module.enabled:
                    found.append(module_name)

                break

    return found


def route(text):

    modules = detect_modules(text)

    if not modules:
        return {
            "modules": [],
            "message": "No se detectó un módulo especializado."
        }

    return {
        "modules": modules,
        "message": f"CEREBRO seleccionó: {', '.join(modules)}"
    }
