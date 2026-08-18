"""
CEREBRO OMEGA
CORE — Núcleo principal

El CORE coordina los módulos.
No contiene la lógica específica de conocimiento,
música, evolución, etc.

Los módulos viven de forma independiente.
"""

from pathlib import Path
import importlib
import traceback


class CerebroCore:
    """Núcleo central de CEREBRO OMEGA."""

    VERSION = "1.0.0"

    def __init__(self, modules_path="modules"):
        self.name = "CEREBRO OMEGA"

        self.modules_path = Path(modules_path)

        self.modules = {}
        self.events = []

        self.status = "initializing"

        self._load_modules()

        self.status = "online"

    # =========================================================
    # REGISTRO DE EVENTOS
    # =========================================================

    def log(self, event, data=None):
        """Registra una actividad del núcleo."""

        self.events.append(
            {
                "event": event,
                "data": data,
            }
        )

    # =========================================================
    # CARGA DE MÓDULOS
    # =========================================================

    def _load_modules(self):
        """
        Descubre módulos disponibles.

        Cada módulo puede exponer una clase llamada:
        - KnowledgeBase
        - Module
        """

        if not self.modules_path.exists():
            self.log(
                "modules_directory_missing",
                str(self.modules_path),
            )
            return

        module_files = self.modules_path.glob("*.py")

        for file in module_files:

            if file.name.startswith("_"):
                continue

            module_name = file.stem

            try:
                module = importlib.import_module(
                    f"{self.modules_path.name}.{module_name}"
                )

                self.modules[module_name] = module

                self.log(
                    "module_loaded",
                    module_name,
                )

            except Exception as error:

                self.log(
                    "module_error",
                    {
                        "module": module_name,
                        "error": str(error),
                    },
                )

    # =========================================================
    # CONSULTAR MÓDULOS
    # =========================================================

    def has_module(self, module_name):
        """Comprueba si un módulo está cargado."""

        return module_name in self.modules

    def get_module(self, module_name):
        """Devuelve un módulo cargado."""

        return self.modules.get(module_name)

    # =========================================================
    # EJECUTAR FUNCIÓN DE UN MÓDULO
    # =========================================================

    def call(self, module_name, function_name, *args, **kwargs):
        """
        Ejecuta una función perteneciente a un módulo.
        """

        module = self.get_module(module_name)

        if module is None:
            return {
                "success": False,
                "error": f"Módulo no encontrado: {module_name}",
            }

        function = getattr(
            module,
            function_name,
            None,
        )

        if function is None:
            return {
                "success": False,
                "error": (
                    f"Función no encontrada: "
                    f"{function_name}"
                ),
            }

        try:

            result = function(
                *args,
                **kwargs,
            )

            self.log(
                "module_call",
                {
                    "module": module_name,
                    "function": function_name,
                },
            )

            return {
                "success": True,
                "result": result,
            }

        except Exception as error:

            self.log(
                "execution_error",
                {
                    "module": module_name,
                    "function": function_name,
                    "error": str(error),
                },
            )

            return {
                "success": False,
                "error": str(error),
            }

    # =========================================================
    # CREAR INSTANCIA DE UN MOTOR
    # =========================================================

    def create_engine(self, module_name, class_name, *args, **kwargs):
        """
        Crea una instancia de una clase perteneciente
        a un módulo.
        """

        module = self.get_module(module_name)

        if module is None:
            return None

        engine_class = getattr(
            module,
            class_name,
            None,
        )

        if engine_class is None:
            return None

        try:

            engine = engine_class(
                *args,
                **kwargs,
            )

            self.log(
                "engine_created",
                {
                    "module": module_name,
                    "class": class_name,
                },
            )

            return engine

        except Exception as error:

            self.log(
                "engine_creation_error",
                {
                    "module": module_name,
                    "class": class_name,
                    "error": str(error),
                },
            )

            return None

    # =========================================================
    # ESTADO DEL CEREBRO
    # =========================================================

    def status_report(self):
        """Devuelve el estado actual."""

        return {
            "name": self.name,
            "version": self.VERSION,
            "status": self.status,
            "modules": list(self.modules.keys()),
            "events": len(self.events),
        }

    # =========================================================
    # REINICIO DE MÓDULOS
    # =========================================================

    def reload_modules(self):
        """Recarga los módulos."""

        self.modules.clear()

        self._load_modules()

        self.log(
            "modules_reloaded"
        )

        return list(self.modules.keys())


# =============================================================
# ARRANQUE DIRECTO
# =============================================================

def create_cerebro():
    """Crea una instancia del núcleo."""

    return CerebroCore()


# =============================================================
# PRUEBA
# =============================================================

if __name__ == "__main__":

    cerebro = create_cerebro()

    print("=" * 60)
    print("🧠 CEREBRO OMEGA")
    print("=" * 60)

    print(
        f"Versión: {cerebro.VERSION}"
    )

    print(
        f"Estado: {cerebro.status}"
    )

    print(
        f"Módulos: {cerebro.modules}"
    )

    print(
        "\nReporte:"
    )

    print(
        cerebro.status_report()
    )

    print(
        "\n✅ CORE OPERATIVO"
    )
