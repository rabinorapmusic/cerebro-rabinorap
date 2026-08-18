"""
CEREBRO OMEGA
Motor Evolutivo Modular
Versión: 1.0

Función:
    - Registrar ciclos
    - Evaluar resultados
    - Guardar aprendizaje
    - Mantener memoria persistente
    - Generar propuestas de evolución
    - No modifica el núcleo automáticamente
"""

from __future__ import annotations

import json
import time
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional


class EvolutionEngine:
    """
    Motor evolutivo independiente de CEREBRO OMEGA.

    Flujo:

        INPUT
          ↓
        PROCESAMIENTO
          ↓
        RESULTADO
          ↓
        EVALUACIÓN
          ↓
        APRENDIZAJE
          ↓
        MEMORIA
          ↓
        PROPUESTA DE EVOLUCIÓN
          ↓
        NUEVO CICLO
    """

    VERSION = "1.0"

    def __init__(self, storage_dir: str = "data/cerebro"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.memory_file = self.storage_dir / "evolution_memory.json"
        self.cycles_file = self.storage_dir / "evolution_cycles.json"

        self.memory = self._load_json(
            self.memory_file,
            {
                "facts": [],
                "learned": [],
                "improvements": [],
            },
        )

        self.cycles = self._load_json(
            self.cycles_file,
            {
                "total": 0,
                "history": [],
            },
        )

    # =========================================================
    # CARGA Y GUARDADO
    # =========================================================

    def _load_json(self, path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not path.exists():
                self._save_json(path, default)
                return default

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

        except (json.JSONDecodeError, OSError):
            pass

        return default.copy()

    def _save_json(self, path: Path, data: Dict[str, Any]) -> None:
        temp = path.with_suffix(".tmp")

        with temp.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

        temp.replace(path)

    # =========================================================
    # IDENTIDAD DE REGISTRO
    # =========================================================

    def _make_id(self, text: str) -> str:
        raw = f"{text}:{time.time_ns()}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:16]

    # =========================================================
    # REGISTRAR FACT
    # =========================================================

    def add_fact(
        self,
        fact: str,
        source: str = "system",
    ) -> Dict[str, Any]:

        fact = str(fact).strip()

        if not fact:
            return {
                "success": False,
                "reason": "empty_fact",
            }

        existing = [
            item.get("content", "").lower()
            for item in self.memory["facts"]
        ]

        if fact.lower() in existing:
            return {
                "success": True,
                "new": False,
                "reason": "already_exists",
            }

        record = {
            "id": self._make_id(fact),
            "content": fact,
            "source": source,
            "timestamp": time.time(),
        }

        self.memory["facts"].append(record)

        self._save_json(
            self.memory_file,
            self.memory,
        )

        return {
            "success": True,
            "new": True,
            "fact": record,
        }

    # =========================================================
    # APRENDIZAJE
    # =========================================================

    def learn(
        self,
        input_text: str,
        result: Any,
        score: float,
    ) -> Dict[str, Any]:

        score = max(0.0, min(1.0, float(score)))

        learning = {
            "id": self._make_id(input_text),
            "input": str(input_text),
            "result": self._safe_value(result),
            "score": round(score, 4),
            "timestamp": time.time(),
        }

        self.memory["learned"].append(learning)

        # Evita crecimiento ilimitado del archivo
        if len(self.memory["learned"]) > 1000:
            self.memory["learned"] = self.memory["learned"][-1000:]

        self._save_json(
            self.memory_file,
            self.memory,
        )

        return learning

    # =========================================================
    # EVALUACIÓN
    # =========================================================

    def evaluate(
        self,
        result: Any,
        expected: Optional[Any] = None,
    ) -> Dict[str, Any]:

        if result is None:
            return {
                "score": 0.0,
                "quality": "EMPTY",
                "useful": False,
            }

        text = str(result).strip()

        if not text:
            return {
                "score": 0.0,
                "quality": "EMPTY",
                "useful": False,
            }

        score = 0.5

        # Resultado con contenido
        if len(text) >= 20:
            score += 0.15

        if len(text) >= 100:
            score += 0.10

        # Si existe referencia esperada
        if expected is not None:
            if str(expected).strip().lower() in text.lower():
                score += 0.25

        score = min(score, 1.0)

        if score >= 0.80:
            quality = "EXCELLENT"
        elif score >= 0.60:
            quality = "GOOD"
        elif score >= 0.40:
            quality = "AVERAGE"
        else:
            quality = "LOW"

        return {
            "score": round(score, 4),
            "quality": quality,
            "useful": score >= 0.60,
        }

    # =========================================================
    # PROPUESTA DE EVOLUCIÓN
    # =========================================================

    def generate_evolution(
        self,
        evaluation: Dict[str, Any],
    ) -> Dict[str, Any]:

        score = float(
            evaluation.get("score", 0.0)
        )

        quality = evaluation.get(
            "quality",
            "UNKNOWN",
        )

        if score >= 0.80:
            action = "REINFORCE"

            proposal = (
                "Conservar el patrón actual y reforzar "
                "las estrategias que produjeron buenos resultados."
            )

        elif score >= 0.60:
            action = "OPTIMIZE"

            proposal = (
                "Mantener la estrategia y buscar una "
                "optimización incremental."
            )

        elif score >= 0.40:
            action = "ANALYZE"

            proposal = (
                "Analizar el resultado y probar una "
                "variante controlada en el siguiente ciclo."
            )

        else:
            action = "CORRECT"

            proposal = (
                "Identificar la causa del bajo rendimiento "
                "antes de intentar una nueva estrategia."
            )

        improvement = {
            "id": self._make_id(proposal),
            "action": action,
            "quality": quality,
            "score": score,
            "proposal": proposal,
            "timestamp": time.time(),
        }

        self.memory["improvements"].append(improvement)

        if len(self.memory["improvements"]) > 500:
            self.memory["improvements"] = (
                self.memory["improvements"][-500:]
            )

        self._save_json(
            self.memory_file,
            self.memory,
        )

        return improvement

    # =========================================================
    # CICLO COMPLETO
    # =========================================================

    def run_cycle(
        self,
        input_text: str,
        processor_result: Any,
        expected: Optional[Any] = None,
    ) -> Dict[str, Any]:

        started = time.time()

        # 1. Evaluar
        evaluation = self.evaluate(
            processor_result,
            expected,
        )

        # 2. Aprender
        learning = self.learn(
            input_text,
            processor_result,
            evaluation["score"],
        )

        # 3. Evolucionar
        evolution = self.generate_evolution(
            evaluation
        )

        # 4. Incrementar ciclo
        self.cycles["total"] += 1

        cycle_number = self.cycles["total"]

        cycle = {
            "cycle": cycle_number,
            "input": str(input_text),
            "result": self._safe_value(
                processor_result
            ),
            "evaluation": evaluation,
            "learning_id": learning["id"],
            "evolution_id": evolution["id"],
            "duration_ms": round(
                (time.time() - started) * 1000,
                2,
            ),
            "timestamp": time.time(),
        }

        self.cycles["history"].append(cycle)

        # Mantener memoria controlada
        if len(self.cycles["history"]) > 500:
            self.cycles["history"] = (
                self.cycles["history"][-500:]
            )

        self._save_json(
            self.cycles_file,
            self.cycles,
        )

        return cycle

    # =========================================================
    # DIAGNÓSTICO
    # =========================================================

    def diagnostics(self) -> Dict[str, Any]:

        return {
            "status": "ACTIVE",
            "version": self.VERSION,
            "cycles": self.cycles["total"],
            "facts": len(
                self.memory.get("facts", [])
            ),
            "learned": len(
                self.memory.get("learned", [])
            ),
            "improvements": len(
                self.memory.get("improvements", [])
            ),
            "memory_file": str(
                self.memory_file
            ),
            "cycles_file": str(
                self.cycles_file
            ),
        }

    # =========================================================
    # MEMORIA RECIENTE
    # =========================================================

    def recent_memory(
        self,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        limit = max(1, int(limit))

        return self.memory["learned"][-limit:]

    # =========================================================
    # HISTORIAL DE CICLOS
    # =========================================================

    def recent_cycles(
        self,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:

        limit = max(1, int(limit))

        return self.cycles["history"][-limit:]

    # =========================================================
    # UTILIDAD
    # =========================================================

    def _safe_value(self, value: Any) -> Any:

        try:
            json.dumps(value, ensure_ascii=False)
            return value

        except TypeError:
            return str(value)


# =============================================================
# PRUEBA DIRECTA DEL MÓDULO
# =============================================================

if __name__ == "__main__":

    cerebro = EvolutionEngine()

    resultado = cerebro.run_cycle(
        input_text="Crear una idea musical para CEREBRO OMEGA",
        processor_result=(
            "Idea musical generada correctamente "
            "con estructura de rap evolutivo."
        ),
    )

    print("\n🧠 CEREBRO OMEGA")
    print("====================")

    print(
        json.dumps(
            resultado,
            ensure_ascii=False,
            indent=2,
        )
    )

    print("\n📊 DIAGNÓSTICO")
    print("====================")

    print(
        json.dumps(
            cerebro.diagnostics(),
            ensure_ascii=False,
            indent=2,
        )
    )
