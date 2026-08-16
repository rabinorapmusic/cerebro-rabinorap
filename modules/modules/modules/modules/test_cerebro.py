from modules.registry import HUB
from modules.health import summary
from modules.router import route


print("=" * 50)
print("🧠 CEREBRO HUB")
print("=" * 50)

estado = summary(HUB)

print(f"📦 Módulos registrados: {estado['total']}")
print(f"🟢 Disponibles: {estado['online']}")
print(f"🔴 Errores: {estado['errors']}")
print(f"⚪ Desactivados: {estado['disabled']}")

print("\n🔎 PRUEBA DEL ROUTER")

preguntas = [
    "Explícame la genética humana",
    "Investiga la evolución",
    "Hazme una canción worship",
    "Calcula una ecuación",
    "Estudia este versículo de la Biblia",
    "Necesito código Python"
]

for pregunta in preguntas:

    resultado = route(pregunta)

    print("\nPregunta:", pregunta)
    print(resultado["message"])
