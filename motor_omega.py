"""
CEREBRO OMEGA ∞
MOTOR CENTRAL

Misión:
    RECIBIR → RECORDAR → INVESTIGAR → RAZONAR
    → CRITICAR → DECIDIR → APRENDER

Este archivo NO es Streamlit.
Es el motor que puede ser utilizado por
cualquier interfaz o módulo.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE = Path(__file__).resolve().parent

DATA_DIR = BASE / "omega_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

MEMORY_FILE = DATA_DIR / "memoria.json"
EXPERIENCE_FILE = DATA_DIR / "experiencias.json"


# ============================================================
# UTILIDADES
# ============================================================

def ahora() -> str:
    return datetime.now().isoformat()


def cargar_json(
    archivo: Path,
    defecto: Any
) -> Any:

    try:

        if not archivo.exists():
            return defecto

        with open(
            archivo,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return defecto


def guardar_json(
    archivo: Path,
    datos: Any
) -> None:

    temporal = archivo.with_suffix(".tmp")

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

    temporal.replace(archivo)


# ============================================================
# MEMORIA
# ============================================================

class MemoriaOmega:

    def __init__(self):

        self.archivo = MEMORY_FILE

    def todos(self) -> List[Dict[str, Any]]:

        return cargar_json(
            self.archivo,
            []
        )

    def guardar(
        self,
        contenido: str,
        tipo: str = "aprendizaje"
    ) -> Dict[str, Any]:

        memoria = self.todos()

        registro = {
            "id": len(memoria) + 1,
            "fecha": ahora(),
            "tipo": tipo,
            "contenido": contenido
        }

        memoria.append(registro)

        guardar_json(
            self.archivo,
            memoria
        )

        return registro

    def buscar(
        self,
        consulta: str,
        limite: int = 10
    ) -> List[Dict[str, Any]]:

        memoria = self.todos()

        palabras = {
            palabra.lower()
            for palabra in re.findall(
                r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+",
                consulta
            )
            if len(palabra) >= 4
        }

        resultados = []

        for registro in memoria:

            contenido = str(
                registro.get(
                    "contenido",
                    ""
                )
            ).lower()

            puntos = sum(
                1
                for palabra in palabras
                if palabra in contenido
            )

            if puntos:

                resultados.append(
                    (puntos, registro)
                )

        resultados.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            registro
            for _, registro in resultados[:limite]
        ]


# ============================================================
# EXPERIENCIAS
# ============================================================

class ExperienciaOmega:

    def __init__(self):

        self.archivo = EXPERIENCE_FILE

    def todas(self):

        return cargar_json(
            self.archivo,
            []
        )

    def registrar(
        self,
        mision: str,
        resultado: str,
        ciclo: int,
        proveedor: str = "local"
    ):

        experiencias = self.todas()

        experiencia = {
            "ciclo": ciclo,
            "fecha": ahora(),
            "proveedor": proveedor,
            "mision": mision,
            "resultado": resultado
        }

        experiencias.append(
            experiencia
        )

        guardar_json(
            self.archivo,
            experiencias
        )

        return experiencia


# ============================================================
# INTELIGENCIA EXTERNA
# ============================================================

class InteligenciaOmega:

    def __init__(self):

        self.hf_token = (
            os.getenv("HF_TOKEN", "")
        )

        self.groq_key = (
            os.getenv("GROQ_API_KEY", "")
        )

    # --------------------------------------------------------
    # HUGGING FACE
    # --------------------------------------------------------

    def huggingface(
        self,
        system: str,
        user: str
    ) -> Optional[str]:

        if not self.hf_token:
            return None

        try:

            from huggingface_hub import (
                InferenceClient
            )

            client = InferenceClient(
                api_key=self.hf_token
            )

            respuesta = (
                client
                .chat
                .completions
                .create(
                    model="openai/gpt-oss-120b",
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
                    max_tokens=5000
                )
            )

            return (
                respuesta
                .choices[0]
                .message
                .content
            )

        except Exception:

            return None

    # --------------------------------------------------------
    # GROQ
    # --------------------------------------------------------

    def groq(
        self,
        system: str,
        user: str
    ) -> Optional[str]:

        if not self.groq_key:
            return None

        try:

            from openai import OpenAI

            cliente = OpenAI(
                api_key=self.groq_key,
                base_url=
                    "https://api.groq.com/openai/v1"
            )

            respuesta = (
                cliente
                .chat
                .completions
                .create(
                    model="openai/gpt-oss-20b",
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
                    max_tokens=5000
                )
            )

            return (
                respuesta
                .choices[0]
                .message
                .content
            )

        except Exception:

            return None

    # --------------------------------------------------------
    # MOTOR
    # --------------------------------------------------------

    def pensar(
        self,
        system: str,
        user: str
    ):

        resultado = self.huggingface(
            system,
            user
        )

        if resultado:

            return {
                "respuesta": resultado,
                "proveedor": "huggingface"
            }

        resultado = self.groq(
            system,
            user
        )

        if resultado:

            return {
                "respuesta": resultado,
                "proveedor": "groq"
            }

        return None


# ============================================================
# CEREBRO OMEGA
# ============================================================

class CerebroOmega:

    VERSION = "OMEGA ∞"

    def __init__(self):

        self.memoria = MemoriaOmega()

        self.experiencias = (
            ExperienciaOmega()
        )

        self.ia = InteligenciaOmega()

        self.ciclos = len(
            self.experiencias.todas()
        )

    # --------------------------------------------------------
    # CONTEXTO
    # --------------------------------------------------------

    def contexto(
        self,
        mision: str
    ) -> str:

        recuerdos = self.memoria.buscar(
            mision
        )

        if not recuerdos:

            return (
                "No existen recuerdos "
                "relevantes."
            )

        return "\n\n".join(
            (
                f"[{r['fecha']}]\n"
                f"{r['contenido']}"
            )
            for r in recuerdos
        )

    # --------------------------------------------------------
    # EJECUTAR CICLO
    # --------------------------------------------------------

    def ejecutar(
        self,
        mision: str
    ) -> Dict[str, Any]:

        mision = mision.strip()

        if not mision:

            return {
                "ok": False,
                "error": "Misión vacía."
            }

        self.ciclos += 1

        memoria = self.contexto(
            mision
        )

        # ====================================================
        # 1. ANÁLISIS
        # ====================================================

        analisis = self.ia.pensar(

            """
Eres el módulo analítico
de CEREBRO OMEGA ∞.

Analiza la misión recibida.
Identifica objetivos, problemas,
variables y datos faltantes.

No describas cómo analizar.
Analiza directamente.
""",

            f"""
MISIÓN:

{mision}

MEMORIA RELEVANTE:

{memoria}
"""
        )

        if not analisis:

            return self._sin_ia(
                mision
            )

        proveedor = analisis[
            "proveedor"
        ]

        # ====================================================
        # 2. RAZONAMIENTO
        # ====================================================

        razonamiento = self.ia.pensar(

            """
Eres el módulo de razonamiento
de CEREBRO OMEGA ∞.

Usa la información recibida.
Relaciona hechos.
Encuentra consecuencias.
Detecta patrones.
Distingue hechos de hipótesis.
""",

            f"""
MISIÓN:

{mision}

ANÁLISIS:

{analisis['respuesta']}

MEMORIA:

{memoria}
"""
        )

        if not razonamiento:

            return {
                "ok": False,
                "error":
                    "Falló el razonamiento."
            }

        # ====================================================
        # 3. CRÍTICA
        # ====================================================

        critica = self.ia.pensar(

            """
Eres el módulo crítico
de CEREBRO OMEGA ∞.

Busca errores en el razonamiento.

Busca:
- contradicciones
- supuestos incorrectos
- información insuficiente
- explicaciones alternativas

No seas complaciente.
""",

            razonamiento[
                "respuesta"
            ]
        )

        if not critica:

            return {
                "ok": False,
                "error":
                    "Falló la crítica."
            }

        # ====================================================
        # 4. SÍNTESIS
        # ====================================================

        sintesis = self.ia.pensar(

            """
Eres el sintetizador
de CEREBRO OMEGA ∞.

Integra análisis,
razonamiento y crítica.

Corrige errores.
Conserva incertidumbres.
Produce la mejor conclusión.
""",

            f"""
MISIÓN:

{mision}

ANÁLISIS:

{analisis['respuesta']}

RAZONAMIENTO:

{razonamiento['respuesta']}

CRÍTICA:

{critica['respuesta']}
"""
        )

        if not sintesis:

            return {
                "ok": False,
                "error":
                    "Falló la síntesis."
            }

        # ====================================================
        # 5. DECISIÓN
        # ====================================================

        decision = self.ia.pensar(

            """
Eres el módulo decisor
de CEREBRO OMEGA ∞.

Entrega la mejor respuesta
posible a la misión.

Sé concreto.
No inventes certeza.
Distingue hechos,
inferencias e incertidumbres.
""",

            sintesis[
                "respuesta"
            ]
        )

        if not decision:

            return {
                "ok": False,
                "error":
                    "Falló la decisión."
            }

        resultado = decision[
            "respuesta"
        ]

        # ====================================================
        # 6. APRENDER
        # ====================================================

        self.memoria.guardar(
            (
                f"MISIÓN:\n{mision}\n\n"
                f"RESULTADO:\n{resultado}"
            ),
            tipo="experiencia"
        )

        self.experiencias.registrar(
            mision,
            resultado,
            self.ciclos,
            proveedor
        )

        return {

            "ok": True,

            "omega": self.VERSION,

            "ciclo": self.ciclos,

            "proveedor": proveedor,

            "mision": mision,

            "analisis":
                analisis["respuesta"],

            "razonamiento":
                razonamiento["respuesta"],

            "critica":
                critica["respuesta"],

            "sintesis":
                sintesis["respuesta"],

            "resultado":
                resultado
        }

    # --------------------------------------------------------
    # MODO SIN IA
    # --------------------------------------------------------

    def _sin_ia(
        self,
        mision: str
    ):

        recuerdos = self.memoria.buscar(
            mision
        )

        return {

            "ok": False,

            "error":
                "CEREBRO OMEGA no tiene "
                "un proveedor de IA conectado.",

            "memoria_encontrada":
                recuerdos
        }

    # --------------------------------------------------------
    # ESTADO
    # --------------------------------------------------------

    def estado(self):

        return {

            "nombre":
                "CEREBRO OMEGA",

            "version":
                self.VERSION,

            "ciclos":
                self.ciclos,

            "conocimiento":
                len(
                    self.memoria.todos()
                ),

            "experiencias":
                len(
                    self.experiencias.todas()
                ),

            "ia_huggingface":
                bool(
                    self.ia.hf_token
                ),

            "ia_groq":
                bool(
                    self.ia.groq_key
                )
        }


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    cerebro = CerebroOmega()

    print()
    print(
        "🧠 CEREBRO OMEGA ∞"
    )
    print()

    print(
        json.dumps(
            cerebro.estado(),
            indent=2,
            ensure_ascii=False
        )
    )

    print()

    mision = input(
        "Misión: "
    )

    resultado = cerebro.ejecutar(
        mision
    )

    print()

    print(
        json.dumps(
            resultado,
            indent=2,
            ensure_ascii=False
        )
    )
