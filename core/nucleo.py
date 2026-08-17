"""
CEREBRO OMEGA
OMEGA CORE — Núcleo Fundacional
"""

from modules.generation import GenerationEngine
from modules.evaluation import EvaluationEngine


class OmegaCore:
    """Núcleo coordinador de CEREBRO OMEGA."""

    def __init__(self):
        self.generator = GenerationEngine()
        self.evaluator = EvaluationEngine()
        self.generation = 0

    def explore(self, objective: str, amount: int = 8):
        """Genera y evalúa posibilidades."""

        if not objective.strip():
            raise ValueError("El objetivo no puede estar vacío.")

        self.generation += 1

        possibilities = self.generator.generate(
            objective,
            amount
        )

        results = self.evaluator.evaluate(
            possibilities
        )

        for possibility in results:
            possibility.generation = self.generation

        return results

    def status(self):
        """Estado básico del núcleo."""

        return {
            "system": "CEREBRO OMEGA",
            "status": "ONLINE",
            "generation": self.generation,
            "engines": [
                "generation",
                "evaluation"
            ]
        }


if __name__ == "__main__":

    omega = OmegaCore()

    results = omega.explore(
        "crear una nueva herramienta musical"
    )

    print("\n🧠 CEREBRO OMEGA")
    print("=" * 50)

    for number, result in enumerate(results, 1):
        print(
            f"{number}. "
            f"[{result.score:.2f}] "
            f"{result.idea}"
        )

    print("\n☁️ ESTADO:")
    print(omega.status())
