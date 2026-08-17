import random
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Possibility:
    idea: str
    score: float = 0.0
    generation: int = 0
    origin: str = "generated"
    metadata: Dict = field(default_factory=dict)


class GenerationEngine:

    def __init__(self):
        self.patterns = [
            "Crear una solución nueva para",
            "Resolver de forma eficiente",
            "Encontrar una alternativa para",
            "Diseñar una estrategia para",
            "Experimentar con una forma diferente de",
            "Automatizar una solución para",
            "Combinar métodos para",
            "Explorar una posibilidad inesperada para",
            "Simplificar la solución de",
            "Crear una versión avanzada de",
        ]

    def generate(
        self,
        objective: str,
        amount: int,
        generation: int,
    ) -> List[Possibility]:

        return [
            Possibility(
                idea=f"{random.choice(self.patterns)} {objective}",
                generation=generation,
                origin="generated",
            )
            for _ in range(amount)
        ]


class EvaluationEngine:

    def evaluate(
        self,
        possibilities: List[Possibility],
    ) -> List[Possibility]:

        for possibility in possibilities:

            score = 0.45

            if len(possibility.idea) > 50:
                score += 0.10

            if len(possibility.idea) > 90:
                score += 0.10

            if possibility.origin == "combined":
                score += 0.15

            if possibility.origin == "mutated":
                score += 0.10

            score += random.uniform(0.0, 0.20)

            possibility.score = min(score, 1.0)

        return sorted(
            possibilities,
            key=lambda item: item.score,
            reverse=True,
        )


class EvolutionEngine:

    def __init__(self):

        self.variations = [
            "más simple",
            "más rápida",
            "más creativa",
            "más económica",
            "más escalable",
            "más experimental",
            "más precisa",
            "completamente diferente",
        ]

    def mutate(
        self,
        possibility: Possibility,
        generation: int,
    ) -> Possibility:

        variation = random.choice(
            self.variations
        )

        return Possibility(
            idea=(
                f"Transformar [{possibility.idea}] "
                f"haciéndolo {variation}"
            ),
            generation=generation,
            origin="mutated",
            metadata={
                "parent": possibility.idea,
                "variation": variation,
            },
        )

    def combine(
        self,
        first: Possibility,
        second: Possibility,
        generation: int,
    ) -> Possibility:

        return Possibility(
            idea=(
                f"Combinar [{first.idea}] "
                f"con [{second.idea}]"
            ),
            generation=generation,
            origin="combined",
            metadata={
                "parents": [
                    first.idea,
                    second.idea,
                ]
            },
        )


class OmegaCore:

    VERSION = "1.0.0"

    def __init__(self):

        self.generator = GenerationEngine()
        self.evaluator = EvaluationEngine()
        self.evolution = EvolutionEngine()

        self.generation = 0
        self.history = []

    def explore(
        self,
        objective: str,
        amount: int = 8,
        cycles: int = 3,
    ):

        if not objective.strip():
            raise ValueError(
                "El objetivo no puede estar vacío."
            )

        self.generation = 0
        self.history = []

        current = self.generator.generate(
            objective,
            amount,
            self.generation,
        )

        self.history.extend(current)

        for _ in range(cycles):

            self.generation += 1

            evaluated = self.evaluator.evaluate(
                current
            )

            best = evaluated[
                :max(2, len(evaluated) // 2)
            ]

            new_possibilities = []

            for possibility in best:

                new_possibilities.append(
                    self.evolution.mutate(
                        possibility,
                        self.generation,
                    )
                )

            if len(best) >= 2:

                for _ in range(
                    max(1, len(best) // 2)
                ):

                    first, second = random.sample(
                        best,
                        2,
                    )

                    new_possibilities.append(
                        self.evolution.combine(
                            first,
                            second,
                            self.generation,
                        )
                    )

            current = self.evaluator.evaluate(
                new_possibilities
            )[:amount]

            self.history.extend(current)

        return self.evaluator.evaluate(
            current
        )

    def status(self):

        return {
            "system": "CEREBRO OMEGA",
            "version": self.VERSION,
            "status": "ONLINE",
            "generation": self.generation,
            "possibilities_explored": len(
                self.history
            ),
            "engines": {
                "generation": "ACTIVE",
                "evaluation": "ACTIVE",
                "evolution": "ACTIVE",
            },
        }

    def diagnostics(self):

        return {
            "core": "ONLINE",
            "generation_engine": "ACTIVE",
            "evaluation_engine": "ACTIVE",
            "evolution_engine": "ACTIVE",
            "memory": "NOT_CONNECTED",
            "external_ai": "NOT_CONNECTED",
            "internet": "NOT_CONNECTED",
        }
