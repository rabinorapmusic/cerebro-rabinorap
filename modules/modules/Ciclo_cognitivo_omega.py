"""
╔══════════════════════════════════════════════════════════════╗
║                    CEREBRO OMEGA ∞                         ║
║                CICLO COGNITIVO OMEGA                      ║
╠══════════════════════════════════════════════════════════════╣
║ ENTRADA → ANÁLISIS → CONOCIMIENTO → RAZONAMIENTO →        ║
║ MEMORIA → EVALUACIÓN → EXPERIENCIA → APRENDIZAJE → ∞     ║
╚══════════════════════════════════════════════════════════════╝

Este módulo NO reemplaza el CORE.
NO reemplaza el ORQUESTADOR.
NO modifica los módulos existentes.

Su función es crear un ciclo cognitivo común entre ellos.
"""

from __future__ import annotations

import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class CicloCognitivoOmega:
    """
    Motor de integración cognitiva de CEREBRO OMEGA.

    Coordina:
        - entrada
        - análisis
        - conocimiento
        - memoria
        - razonamiento
        - evaluación
        - experiencia
        - aprendizaje
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        memoria_path: str = "memoria_omega.json",
        experiencias_path: str = "experiencias_omega.json",
        conocimiento_path: str = "conocimiento_omega.json",
        max_experiencias: int = 5000,
    ):
        self.memoria_path = Path(memoria_path)
        self.experiencias_path = Path(experiencias_path)
        self.conocimiento_path = Path(conocimiento_path)

        self.max_experiencias = max_experiencias

        self.estado = {
            "activo": True,
            "ciclos": 0,
            "ultimo_ciclo": None,
            "aprendizajes": 0,
            "errores": 0,
        }

        self.memoria = self._cargar_json(
            self.memoria_path,
            {"recuerdos": []}
        )

        self.experiencias = self._cargar_json(
            self.experiencias_path,
            {"experiencias": []}
        )

        self.conocimiento = self._cargar_json(
            self.conocimiento_path,
            {"conocimientos": []}
        )

    # ==========================================================
    # ARCHIVOS
    # ==========================================================

    def _cargar_json(
        self,
        archivo: Path,
        defecto: Dict[str, Any]
    ) -> Dict[str, Any]:

        try:
            if archivo.exists():
                with open(archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)

                if isinstance(datos, dict):
                    return datos

        except Exception:
            pass

        return defecto.copy()

    def _guardar_json(
        self,
        archivo: Path,
        datos: Dict[str, Any]
    ) -> bool:

        try:
            archivo.parent.mkdir(parents=True, exist_ok=True)

            temporal = archivo.with_suffix(
                archivo.suffix + ".tmp"
            )

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

            return True

        except Exception:
            self.estado["errores"] += 1
            return False

    # ==========================================================
    # IDENTIDAD DEL CICLO
    # ==========================================================

    def _id_ciclo(self, entrada: str) -> str:

        contenido = (
            entrada
            + str(time.time_ns())
        ).encode("utf-8")

        return hashlib.sha256(
            contenido
        ).hexdigest()[:16]

    def _ahora(self) -> str:

        return datetime.now(
            timezone.utc
        ).isoformat()

    # ==========================================================
    # 1. ANALIZAR ENTRADA
    # ==========================================================

    def analizar_entrada(
        self,
        entrada: str
    ) -> Dict[str, Any]:

        texto = str(entrada).strip()

        palabras = texto.split()

        return {
            "entrada": texto,
            "longitud": len(texto),
            "palabras": len(palabras),
            "vacia": not bool(texto),
            "tipo": self._clasificar_entrada(texto),
        }

    def _clasificar_entrada(
        self,
        texto: str
    ) -> str:

        t = texto.lower()

        if not t:
            return "vacia"

        if any(
            x in t
            for x in [
                "investiga",
                "investigar",
                "busca",
                "averigua"
            ]
        ):
            return "investigacion"

        if any(
            x in t
            for x in [
                "pasado",
                "historia",
                "antes",
                "histórico"
            ]
        ):
            return "pasado"

        if any(
            x in t
            for x in [
                "futuro",
                "posible",
                "escenario",
                "qué pasaría"
            ]
        ):
            return "futuro"

        if any(
            x in t
            for x in [
                "aprende",
                "aprendizaje",
                "recuerda"
            ]
        ):
            return "aprendizaje"

        if any(
            x in t
            for x in [
                "analiza",
                "analizar",
                "razona",
                "razonar"
            ]
        ):
            return "razonamiento"

        return "general"

    # ==========================================================
    # 2. MEMORIA
    # ==========================================================

    def consultar_memoria(
        self,
        entrada: str,
        limite: int = 10
    ) -> List[Dict[str, Any]]:

        recuerdos = self.memoria.get(
            "recuerdos",
            []
        )

        if not recuerdos:
            return []

        palabras = {
            p.lower()
            for p in entrada.split()
            if len(p) > 2
        }

        resultados = []

        for recuerdo in recuerdos:

            texto = json.dumps(
                recuerdo,
                ensure_ascii=False
            ).lower()

            coincidencias = sum(
                1
                for palabra in palabras
                if palabra in texto
            )

            if coincidencias > 0:

                resultados.append(
                    (
                        coincidencias,
                        recuerdo
                    )
                )

        resultados.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            item[1]
            for item in resultados[:limite]
        ]

    # ==========================================================
    # 3. CONOCIMIENTO
    # ==========================================================

    def consultar_conocimiento(
        self,
        entrada: str,
        limite: int = 10
    ) -> List[Dict[str, Any]]:

        conocimientos = self.conocimiento.get(
            "conocimientos",
            []
        )

        palabras = {
            p.lower()
            for p in entrada.split()
            if len(p) > 2
        }

        resultados = []

        for conocimiento in conocimientos:

            texto = json.dumps(
                conocimiento,
                ensure_ascii=False
            ).lower()

            coincidencias = sum(
                1
                for palabra in palabras
                if palabra in texto
            )

            if coincidencias:

                resultados.append(
                    (
                        coincidencias,
                        conocimiento
                    )
                )

        resultados.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            item[1]
            for item in resultados[:limite]
        ]

    # ==========================================================
    # 4. RAZONAMIENTO BASE
    # ==========================================================

    def razonar(
        self,
        entrada: str,
        analisis: Dict[str, Any],
        memoria: List[Dict[str, Any]],
        conocimiento: List[Dict[str, Any]],
        resultados_externos: Optional[Any] = None,
    ) -> Dict[str, Any]:

        evidencia = []

        if memoria:
            evidencia.append({
                "fuente": "memoria",
                "cantidad": len(memoria),
            })

        if conocimiento:
            evidencia.append({
                "fuente": "conocimiento",
                "cantidad": len(conocimiento),
            })

        if resultados_externos:
            evidencia.append({
                "fuente": "modulos_externos",
                "disponible": True,
            })

        nivel = 0

        nivel += min(len(memoria), 5)
        nivel += min(len(conocimiento), 5)

        if resultados_externos:
            nivel += 2

        return {
            "pregunta": entrada,
            "tipo": analisis["tipo"],
            "evidencia": evidencia,
            "nivel_evidencia": nivel,
            "conclusion_base": self._conclusion_base(
                analisis,
                nivel
            ),
            "requiere_verificacion": nivel < 2,
        }

    def _conclusion_base(
        self,
        analisis: Dict[str, Any],
        nivel: int
    ) -> str:

        tipo = analisis.get(
            "tipo",
            "general"
        )

        if nivel == 0:
            return (
                "No existe suficiente evidencia interna. "
                "Se necesita investigación o conocimiento adicional."
            )

        if tipo == "investigacion":
            return (
                "La consulta requiere reunir y comparar "
                "información antes de establecer una conclusión."
            )

        if tipo == "pasado":
            return (
                "La consulta debe contrastarse con información "
                "histórica antes de establecer una conclusión."
            )

        if tipo == "futuro":
            return (
                "El futuro debe tratarse como escenarios potenciales, "
                "no como una certeza."
            )

        return (
            "Existe información relacionada disponible "
            "para construir un razonamiento."
        )

    # ==========================================================
    # 5. EVALUACIÓN
    # ==========================================================

    def evaluar(
        self,
        razonamiento: Dict[str, Any]
    ) -> Dict[str, Any]:

        evidencia = razonamiento.get(
            "nivel_evidencia",
            0
        )

        requiere = razonamiento.get(
            "requiere_verificacion",
            True
        )

        if evidencia >= 7:
            confianza = "alta"

        elif evidencia >= 3:
            confianza = "media"

        else:
            confianza = "baja"

        return {
            "confianza": confianza,
            "nivel_evidencia": evidencia,
            "requiere_verificacion": requiere,
            "estado": (
                "aceptable"
                if evidencia >= 3
                else "insuficiente"
            ),
        }

    # ==========================================================
    # 6. GUARDAR EXPERIENCIA
    # ==========================================================

    def guardar_experiencia(
        self,
        ciclo_id: str,
        entrada: str,
        resultado: Dict[str, Any]
    ) -> bool:

        experiencia = {
            "id": ciclo_id,
            "fecha": self._ahora(),
            "entrada": entrada,
            "resultado": resultado,
        }

        lista = self.experiencias.setdefault(
            "experiencias",
            []
        )

        lista.append(experiencia)

        if len(lista) > self.max_experiencias:

            self.experiencias["experiencias"] = (
                lista[-self.max_experiencias:]
            )

        return self._guardar_json(
            self.experiencias_path,
            self.experiencias
        )

    # ==========================================================
    # 7. APRENDER
    # ==========================================================

    def aprender(
        self,
        entrada: str,
        resultado: Dict[str, Any]
    ) -> Dict[str, Any]:

        evaluacion = resultado.get(
            "evaluacion",
            {}
        )

        confianza = evaluacion.get(
            "confianza",
            "baja"
        )

        aprendizaje = {
            "fecha": self._ahora(),
            "entrada": entrada,
            "tipo": resultado.get(
                "analisis",
                {}
            ).get(
                "tipo",
                "general"
            ),
            "confianza": confianza,
            "leccion": (
                resultado.get(
                    "razonamiento",
                    {}
                ).get(
                    "conclusion_base",
                    ""
                )
            ),
        }

        # Solo consolidamos como conocimiento
        # aquello que tenga evidencia suficiente.
        if confianza in ("media", "alta"):

            conocimientos = self.conocimiento.setdefault(
                "conocimientos",
                []
            )

            conocimientos.append(
                aprendizaje
            )

            self.conocimiento["conocimientos"] = (
                conocimientos[-self.max_experiencias:]
            )

            self._guardar_json(
                self.conocimiento_path,
                self.conocimiento
            )

            self.estado["aprendizajes"] += 1

            return {
                "aprendido": True,
                "datos": aprendizaje,
            }

        return {
            "aprendido": False,
            "motivo": (
                "Evidencia insuficiente para consolidar "
                "el resultado como conocimiento."
            ),
        }

    # ==========================================================
    # 8. CICLO COMPLETO
    # ==========================================================

    def ejecutar(
        self,
        entrada: str,
        resultados_externos: Optional[Any] = None,
    ) -> Dict[str, Any]:

        inicio = time.perf_counter()

        ciclo_id = self._id_ciclo(
            str(entrada)
        )

        self.estado["ciclos"] += 1
        self.estado["ultimo_ciclo"] = ciclo_id

        # --------------------------------------
        # ENTRADA
        # --------------------------------------

        analisis = self.analizar_entrada(
            entrada
        )

        # --------------------------------------
        # MEMORIA
        # --------------------------------------

        memoria = self.consultar_memoria(
            entrada
        )

        # --------------------------------------
        # CONOCIMIENTO
        # --------------------------------------

        conocimiento = self.consultar_conocimiento(
            entrada
        )

        # --------------------------------------
        # RAZONAMIENTO
        # --------------------------------------

        razonamiento = self.razonar(
            entrada,
            analisis,
            memoria,
            conocimiento,
            resultados_externos,
        )

        # --------------------------------------
        # EVALUACIÓN
        # --------------------------------------

        evaluacion = self.evaluar(
            razonamiento
        )

        resultado = {
            "ciclo_id": ciclo_id,
            "fecha": self._ahora(),
            "analisis": analisis,
            "memoria": memoria,
            "conocimiento": conocimiento,
            "resultados_externos": resultados_externos,
            "razonamiento": razonamiento,
            "evaluacion": evaluacion,
        }

        # --------------------------------------
        # EXPERIENCIA
        # --------------------------------------

        self.guardar_experiencia(
            ciclo_id,
            entrada,
            resultado
        )

        # --------------------------------------
        # APRENDIZAJE
        # --------------------------------------

        aprendizaje = self.aprender(
            entrada,
            resultado
        )

        resultado["aprendizaje"] = aprendizaje

        resultado["duracion_ms"] = round(
            (time.perf_counter() - inicio)
            * 1000,
            3
        )

        return resultado

    # ==========================================================
    # ESTADO
    # ==========================================================

    def estado_actual(self) -> Dict[str, Any]:

        return {
            **self.estado,
            "version": self.VERSION,
            "recuerdos": len(
                self.memoria.get(
                    "recuerdos",
                    []
                )
            ),
            "experiencias": len(
                self.experiencias.get(
                    "experiencias",
                    []
                )
            ),
            "conocimientos": len(
                self.conocimiento.get(
                    "conocimientos",
                    []
                )
            ),
        }


# ==============================================================
# PRUEBA DIRECTA
# ==============================================================

if __name__ == "__main__":

    cerebro = CicloCognitivoOmega()

    resultado = cerebro.ejecutar(
        "Analiza cómo podría cambiar la inteligencia artificial en el futuro."
    )

    print("\n🧠 CEREBRO OMEGA ∞")
    print("CICLO COGNITIVO:", resultado["ciclo_id"])
    print(
        "TIPO:",
        resultado["analisis"]["tipo"]
    )
    print(
        "CONFIANZA:",
        resultado["evaluacion"]["confianza"]
    )
    print(
        "APRENDIÓ:",
        resultado["aprendizaje"]["aprendido"]
    )

    print("\n📊 ESTADO")
    print(
        json.dumps(
            cerebro.estado_actual(),
            ensure_ascii=False,
            indent=2
        )
    )
