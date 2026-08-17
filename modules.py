import math
import random
import statistics


class StatisticsEngine:
    def analyze(self, values):
        if not values:
            return {}
        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "minimum": min(values),
            "maximum": max(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
        }


class MathEngine:
    def average(self, a, b):
        return (a + b) / 2

    def normalize(self, value, minimum, maximum):
        if maximum == minimum:
            return 0.0
        return (value - minimum) / (maximum - minimum)

    def sigmoid(self, value):
        return 1 / (1 + math.exp(-value))


class AlgorithmEngine:
    def rank(self, items, key=lambda x: x):
        return sorted(items, key=key, reverse=True)

    def unique(self, items):
        return list(dict.fromkeys(items))

    def combine(self, items, amount=5):
        if len(items) < 2:
            return []
        return [
            random.sample(items, 2)
            for _ in range(amount)
        ]

    def mutate(self, value):
        variations = [
            "simple",
            "advanced",
            "creative",
            "experimental",
            "optimized",
            "radical",
        ]
        return f"{value} [{random.choice(variations)}]"


class MusicEngine:
    KEYS = [
        "C", "C#", "D", "D#", "E", "F",
        "F#", "G", "G#", "A", "A#", "B"
    ]

    MAJOR_PROGRESSIONS = [
        ["I", "V", "vi", "IV"],
        ["I", "vi", "IV", "V"],
        ["vi", "IV", "I", "V"],
    ]

    MINOR_PROGRESSIONS = [
        ["i", "VI", "III", "VII"],
        ["i", "VII", "VI", "VII"],
        ["i", "iv", "VII", "III"],
    ]

    def generate(self, bpm=None, key=None, scale=None):
        bpm = bpm or random.randint(70, 150)
        key = key or random.choice(self.KEYS)
        scale = scale or random.choice(["major", "minor"])

        progression = random.choice(
            self.MAJOR_PROGRESSIONS
            if scale == "major"
            else self.MINOR_PROGRESSIONS
        )

        return {
            "bpm": bpm,
            "key": key,
            "scale": scale,
            "progression": progression,
        }

    def beat_duration(self, bpm):
        if bpm <= 0:
            raise ValueError("BPM inválido")
        return 60 / bpm

    def frequency(self, midi_note):
        return 440 * (2 ** ((midi_note - 69) / 12))


class RhythmEngine:
    def generate(self, steps=16, density=0.5):
        density = max(0.0, min(1.0, density))
        return [
            1 if random.random() < density else 0
            for _ in range(steps)
        ]

    def category(self, bpm):
        if bpm < 80:
            return "lento"
        if bpm < 110:
            return "medio"
        if bpm < 140:
            return "rápido"
        return "muy rápido"


class ModuleRegistry:
    def __init__(self):
        self.modules = {
            "statistics": StatisticsEngine(),
            "mathematics": MathEngine(),
            "algorithms": AlgorithmEngine(),
            "music": MusicEngine(),
            "rhythm": RhythmEngine(),
        }

    def get(self, name):
        return self.modules.get(name)

    def list_modules(self):
        return list(self.modules.keys())

    def status(self):
        return {
            name: "ACTIVE"
            for name in self.modules
        }


modules = ModuleRegistry()
