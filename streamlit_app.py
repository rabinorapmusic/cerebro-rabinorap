import streamlit as st
import random

st.set_page_config(page_title="CEREBRO RABINO 🎤", page_icon="🎧", layout="centered")

st.title("🎤 CEREBRO RABINO")
st.subheader("El Generador de Rimas Más Duro del Barrio")

st.write("Escribe una palabra y te tiro 4 barras de rap al instante 🔥")

palabra = st.text_input("Tu palabra clave:", placeholder="Ej: dinero, calle, flow...")

rimas = {
    "dinero": ["Contando billete en la noche entera", "Sin ti el flow no suena ni en la cartera", "Subo en la nube y no bajo a la tierra", "Mi cadena brilla más que una esfera"],
    "calle": ["Criado en la calle, corazón de acero", "Cada esquina me conoce, yo soy el primero", "Respeto en el bloque, eso es lo verdadero", "Si hablan de mí, que sea con dinero"],
    "flow": ["Llego con el flow que tumba el sombrero", "Rompo el beat, lo dejo en el cementerio", "Dime quién rapea más duro en el hemisferio", "CEREBRO RABINO, el dueño del imperio"],
    "amor": ["Te escribo una carta con fuego y dolor", "Pero en el micrófono me vuelvo campeón", "El amor es arte, también es traición", "Por eso le canto con esta canción"],
    "vida": ["La vida es una pista y yo soy el rapero", "Cayendo y levantando, siempre guerrillero", "De Los Alcarrizos pa' to' el mundo entero", "CEREBRO RABINO, rompiendo el cerro"]
}

def generar_rap(palabra):
    palabra = palabra.lower()
    if palabra in rimas:
        barras = random.sample(rimas[palabra], 4)
    else:
        barras = [
            f"Tirando barras con la palabra {palabra}",
            "Improvisando como si fuera de NASA",
            "El micrófono quema cuando yo paso",
            "CEREBRO RABINO, rompiendo la casa"
        ]
    return "\n".join([f"**{i+1}.** {barra}" for i, barra in enumerate(barras)])

if st.button("TIRAR BARRAS 🔥"):
    if palabra:
        st.success("Aquí tienes tus 4 barras:")
        st.markdown(generar_rap(palabra))
    else:
        st.warning("Escribe una palabra primero manito")

st.markdown("---")
st.caption("Hecho con Streamlit por CEREBRO RABINO 🎧 | Los Alcarrizos 2026")
