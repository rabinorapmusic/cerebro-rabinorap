"""
CEREBRO OMEGA
Motor de Evaluación de Posibilidades
"""


class EvaluationEngine:
    """Evalúa y ordena posibilidades."""

    def evaluate(self, possibilities):
        results = []

        for possibility in possibilities:
            score = self._score(possibility)

            possibility.score = score
            results.append(possibility)

        return sorted(
            results,
            key=lambda item: item.score,
            reverse=True,
        )

    def _score(self, possibility):
        """
        Evaluador inicial.

        Será reemplazado posteriormente por motores
        más avanzados, simuladores o IA.
        """

        score = 0.5

        if len(possibility.idea) > 40:
            score += 0.15

        if "innovadora" in possibility.idea.lower():
            score += 0.10

        if "alternativa" in possibility.idea.lower():
            score += 0.10

        if "experimentación" in possibility.idea.lower():
            score += 0.10

        return min(score, 1.0)
