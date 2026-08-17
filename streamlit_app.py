import streamlit as st
import random
import statistics
from dataclasses import dataclass, field


@dataclass
class Possibility:
    idea: str
    score: float = 0.0
    generation: int = 0
    origin: str = "generated"
    metadata: dict = field(default_factory=dict)


class StatisticsEngine:

    def analyze(self, values):
        if not values:
            return {}

        return {
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "maximum": max(values),
            "minimum": min(values),
        }


class AlgorithmEngine:

    def rank(self, possibilities):
        return sorted(
            possibilities,
            key=lambda x: x.score,
            reverse=True,
        )

    def combine(self, first, second, generation):
        return Possibility(
            idea=f"Combinar: {first.idea} + {second.idea}",
            generation=generation,
            origin="combined",
        )

    def mutate(self, possibility, generation):
        variations = [
            "más simple",
            "más potente",
            "más creativa",
            "más rápida",
            "más precisa",
            "más experimental",
        ]

        return Possibility(
            idea=(
                f"Transformar {possibility.idea} "
                f"para hacerla {random.choice(variations)}"
            ),
            generation=generation,
            origin="mutated",
        )


class MusicEngine:

    def generate(self):
        keys = [
            "C", "D", "E", "F",
            "G", "A", "B"
        ]

        scales = [
            "Mayor",
            "Menor",
        ]

        progressions = [
            "I - V - vi - IV",
            "vi - IV - I - V",
            "I - vi - IV - V",
            "i - VI - III - VII",
        ]

        return {
            "bpm": random.randint(70, 150),
            "key": random.choice(keys),
            "scale": random.choice(scales),
            "progression": random.choice(progressions),
        }


class OmegaCore:

    def __init__(self):
        self.statistics = StatisticsEngine()
        self.algorithms = AlgorithmEngine()
        self.music = MusicEngine()

        self.generation = 0
        self.history = []

    def generate(self, objective, amount):

        patterns = [
            "Crear una solución para",
            "Encontrar una alternativa para",
            "Diseñar una estrategia para",
            "Explorar una posibilidad para",
            "Construir una solución avanzada para",
            "Experimentar con",
            "Combinar métodos para",
            "Descubrir una nueva forma de",
        ]

        results = []

        for _ in range(amount):

            results.append(
                Possibility(
                    idea=(
                        f"{random.choice(patterns)} "
                        f"{objective}"
                    ),
                    generation=self.generation,
                )
            )

        return results

    def evaluate(self, possibilities):

        for possibility in possibilities:

            score = random.uniform(0.45, 0.95)

            if possibility.origin == "combined":
                score += 0.05

            if possibility.origin == "mutated":
                score += 0.03

            possibility.score = min(
                score,
                1.0
            )

        return self.algorithms.rank(
            possibilities
        )

    def cycle(self, objective, amount):

        self.generation += 1

        generated = self.generate(
            objective,
            amount,
        )

        evaluated = self.evaluate(
            generated
        )

        selected = evaluated[
            :max(2, amount // 2)
        ]

        new_generation = []

        for possibility in selected:

            new_generation.append(
                self.algorithms.mutate(
                    possibility,
                    self.generation,
                )
            )

        if len(selected) >= 2:

            for _ in range(
                max(1, amount // 2)
            ):

                first, second = random.sample(
                    selected,
                    2,
                )

                new_generation.append(
                    self.algorithms.combine(
                        first,
                        second,
                        self.generation,
                    )
                )

        final = self.evaluate(
            new_generation
        )[:amount]

        self.history.extend(final)

        return {
            "generation": self.generation,
            "generated": generated,
            "selected": selected,
            "results": final,
            "statistics": self.statistics.analyze(
                [x.score for x in final]
            ),
            "music": self.music.generate(),
        }


# ============================================================
# STREAMLIT
# ============================================================

st.set_page_config(
    page_title="CEREBRO OMEGA",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 CEREBRO OMEGA ♾️")
st.caption(
    "Generador evolutivo de posibilidades"
)

objective = st.text_area(
    "🎯 Objetivo",
    placeholder="Escribe lo que quieres explorar..."
)

col1, col2 = st.columns(2)

with col1:
    amount = st.slider(
        "♾️ Posibilidades por ciclo",
        2,
        20,
        8,
    )

with col2:
    cycles = st.slider(
        "🌀 Ciclos evolutivos",
        1,
        10,
        3,
    )


if st.button(
    "⚡ EJECUTAR CEREBRO OMEGA",
    use_container_width=True,
):

    if not objective.strip():

        st.warning(
            "Escribe un objetivo."
        )

    else:

        omega = OmegaCore()

        for _ in range(cycles):

            data = omega.cycle(
                objective,
                amount,
            )

            st.divider()

            st.subheader(
                f"🌀 CICLO {data['generation']}"
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "♾️ Generadas",
                    len(data["generated"]),
                )

            with c2:
                st.metric(
                    "🏆 Seleccionadas",
                    len(data["selected"]),
                )

            with c3:
                st.metric(
                    "🧬 Nuevas",
                    len(data["results"]),
                )

            st.markdown(
                "### 📊 Estadística"
            )

            stats = data["statistics"]

            st.write(
                f"Promedio: **{stats['mean']:.2f}**"
            )

            st.write(
                f"Máximo: **{stats['maximum']:.2f}**"
            )

            st.write(
                f"Mínimo: **{stats['minimum']:.2f}**"
            )

            st.markdown(
                "### 🎵 Motor musical"
            )

            music = data["music"]

            st.write(
                f"**BPM:** {music['bpm']}  |  "
                f"**Tonalidad:** {music['key']} "
                f"{music['scale']}  |  "
                f"**Progresión:** "
                f"{music['progression']}"
            )

            st.markdown(
                "### ♾️ Posibilidades resultantes"
            )

            for number, possibility in enumerate(
                data["results"],
                1,
            ):

                st.write(
                    f"**{number}.** "
                    f"{possibility.idea}"
                )

                st.progress(
                    possibility.score
                )

                st.caption(
                    f"Origen: {possibility.origin} "
                    f"| Puntuación: "
                    f"{possibility.score:.2f}"
        )
