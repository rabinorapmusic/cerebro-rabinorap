import streamlit as st
import random
from dataclasses import dataclass, field
from typing import List, Dict


# ============================================================
# 🧠 CEREBRO OMEGA
# Núcleo evolutivo + motores fundamentales
# ============================================================

@dataclass
class Possibility:
    idea: str
    score: float = 0.0
    generation: int = 0
    origin: str = "generated"
    metadata: Dict = field(default_factory=dict)


class GenerationEngine:
    """Motor de generación."""

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

    def generate(self, objective: str, amount: int, generation: int):
        results = []

        for _ in range(amount):
            pattern = random.choice(self.patterns)

            results.append(
                Possibility(
                    idea=f"{pattern} {objective}",
                    generation=generation,
                    origin="generated",
                )
            )

        return results


class EvaluationEngine:
    """Motor de evaluación."""

    def evaluate(self, possibilities: List[Possibility]):
        for possibility in possibilities:
            score = 0.45

            length = len(possibility.idea)

            if length > 50:
                score += 0.10

            if length > 90:
                score += 0.10

            if possibility.origin == "combined":
                score += 0.15

            if possibility.origin == "mutated":
                score += 0.10

            score += random.uniform(0.0, 0.20)

            possibility.score = min(score, 1.0)

        return sorted(
            possibilities,
            key=lambda x: x.score,
            reverse=True,
        )


class EvolutionEngine:
    """Motor de combinación y mutación."""

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

    def combine(
        self,
        first: Possibility,
        second: Possibility,
        generation: int,
    ):
        idea = (
            f"Combinar [{first.idea}] "
            f"con [{second.idea}]"
        )

        return Possibility(
            idea=idea,
            generation=generation,
            origin="combined",
            metadata={
                "parents": [first.idea, second.idea]
            },
        )

    def mutate(
        self,
        possibility: Possibility,
        generation: int,
    ):
        variation = random.choice(self.variations)

        idea = (
            f"Transformar [{possibility.idea}] "
            f"haciéndolo {variation}"
        )

        return Possibility(
            idea=idea,
            generation=generation,
            origin="mutated",
            metadata={
                "parent": possibility.idea,
                "variation": variation,
            },
        )


class OmegaCore:
    """🧠 Coordinador central de OMEGA."""

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

            new_possibilities = []

            evaluated = self.evaluator.evaluate(current)

            best = evaluated[:max(2, len(evaluated) // 2)]

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

            evaluated_new = self.evaluator.evaluate(
                new_possibilities
            )

            current = evaluated_new[:amount]

            self.history.extend(current)

        return self.evaluator.evaluate(current)

    def status(self):
        return {
            "sistema": "CEREBRO OMEGA",
            "estado": "ONLINE",
            "generacion": self.generation,
            "posibilidades_exploradas": len(self.history),
            "motores": [
                "generación",
                "evaluación",
                "evolución",
            ],
        }


# ============================================================
# 🌐 INTERFAZ STREAMLIT
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 CEREBRO OMEGA ♾️")
st.caption(
    "Sistema evolutivo de exploración de posibilidades"
)

st.divider()

if "omega" not in st.session_state:
    st.session_state.omega = OmegaCore()

omega = st.session_state.omega


# ============================================================
# 🎯 ENTRADA
# ============================================================

objective = st.text_area(
    "🎯 OBJETIVO",
    placeholder=(
        "Escribe algo que quieras explorar..."
    ),
    height=100,
)

col1, col2 = st.columns(2)

with col1:
    amount = st.slider(
        "♾️ Posibilidades por ciclo",
        min_value=4,
        max_value=20,
        value=8,
    )

with col2:
    cycles = st.slider(
        "🌀 Ciclos evolutivos",
        min_value=1,
        max_value=10,
        value=3,
    )


# ============================================================
# ⚡ ACTIVACIÓN
# ============================================================

if st.button(
    "⚡ ACTIVAR CEREBRO OMEGA",
    use_container_width=True,
):

    if not objective.strip():

        st.warning(
            "⚠️ Introduce un objetivo."
        )

    else:

        with st.spinner(
            "🧠 OMEGA explorando posibilidades..."
        ):

            results = omega.explore(
                objective=objective,
                amount=amount,
                cycles=cycles,
            )

        st.success(
            "♾️ Exploración completada."
        )

        st.subheader(
            "🏆 Posibilidades seleccionadas"
        )

        for index, possibility in enumerate(
            results,
            start=1,
        ):

            with st.container():

                st.markdown(
                    f"### {index}. "
                    f"{possibility.idea}"
                )

                st.progress(
                    possibility.score
                )

                st.caption(
                    f"Generación: "
                    f"{possibility.generation}  •  "
                    f"Origen: "
                    f"{possibility.origin}  •  "
                    f"Puntuación: "
                    f"{possibility.score:.2f}"
                )

                st.divider()


# ============================================================
# 📊 ESTADO DEL SISTEMA
# ============================================================

st.subheader("📊 Estado de OMEGA")

status = omega.status()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Estado",
        status["estado"],
    )

with c2:
    st.metric(
        "Generación",
        status["generacion"],
    )

with c3:
    st.metric(
        "Exploradas",
        status["posibilidades_exploradas"],
    )

with st.expander("⚙️ Motores activos"):

    for engine in status["motores"]:
        st.write(f"⚙️ {engine}")

st.divider()

st.caption(
    "☁️ CEREBRO OMEGA — Fundación Evolutiva"
)
