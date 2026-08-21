from modules.supraconsciencia_omega import SupraconscienciaOmega


cerebro = SupraconscienciaOmega()

resultado = cerebro.ciclo(
    "¿Qué significa aprender?",
    "Aprender significa adquirir conocimiento mediante experiencia o estudio."
)

print("\n🧠 SUPRACONSCIENCIA OMEGA ∞")
print(resultado)

print("\n📊 ESTADO")
print(cerebro.estado_actual())
