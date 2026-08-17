from modules.generation import GenerationEngine
from modules.evaluation import EvaluationEngine
cerebro/omega
Principio:
    GENERAR → COMBINAR → MUTAR → EVALUAR → EVOLUCIONAR

El núcleo coordina posibilidades.
Los módulos externos aportan capacidades especializadas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional
import random
import uuid


# ============================================================
# 🧬 MODELO FUNDAMENTAL
# ============================================================

@dataclass
class Possibility:
    """Representa una posibilidad explorada por OMEGA."""

    idea: str
    score: float = 0.0
    generation: int = 0
    origin: str = "generated"
    metadata: dict = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        self.score = max(0.0, min(1.0, float(self.score)))

    def describe(self) -> str:
        return (
            f"[{self.score:.2f}] "
            f"G{self.generation} "
            f"{self.origin}: {self.idea}"
        )


# ============================================================
# ♾️ GENERADOR DE POSIBILIDADES
# ============================================================

class PossibilityEngine:
    """
    Motor encargado de producir posibilidades.

    Puede ser reemplazado posteriormente por motores de IA,
    modelos externos o algoritmos especializados.
    """

    def __init__(self, seed: Optional[int] = None):
        self.random = random.Random(seed)

    def generate(
        self,
        objective: str,
        amount: int = 10,
        generation: int = 0,
    ) -> list[Possibility]:

        if not objective.strip():
            raise ValueError("El objetivo no puede estar vacío.")

        amount = max(1, amount)

        templates = [
            "Resolver {objective} de forma simple.",
            "Resolver {objective} de forma eficiente.",
            "Resolver {objective} mediante una estrategia alternativa.",
            "Resolver {objective} utilizando automatización.",
            "Resolver {objective} dividiéndolo en partes pequeñas.",
            "Resolver {objective} combinando diferentes métodos.",
            "Resolver {objective} mediante experimentación.",
            "Resolver {objective} buscando una solución completamente diferente.",
        ]

        possibilities = []

        for _ in range(amount):
            template = self.random.choice(templates)

            possibilities.append(
                Possibility(
                    idea=template.format(objective=objective),
                    generation=generation,
                    origin="generated",
                )
            )

        return possibilities


# ============================================================
# 🧬 COMBINADOR
# ============================================================

class Combiner:
    """Combina dos posibilidades para crear una nueva."""

    @staticmethod
    def combine(
        first: Possibility,
        second: Possibility,
    ) -> Possibility:

        idea = (
            f"Combinación de: "
            f"({first.idea}) + ({second.idea})"
        )

        return Possibility(
            idea=idea,
            generation=max(first.generation, second.generation) + 1,
            origin="combined",
            metadata={
                "parents": [first.id, second.id]
            },
        )


# ============================================================
# 🌀 MUTADOR
# ============================================================

class Mutator:
    """Genera variantes de una posibilidad existente."""

    @staticmethod
    def mutate(
        possibility: Possibility,
        variation: str = "alternativa",
    ) -> Possibility:

        idea = (
            f"Variación {variation} de: "
            f"{possibility.idea}"
        )

        return Possibility(
            idea=idea,
            generation=possibility.generation + 1,
            origin="mutation",
            metadata={
                "parent": possibility.id,
                "variation": variation,
            },
        )


# ============================================================
# ⚖️ EVALUADOR
# ============================================================

class Evaluator:
    """
    Evalúa posibilidades.

    Se puede conectar posteriormente con:
    - modelos de IA
    - reglas matemáticas
    - simuladores
    - datos reales
    - evaluadores especializados
    """

    def __init__(
        self,
        evaluator: Optional[Callable[[Possibility], float]] = None,
    ):
        self.evaluator = evaluator or self.default_evaluator

    @staticmethod
    def default_evaluator(possibility: Possibility) -> float:
        """
        Evaluación inicial.

        No pretende representar inteligencia avanzada.
        Solo proporciona un mecanismo funcional para que
        el núcleo pueda operar desde el primer día.
        """

        length_score = min(len(possibility.idea) / 200, 1.0)

        diversity_bonus = {
            "generated": 0.05,
            "combined": 0.15,
            "mutation": 0.10,
        }.get(possibility.origin, 0.0)

        score = 0.5 + (length_score * 0.25) + diversity_bonus

        return min(score, 1.0)

    def evaluate(
        self,
        possibilities: Iterable[Possibility],
    ) -> list[Possibility]:

        results = list(possibilities)

        for possibility in results:
            possibility.score = self.evaluator(possibility)

        return sorted(
            results,
            key=lambda item: item.score,
            reverse=True,
        )


# ============================================================
# 🧭 OMEGA CORE
# ============================================================

class OmegaCore:
    """
    Núcleo coordinador de CEREBRO OMEGA.

    No contiene conocimiento específico de un área.
    Coordina procesos generales de exploración.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        seed: Optional[int] = None,
        evaluator: Optional[Callable[[Possibility], float]] = None,
    ):
        self.generator = PossibilityEngine(seed=seed)
        self.combiner = Combiner()
        self.mutator = Mutator()
        self.evaluator = Evaluator(evaluator)

        self.generation = 0
        self.history: list[Possibility] = []

    # --------------------------------------------------------
    # GENERAR
    # --------------------------------------------------------

    def generate(
        self,
        objective: str,
        amount: int = 10,
    ) -> list[Possibility]:

        possibilities = self.generator.generate(
            objective=objective,
            amount=amount,
            generation=self.generation,
        )

        self.history.extend(possibilities)

        return possibilities

    # --------------------------------------------------------
    # COMBINAR
    # --------------------------------------------------------

    def combine(
        self,
        possibilities: list[Possibility],
        amount: int = 5,
    ) -> list[Possibility]:

        if len(possibilities) < 2:
            return []

        combinations = []

        for _ in range(amount):
            first, second = self.generator.random.sample(
                possibilities,
                2,
            )

            combinations.append(
                self.combiner.combine(first, second)
            )

        self.history.extend(combinations)

        return combinations

    # --------------------------------------------------------
    # MUTAR
    # --------------------------------------------------------

    def mutate(
        self,
        possibilities: list[Possibility],
        amount: int = 5,
    ) -> list[Possibility]:

        if not possibilities:
            return []

        variations = [
            "simplificada",
            "optimizada",
            "experimental",
            "radical",
            "económica",
            "escalable",
            "creativa",
        ]

        mutations = []

        for _ in range(amount):
            parent = self.generator.random.choice(
                possibilities
            )

            variation = self.generator.random.choice(
                variations
            )

            mutations.append(
                self.mutator.mutate(
                    parent,
                    variation,
                )
            )

        self.history.extend(mutations)

        return mutations

    # --------------------------------------------------------
    # EVALUAR
    # --------------------------------------------------------

    def evaluate(
        self,
        possibilities: Iterable[Possibility],
    ) -> list[Possibility]:

        return self.evaluator.evaluate(possibilities)

    # --------------------------------------------------------
    # CICLO OMEGA
    # --------------------------------------------------------

    def explore(
        self,
        objective: str,
        possibilities_per_generation: int = 10,
        cycles: int = 3,
    ) -> list[Possibility]:

        if cycles < 1:
            raise ValueError("Los ciclos deben ser mayores que cero.")

        current = self.generate(
            objective,
            possibilities_per_generation,
        )

        for _ in range(cycles):

            self.generation += 1

            combined = self.combine(
                current,
                max(1, possibilities_per_generation // 2),
            )

            mutated = self.mutate(
                current,
                max(1, possibilities_per_generation // 2),
            )

            candidates = current + combined + mutated

            ranked = self.evaluate(candidates)

            current = ranked[
                :possibilities_per_generation
            ]

        return current

    # --------------------------------------------------------
    # ESTADO
    # --------------------------------------------------------

    def status(self) -> dict:
        return {
            "system": "CEREBRO OMEGA",
            "version": self.VERSION,
            "generation": self.generation,
            "history_size": len(self.history),
            "modules": [
                "possibility",
                "combination",
                "mutation",
                "evaluation",
                "evolution",
            ],
        }


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    omega = OmegaCore(seed=42)

    results = omega.explore(
        objective="crear una nueva herramienta musical",
        possibilities_per_generation=8,
        cycles=3,
    )

    print("\n🧠 CEREBRO OMEGA")
    print("═" * 60)

    for number, possibility in enumerate(results, 1):
        print(
            f"{number}. "
            f"{possibility.describe()}"
        )

    print("\n☁️ ESTADO")
    print(omega.status())
