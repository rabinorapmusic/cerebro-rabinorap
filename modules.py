"""
CEREBRO OMEGA
MODULES — Motores especializados

Este archivo contiene capacidades que pueden ser conectadas
al núcleo sin modificar su arquitectura fundamental.
"""

import math
import random
import statistics
from dataclasses import dataclass
from typing import List, Dict, Any


# ============================================================
# 📊 MOTOR ESTADÍSTICO
# ============================================================

class StatisticsEngine:

    @staticmethod
    def analyze(values: List[float]) -> Dict[str, Any]:

        if not values:
            return {
                "count": 0,
                "mean": None,
                "median": None,
                "minimum": None,
                "maximum": None,
                "stdev": None,
            }

        result = {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "minimum": min(values),
            "maximum": max(values),
        }

        if len(values) > 1:
            result["stdev"] = statistics.stdev(values)
        else:
            result["stdev"] = 0.0

        return result


# ============================================================
# 🧮 MOTOR MATEMÁTICO
# ============================================================

class MathEngine:

    @staticmethod
    def average(a: float, b: float) -> float:
        return (a + b) / 2

    @staticmethod
    def distance(a: float, b: float) -> float:
        return abs(a - b)

    @staticmethod
    def normalize(
        value: float,
        minimum: float,
        maximum: float,
    ) -> float:

        if maximum == minimum:
            return 0.0

        return (
            (value - minimum)
            / (maximum - minimum)
        )

    @staticmethod
    def sigmoid(value: float) -> float:
        return 1 / (1 + math.exp(-value))


# ============================================================
# 🧠 MOTOR DE ALGORITMOS
# ============================================================

class AlgorithmEngine:

    @staticmethod
    def rank(items, key):
        return sorted(
            items,
            key=key,
            reverse=True,
        )

    @staticmethod
    def unique(items):
        return list(dict.fromkeys(items))

    @staticmethod
    def combinations(items, amount=10):

        if len(items) < 2:
            return []

        results = []

        for _ in range(amount):

            a, b = random.sample(
                items,
                2,
            )

            results.append(
                (a, b)
            )

        return results

    @staticmethod
    def mutate(
        value: str,
        variations=None,
    ):

        if variations is None:
            variations = [
                "simple",
                "advanced",
                "creative",
                "experimental",
                "optimized",
            ]

        variation = random.choice(
            variations
        )

        return f"{value} [{variation}]"


# ============================================================
# 🎵 MOTOR MUSICAL
# ============================================================

@dataclass
class MusicalIdea:
    bpm: int
    key: str
    scale: str
    progression: List[str]
    mood: str


class MusicEngine:

    KEYS = [
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
    ]

    MAJOR_PROGRESSIONS = [
        ["I", "V", "vi", "IV"],
        ["I", "vi", "IV", "V"],
        ["vi", "IV", "I", "V"],
        ["I", "IV", "V", "I"],
    ]

    MINOR_PROGRESSIONS = [
        ["i", "VI", "III", "VII"],
        ["i", "VII", "VI", "VII"],
        ["i", "iv", "VII", "III"],
        ["i", "VI", "VII", "V"],
    ]

    MOODS = [
        "épico",
        "melancólico",
        "alegre",
        "oscuro",
        "espiritual",
        "energético",
        "cinemático",
        "romántico",
    ]

    @classmethod
    def generate(
        cls,
        bpm=None,
        key=None,
        scale=None,
        mood=None,
    ):

        bpm = bpm or random.randint(
            70,
            150,
        )

        key = key or random.choice(
            cls.KEYS
        )

        scale = scale or random.choice(
            [
                "major",
                "minor",
            ]
        )

        mood = mood or random.choice(
            cls.MOODS
        )

        if scale == "major":
            progression = random.choice(
                cls.MAJOR_PROGRESSIONS
            )
        else:
            progression = random.choice(
                cls.MINOR_PROGRESSIONS
            )

        return MusicalIdea(
            bpm=bpm,
            key=key,
            scale=scale,
            progression=progression,
            mood=mood,
        )

    @staticmethod
    def beat_duration(bpm: int) -> float:

        if bpm <= 0:
            raise ValueError(
                "BPM debe ser mayor que cero."
            )

        return 60 / bpm

    @staticmethod
    def frequency(note_number: int) -> float:

        return 440 * (
            2 ** (
                (note_number - 69) / 12
            )
        )


# ============================================================
# 🎼 MOTOR DE ESTRUCTURA MUSICAL
# ============================================================

class SongStructureEngine:

    STRUCTURES = {
        "pop": [
            "intro",
            "verse",
            "chorus",
            "verse",
            "chorus",
            "bridge",
            "chorus",
            "outro",
        ],

        "rap": [
            "intro",
            "verse",
            "hook",
            "verse",
            "hook",
            "outro",
        ],

        "worship": [
            "intro",
            "verse",
            "chorus",
            "verse",
            "chorus",
            "bridge",
            "chorus",
            "outro",
        ],

        "dembow": [
            "intro",
            "verse",
            "hook",
            "verse",
            "hook",
            "outro",
        ],
    }

    @classmethod
    def create(cls, genre="rap"):

        genre = genre.lower()

        return cls.STRUCTURES.get(
            genre,
            cls.STRUCTURES["rap"],
        )


# ============================================================
# 🔊 MOTOR DE RITMO
# ============================================================

class RhythmEngine:

    @staticmethod
    def generate(
        steps=16,
        density=0.5,
    ):

        density = max(
            0.0,
            min(1.0, density),
        )

        return [
            1
            if random.random() < density
            else 0
            for _ in range(steps)
        ]

    @staticmethod
    def bpm_category(bpm):

        if bpm < 80:
            return "lento"

        if bpm < 110:
            return "medio"

        if bpm < 140:
            return "rápido"

        return "muy rápido"


# ============================================================
# 🧪 MOTOR EXPERIMENTAL
# ============================================================

class ExperimentEngine:

    def __init__(self):
        self.experiments = []

    def run(
        self,
        name: str,
        input_data,
        function,
    ):

        result = function(input_data)

        experiment = {
            "name": name,
            "input": input_data,
            "result": result,
        }

        self.experiments.append(
            experiment
        )

        return experiment

    def history(self):

        return list(
            self.experiments
        )


# ============================================================
# 🧭 REGISTRO CENTRAL DE MÓDULOS
# ============================================================

class ModuleRegistry:

    def __init__(self):

        self.modules = {
            "statistics": StatisticsEngine(),
            "mathematics": MathEngine(),
            "algorithms": AlgorithmEngine(),
            "music": MusicEngine(),
            "song_structure": SongStructureEngine(),
            "rhythm": RhythmEngine(),
            "experiments": ExperimentEngine(),
        }

    def get(self, name):

        return self.modules.get(name)

    def list_modules(self):

        return list(
            self.modules.keys()
        )

    def status(self):

        return {
            name: "ACTIVE"
            for name in self.modules
        }


# ============================================================
# ♾️ MOTOR UNIVERSAL DE POSIBILIDADES
# ============================================================

class PossibilityModule:

    def __init__(self):

        self.registry = ModuleRegistry()

    def explore_domains(self):

        return self.registry.list_modules()

    def status(self):

        return self.registry.status()
