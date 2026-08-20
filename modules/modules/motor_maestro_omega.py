"""
╔══════════════════════════════════════════════════════════════════╗
║                       CEREBRO OMEGA ∞                           ║
║                    MOTOR MAESTRO OMEGA                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║     ENTRADA                                                      ║
║        ↓                                                         ║
║     PLANIFICADOR                                                 ║
║        ↓                                                         ║
║     ORQUESTADOR                                                  ║
║        ↓                                                         ║
║  ┌───────────────┬──────────────┬───────────────┐                ║
║  │ ALIMENTADOR   │ INVESTIGADOR │ MOTOR TEMPORAL│                ║
║  └───────────────┴──────────────┴───────────────┘                ║
║        ↓                                                         ║
║     CICLO COGNITIVO                                              ║
║        ↓                                                         ║
║     FUSIÓN                                                       ║
║        ↓                                                         ║
║     EVALUACIÓN                                                   ║
║        ↓                                                         ║
║     MEMORIA                                                      ║
║        ↓                                                         ║
║     APRENDIZAJE                                                  ║
║        ↓                                                         ║
║     RESPUESTA                                                    ║
║                                                                  ║
║                         ∞                                        ║
╚══════════════════════════════════════════════════════════════════╝

Motor superior de coordinación.

IMPORTANTE:
- No reemplaza core.py.
- No reemplaza el orquestador.
- No modifica los módulos existentes.
- Carga los módulos de forma dinámica.
- Si un módulo falla, el sistema intenta continuar.
"""

from __future__ import annotations

import importlib
import inspect
import json
import time
import traceback
import uuid

from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class MotorMaestroOmega:

    VERSION = "1.0.0"

    def __init__(
        self,
        modules_path: str = "modules",
        registro_path: str = "omega_motor_registro.json",
    ):

        self.modules_path = modules_path
        self.registro_path = Path(registro_path)

        self.id_motor = str(uuid.uuid4())[:12]

        self.modulos: Dict[str, Any] = {}
        self.errores: List[Dict[str, Any]] = []

        self.estadisticas = {
            "ejecuciones": 0,
            "exitos": 0,
            "fallos": 0,
            "modulos_ejecutados": 0,
            "aprendizajes": 0,
        }

        self.configuracion = {
            "modo": "omega",
            "tolerante_a_fallos": True,
            "aprendizaje": True,
            "memoria": True,
            "investigacion": True,
            "temporal": True,
            "evaluacion": True,
        }

        self._cargar_modulos()

    # ==========================================================
    # UTILIDADES
    # ==========================================================

    def _ahora(self) -> str:

        return datetime.now(
            timezone.utc
        ).isoformat()

    def _registrar_error(
        self,
        modulo: str,
        error: Exception,
    ):

        datos = {
            "fecha": self._ahora(),
            "modulo": modulo,
            "error": str(error),
            "tipo": type(error).__name__,
        }

        self.errores.append(datos)

        self.estadisticas["fallos"] += 1

    # ==========================================================
    # CARGADOR DINÁMICO
    # ==========================================================

    def _cargar_modulos(self):

        candidatos = {

            "alimentador": [
                "modules.alimentador",
            ],

            "investigador": [
                "modules.investigador_omega",
                "modules.investigador",
            ],

            "temporal": [
                "modules.motor_temporal_omega",
            ],

            "cognitivo": [
                "modules.ciclo_cognitivo_omega",
            ],

            "orquestador": [
                "modules.orquestador_omega",
                "modules.orquestador",
            ],
        }

        for nombre, opciones in candidatos.items():

            for modulo_nombre in opciones:

                try:

                    modulo = importlib.import_module(
                        modulo_nombre
                    )

                    self.modulos[nombre] = modulo

                    break

                except Exception:

                    continue

    # ==========================================================
    # CREAR INSTANCIA
    # ==========================================================

    def _crear_instancia(
        self,
        nombre: str,
    ):

        modulo = self.modulos.get(nombre)

        if modulo is None:
            return None

        clases_preferidas = {

            "alimentador": [
                "AlimentadorOmega",
                "Alimentador",
            ],

            "investigador": [
                "InvestigadorOmega",
                "Investigador",
            ],

            "temporal": [
                "MotorTemporalOmega",
            ],

            "cognitivo": [
                "CicloCognitivoOmega",
            ],

            "orquestador": [
                "OrquestadorOmega",
                "Orquestador",
            ],
        }

        for nombre_clase in clases_preferidas.get(
            nombre,
            []
        ):

            clase = getattr(
                modulo,
                nombre_clase,
                None
            )

            if clase is None:
                continue

            try:
                return clase()

            except TypeError:

                try:
                    return clase

                except Exception:
                    pass

            except Exception:
                continue

        return modulo

    # ==========================================================
    # PLANIFICADOR
    # ==========================================================

    def planificar(
        self,
        entrada: str,
    ) -> Dict[str, Any]:

        texto = str(entrada).lower()

        plan = {
            "alimentador": False,
            "investigador": False,
            "temporal": False,
            "cognitivo": False,
            "orquestador": False,
        }

        # Siempre intentamos pasar por cognición.
        plan["cognitivo"] = True

        if any(
            palabra in texto
            for palabra in (
                "aprende",
                "enseña",
                "conocimiento",
                "aliment",
            )
        ):
            plan["alimentador"] = True

        if any(
            palabra in texto
            for palabra in (
                "investiga",
                "investigar",
                "busca",
                "fuentes",
                "evidencia",
                "averigua",
            )
        ):
            plan["investigador"] = True

        if any(
            palabra in texto
            for palabra in (
                "pasado",
                "historia",
                "histórico",
                "futuro",
                "futuros",
                "escenario",
                "posibilidad",
            )
        ):
            plan["temporal"] = True

        # Si existe, el orquestador puede coordinar
        # operaciones adicionales.
        plan["orquestador"] = True

        return {
            "entrada": entrada,
            "plan": plan,
            "fecha": self._ahora(),
        }

    # ==========================================================
    # EJECUTOR UNIVERSAL
    # ==========================================================

    def _ejecutar_objeto(
        self,
        objeto: Any,
        entrada: str,
        contexto: Dict[str, Any],
    ):

        if objeto is None:
            return None

        candidatos = [
            "ejecutar",
            "procesar",
            "analizar",
            "investigar",
            "alimentar",
            "run",
            "run_cycle",
        ]

        for nombre in candidatos:

            funcion = getattr(
                objeto,
                nombre,
                None
            )

            if not callable(funcion):
                continue

            try:

                firma = inspect.signature(
                    funcion
                )

                parametros = list(
                    firma.parameters.values()
                )

                obligatorios = [
                    p for p in parametros
                    if (
                        p.default is inspect.Parameter.empty
                        and
                        p.kind
                        in (
                            inspect.Parameter.POSITIONAL_ONLY,
                            inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        )
                    )
                ]

                if len(obligatorios) == 0:

                    return funcion()

                if len(obligatorios) == 1:

                    return funcion(entrada)

                return funcion(
                    entrada,
                    contexto
                )

            except TypeError:

                # Compatibilidad con APIs diferentes.
                intentos = [
                    lambda: funcion(entrada),
                    lambda: funcion(contexto),
                    lambda: funcion(),
                ]

                for intento in intentos:

                    try:
                        return intento()

                    except TypeError:
                        continue

            except Exception as error:

                raise error

        return None

    # ==========================================================
    # EJECUTAR MÓDULO
    # ==========================================================

    def _ejecutar_modulo(
        self,
        nombre: str,
        entrada: str,
        contexto: Dict[str, Any],
    ):

        if nombre not in self.modulos:

            return {
                "disponible": False,
                "modulo": nombre,
            }

        try:

            instancia = self._crear_instancia(
                nombre
            )

            resultado = self._ejecutar_objeto(
                instancia,
                entrada,
                contexto,
            )

            self.estadisticas[
                "modulos_ejecutados"
            ] += 1

            return {
                "disponible": True,
                "resultado": resultado,
            }

        except Exception as error:

            self._registrar_error(
                nombre,
                error
            )

            return {
                "disponible": True,
                "error": str(error),
            }

    # ==========================================================
    # FUSIÓN DE INFORMACIÓN
    # ==========================================================

    def fusionar(
        self,
        resultados: Dict[str, Any],
    ) -> Dict[str, Any]:

        evidencia = []

        for nombre, resultado in resultados.items():

            if not isinstance(resultado, dict):
                continue

            if resultado.get("error"):
                continue

            if resultado.get("resultado") is not None:

                evidencia.append({
                    "modulo": nombre,
                    "datos": resultado["resultado"],
                })

        return {
            "cantidad_fuentes": len(evidencia),
            "evidencia": evidencia,
        }

    # ==========================================================
    # EVALUACIÓN GLOBAL
    # ==========================================================

    def evaluar(
        self,
        fusion: Dict[str, Any],
    ) -> Dict[str, Any]:

        cantidad = fusion.get(
            "cantidad_fuentes",
            0
        )

        if cantidad >= 4:
            nivel = "alto"

        elif cantidad >= 2:
            nivel = "medio"

        elif cantidad == 1:
            nivel = "bajo"

        else:
            nivel = "insuficiente"

        return {
            "nivel": nivel,
            "fuentes": cantidad,
            "requiere_revision": (
                nivel in (
                    "bajo",
                    "insuficiente"
                )
            ),
        }

    # ==========================================================
    # MEMORIA DEL MOTOR
    # ==========================================================

    def guardar_registro(
        self,
        resultado: Dict[str, Any],
    ) -> bool:

        datos = []

        try:

            if self.registro_path.exists():

                with open(
                    self.registro_path,
                    "r",
                    encoding="utf-8",
                ) as archivo:

                    datos = json.load(
                        archivo
                    )

                    if not isinstance(
                        datos,
                        list
                    ):
                        datos = []

        except Exception:

            datos = []

        datos.append(resultado)

        # Evitar crecimiento infinito.
        datos = datos[-500:]

        try:

            temporal = self.registro_path.with_suffix(
                ".tmp"
            )

            with open(
                temporal,
                "w",
                encoding="utf-8",
            ) as archivo:

                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=2,
                )

            temporal.replace(
                self.registro_path
            )

            return True

        except Exception:

            return False

    # ==========================================================
    # EJECUCIÓN MAESTRA
    # ==========================================================

    def ejecutar(
        self,
        entrada: str,
    ) -> Dict[str, Any]:

        inicio = time.perf_counter()

        self.estadisticas[
            "ejecuciones"
        ] += 1

        contexto: Dict[str, Any] = {
            "entrada": entrada,
            "motor": self.VERSION,
            "fecha": self._ahora(),
        }

        # ------------------------------------------------------
        # 1. PLAN
        # ------------------------------------------------------

        plan = self.planificar(
            entrada
        )

        resultados = {}

        # ------------------------------------------------------
        # 2. ALIMENTADOR
        # ------------------------------------------------------

        if plan["plan"]["alimentador"]:

            resultados["alimentador"] = (
                self._ejecutar_modulo(
                    "alimentador",
                    entrada,
                    contexto,
                )
            )

            contexto["alimentador"] = (
                resultados["alimentador"]
            )

        # ------------------------------------------------------
        # 3. INVESTIGADOR
        # ------------------------------------------------------

        if plan["plan"]["investigador"]:

            resultados["investigador"] = (
                self._ejecutar_modulo(
                    "investigador",
                    entrada,
                    contexto,
                )
            )

            contexto["investigador"] = (
                resultados["investigador"]
            )

        # ------------------------------------------------------
        # 4. MOTOR TEMPORAL
        # ------------------------------------------------------

        if plan["plan"]["temporal"]:

            resultados["temporal"] = (
                self._ejecutar_modulo(
                    "temporal",
                    entrada,
                    contexto,
                )
            )

            contexto["temporal"] = (
                resultados["temporal"]
            )

        # ------------------------------------------------------
        # 5. ORQUESTADOR EXISTENTE
        # ------------------------------------------------------

        if plan["plan"]["orquestador"]:

            resultados["orquestador"] = (
                self._ejecutar_modulo(
                    "orquestador",
                    entrada,
                    contexto,
                )
            )

            contexto["orquestador"] = (
                resultados["orquestador"]
            )

        # ------------------------------------------------------
        # 6. FUSIÓN
        # ------------------------------------------------------

        fusion = self.fusionar(
            resultados
        )

        contexto["fusion"] = fusion

        # ------------------------------------------------------
        # 7. CICLO COGNITIVO
        # ------------------------------------------------------

        if plan["plan"]["cognitivo"]:

            resultados["cognitivo"] = (
                self._ejecutar_modulo(
                    "cognitivo",
                    entrada,
                    contexto,
                )
            )

        # ------------------------------------------------------
        # 8. EVALUACIÓN GLOBAL
        # ------------------------------------------------------

        evaluacion = self.evaluar(
            fusion
        )

        # ------------------------------------------------------
        # 9. RESULTADO FINAL
        # ------------------------------------------------------

        resultado_final = {

            "omega": "CEREBRO OMEGA ∞",

            "motor": {
                "version": self.VERSION,
                "id": self.id_motor,
            },

            "entrada": entrada,

            "plan": plan,

            "resultados": resultados,

            "fusion": fusion,

            "evaluacion": evaluacion,

            "errores": self.errores[-20:],

            "duracion_ms": round(
                (
                    time.perf_counter()
                    - inicio
                ) * 1000,
                3,
            ),

            "fecha": self._ahora(),
        }

        # ------------------------------------------------------
        # 10. MEMORIA OPERACIONAL
        # ------------------------------------------------------

        if evaluacion["nivel"] in (
            "medio",
            "alto",
        ):

            self.estadisticas[
                "aprendizajes"
            ] += 1

        # ------------------------------------------------------
        # 11. REGISTRO
        # ------------------------------------------------------

        self.guardar_registro(
            resultado_final
        )

        if not self.errores:

            self.estadisticas[
                "exitos"
            ] += 1

        return resultado_final

    # ==========================================================
    # DIAGNÓSTICO
    # ==========================================================

    def diagnostico(self) -> Dict[str, Any]:

        return {

            "sistema": "CEREBRO OMEGA ∞",

            "motor": self.VERSION,

            "activo": True,

            "modulos_detectados": list(
                self.modulos.keys()
            ),

            "cantidad_modulos": len(
                self.modulos
            ),

            "estadisticas": self.estadisticas,

            "errores": self.errores[-20:],

            "configuracion": self.configuracion,

        }


# ==============================================================
# PRUEBA
# ==============================================================

if __name__ == "__main__":

    print()
    print("🧠 CEREBRO OMEGA ∞")
    print("⚡ MOTOR MAESTRO OMEGA")
    print()

    motor = MotorMaestroOmega()

    print("MÓDULOS DETECTADOS:")

    for modulo in motor.modulos:

        print(
            "  ✓",
            modulo
        )

    print()

    consulta = (
        "Analiza las posibilidades del futuro "
        "de la inteligencia artificial."
    )

    resultado = motor.ejecutar(
        consulta
    )

    print(
        "CONSULTA:",
        consulta
    )

    print(
        "EVALUACIÓN:",
        resultado[
            "evaluacion"
        ]["nivel"]
    )

    print(
        "TIEMPO:",
        resultado[
            "duracion_ms"
        ],
        "ms"
    )

    print()

    print(
        "DIAGNÓSTICO:"
    )

    print(
        json.dumps(
            motor.diagnostico(),
            ensure_ascii=False,
            indent=2,
        )
    )
