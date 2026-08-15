import streamlit as st

st.set_page_config(page_title="CEREBRO RABINO PRO", page_icon="🎤", layout="wide")

st.title("🎤 CEREBRO RABINO PRO")
st.subheader("El Generador de Rimas Más Duro + Profe de Biología")

tab1, tab2, tab3, tab4 = st.tabs(["TIRAR BARRAS", "CANCIÓN COMPLETA", "BEAT MAKER", "PROFE BIO"])

with tab1:
    palabra = st.text_input("Tu palabra clave:", placeholder="Ej: gracia, calle, flow...")
    if st.button("TIRAR BARRAS 🔥"):
        st.success(f"4 Barras sobre '{palabra}' vienen en camino...")

with tab2:
    tema = st.text_input("Tema de la canción:", placeholder="Ej: Salmo 23, Victoria")
    if st.button("COMPONER CANCIÓN 🙏"):
        st.info("Generando Verso, Coro y Puente...")

with tab3:
    estilo = st.selectbox("Elige el beat:", ["Worship", "Trap Cristiano", "Boom Bap", "Adoración"])
    if st.button("GENERAR BEAT 🎵"):
        st.warning("Aquí conectamos la IA de música después")

with tab4:
    bio_tema = st.text_input("Tema de Biología:", placeholder="Ej: Mitocondria, ADN, Célula")
    if st.button("EXPLICAME PROFE 🧬"):
        st.success(f"Explicación de '{bio_tema}' nivel barrio + nivel examen")
        
st.markdown("---")
st.caption("Hecho con Streamlit por CEREBRO RABINO | Los Alcarrizos 2026")
