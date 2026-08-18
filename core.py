# core.py
# ============================================================
# CEREBRO OMEGA — NÚCLEO CENTRAL
# Sistema de mandatos y principios operativos
# ============================================================

from datetime import datetime


class CerebroOmegaCore:
    """
    Núcleo central de CEREBRO OMEGA.

    El core NO crea música directamente.
    El core define reglas, prioridades, estados y decisiones
    para los módulos externos.
    """

    VERSION = "OMEGA-CORE-1.0"

    # ========================================================
    # MANDATOS FUNDAMENTALES
    # ========================================================

    MANDATOS = {
        1: "Preservar la integridad del núcleo.",
        2: "No destruir información válida existente.",
        3: "No modificar el núcleo sin autorización explícita.",
        4: "Trabajar mediante módulos independientes.",
        5: "Registrar cambios importantes.",
        6: "Aprender de los resultados sin alterar arbitrariamente el núcleo.",
        7: "Evaluar antes de ejecutar.",
        8: "Priorizar estabilidad sobre experimentación peligrosa.",
        9: "Permitir evolución progresiva.",
        10: "Mantener separación entre núcleo y módulos.",
        11: "Detectar errores antes de propagarlos.",
        12: "No inventar resultados que no hayan sido comprobados.",
        13: "Mantener trazabilidad de las decisiones.",
        14: "Permitir recuperación ante fallos.",
        15: "Conservar versiones anteriores importantes.",
        16: "No depender exclusivamente del teléfono.",
        17: "Preparar el sistema para funcionar en la nube.",
        18: "Mantener las capacidades separadas por módulos.",
        19: "Evaluar cada ciclo evolutivo.",
        20: "No considerar una prueba exitosa hasta verificar su resultado.",
        21: "Optimizar el uso de recursos disponibles.",
        22: "Evitar procesos innecesariamente pesados.",
        23: "Mantener el sistema preparado para crecer.",
        24: "Priorizar seguridad e integridad de los datos.",
        25: "Registrar el estado actual del sistema.",
    }

    # ========================================================
    # ESTADOS DEL CEREBRO
    # ========================================================

    ESTADOS = (
        "INACTIVO",
        "ANALIZANDO",
        "APRENDIENDO",
        "EJECUTANDO",
        "VERIFICANDO",
        "EVOLUCIONANDO",
        "ERROR",
        "RECUPERACION",
    )

    def __init__(self):
        self.version = self.VERSION
        self.estado = "INACTIVO"
        self.ciclo = 0
        self.memoria = []
        self.modulos = {}
        self.historial = []

    # ========================================================
    # REGISTRO
    # ========================================================

    def registrar(self, mensaje):
        evento = {
            "fecha": datetime.now().isoformat(),
            "ciclo": self.ciclo,
            "estado": self.estado,
            "mensaje": mensaje,
        }

        self.historial.append(evento)
        return evento

    # ========================================================
    # CAMBIO DE ESTADO
    # ========================================================

    def cambiar_estado(self, nuevo_estado):

        if nuevo_estado not in self.ESTADOS:
            raise ValueError(
                f"Estado no permitido: {nuevo_estado}"
            )

        self.estado = nuevo_estado

        self.registrar(
            f"Estado cambiado a {nuevo_estado}"
        )

    # ========================================================
    # REGISTRO DE MÓDULOS
    # ========================================================

    def registrar_modulo(self, nombre, modulo):

        if not nombre:
            raise ValueError("El módulo necesita un nombre.")

        self.modulos[nombre] = modulo

        self.registrar(
            f"Módulo registrado: {nombre}"
        )

        return True

    # ========================================================
    # MEMORIA
    # ========================================================

    def guardar_memoria(self, dato):

        if dato is None:
            return False

        self.memoria.append({
            "fecha": datetime.now().isoformat(),
            "dato": dato,
        })

        self.registrar(
            "Nueva información almacenada en memoria."
        )

        return True

    # ========================================================
    # ANÁLISIS
    # ========================================================

    def analizar(self, objetivo):

        self.cambiar_estado("ANALIZANDO")

        resultado = {
            "objetivo": objetivo,
            "valido": bool(objetivo),
            "modulos_disponibles": list(self.modulos.keys()),
            "ciclo": self.ciclo,
        }

        self.registrar(
            f"Objetivo analizado: {objetivo}"
        )

        return resultado

    # ========================================================
    # EJECUCIÓN
    # ========================================================

    def ejecutar(self, objetivo):

        analisis = self.analizar(objetivo)

        if not analisis["valido"]:
            self.cambiar_estado("ERROR")
            return {
                "ok": False,
                "error": "Objetivo inválido."
            }

        self.cambiar_estado("EJECUTANDO")

        resultado = {
            "ok": True,
            "objetivo": objetivo,
            "ciclo": self.ciclo,
        }

        self.registrar(
            f"Ejecución completada: {objetivo}"
        )

        self.cambiar_estado("VERIFICANDO")

        return resultado

    # ========================================================
    # VERIFICACIÓN
    # ========================================================

    def verificar(self, resultado):

        if not isinstance(resultado, dict):
            self.cambiar_estado("ERROR")

            return False

        valido = resultado.get("ok", False)

        self.registrar(
            f"Resultado verificado: {valido}"
        )

        return valido

    # ========================================================
    # CICLO EVOLUTIVO
    # ========================================================

    def evolucionar(self, aprendizaje=None):

        self.cambiar_estado("EVOLUCIONANDO")

        self.ciclo += 1

        if aprendizaje is not None:
            self.guardar_memoria(aprendizaje)

        evento = self.registrar(
            f"Ciclo evolutivo #{self.ciclo} completado."
        )

        self.cambiar_estado("INACTIVO")

        return {
            "ciclo": self.ciclo,
            "aprendizaje": aprendizaje,
            "evento": evento,
        }

    # ========================================================
    # RECUPERACIÓN
    # ========================================================

    def recuperar(self):

        self.cambiar_estado("RECUPERACION")

        self.registrar(
            "Sistema entrando en modo de recuperación."
        )

        self.cambiar_estado("INACTIVO")

        return True

    # ========================================================
    # DIAGNÓSTICO
    # ========================================================

    def diagnostico(self):

        return {
            "sistema": "CEREBRO OMEGA",
            "version": self.version,
            "estado": self.estado,
            "ciclo": self.ciclo,
            "memorias": len(self.memoria),
            "modulos": list(self.modulos.keys()),
            "eventos": len(self.historial),
            "mandatos": len(self.MANDATOS),
        }


# ============================================================
# INSTANCIA PRINCIPAL
# ============================================================

CEREBRO = CerebroOmegaCore()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("======================================")
    print("   CEREBRO OMEGA — CORE ACTIVADO")
    print("======================================")

    print()

    print("Versión:", CEREBRO.version)
    print("Estado:", CEREBRO.estado)
    print("Mandatos:", len(CEREBRO.MANDATOS))

    print()

    resultado = CEREBRO.ejecutar(
        "Analizar próxima capacidad evolutiva"
    )

    print("Resultado:", resultado)

    CEREBRO.verificar(resultado)

    CEREBRO.evolucionar(
        "El sistema completó correctamente un ciclo."
    )

    print()

    print("DIAGNÓSTICO:")
    print(CEREBRO.diagnostico())
