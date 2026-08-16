"""
CEREBRO HUB
Registro central de módulos y herramientas.
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Optional


@dataclass
class Module:
    name: str
    description: str
    category: str
    function: Optional[Callable] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModuleRegistry:

    def __init__(self):
        self.modules: Dict[str, Module] = {}

    def register(
        self,
        name: str,
        description: str,
        category: str,
        function: Optional[Callable] = None,
        enabled: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.modules[name] = Module(
            name=name,
            description=description,
            category=category,
            function=function,
            enabled=enabled,
            metadata=metadata or {}
        )

    def get(self, name: str):
        return self.modules.get(name)

    def enable(self, name: str):
        if name in self.modules:
            self.modules[name].enabled = True

    def disable(self, name: str):
        if name in self.modules:
            self.modules[name].enabled = False

    def active(self):
        return {
            name: module
            for name, module in self.modules.items()
            if module.enabled
        }

    def categories(self):
        result = {}

        for module in self.modules.values():
            result.setdefault(module.category, [])
            result[module.category].append(module.name)

        return result

    def status(self):
        total = len(self.modules)
        active = len(self.active())

        return {
            "total": total,
            "active": active,
            "inactive": total - active
        }


# Registro global
HUB = ModuleRegistry()


# Módulos iniciales
HUB.register(
    "web",
    "Investigación y búsqueda de información.",
    "Investigación"
)

HUB.register(
    "matematicas",
    "Cálculos y razonamiento matemático.",
    "Ciencia"
)

HUB.register(
    "biologia",
    "Biología y ciencias de la vida.",
    "Ciencia"
)

HUB.register(
    "genetica",
    "Genética y herencia.",
    "Ciencia"
)

HUB.register(
    "evolucion",
    "Evolución y selección natural.",
    "Ciencia"
)

HUB.register(
    "biblia",
    "Estudio y análisis bíblico.",
    "Teología"
)

HUB.register(
    "musica",
    "Generación y análisis musical.",
    "Creatividad"
)

HUB.register(
    "codigo",
    "Programación y análisis de código.",
    "Tecnología"
)

HUB.register(
    "memoria",
    "Sistema de memoria de CEREBRO.",
    "Sistema"
)
