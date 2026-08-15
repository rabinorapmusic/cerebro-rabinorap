import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="CEREBRO RABINO PRO", page_icon="🎤", layout="wide")
st.title("🎤 CEREBRO RABINO PRO")
st.subheader("El Generador de Rimas Más Duro + Profe de Biología")

# CONFIGURA TU API KEY EN STREAMLIT CLOUD > SETTINGS > SECRETS
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY) 
model = genai.GenerativeModel('gemini-1.5-flash')

tab1, tab2, tab3, tab4 = st.tabs(["TIRAR BARRAS", "CANCIÓN COMPLETA", "BEAT MAKER", "PROFE BIO"])

with tab1:
    palabra = st.text_input("Tu palabra clave:", placeholder="Ej: gracia, fuego, victoria")
    if st.button("TIRAR BARRAS 🔥"):
        if palabra:
            prompt = f"Eres Rabino, rapero cristiano de Los Alcarrizos. Escribe 4 barras duras con la palabra '{palabra}'. Estilo calle pero con Dios. Que rime."
            response = model.generate_content(prompt)
            st.success(response.text)
        else:
            st.warning("Pon una palabra rey")

with tab2:
    tema = st.text_input("Tema de la canción:", placeholder="Ej: Te amo Dios, Salmo 23")
    estilo = st.selectbox("Estilo:", ["Worship", "Rap Cristiano", "Adoración", "Salmo"])
    if st.button("COMPONER CANCIÓN 🙏"):
        if tema:
            prompt = f"Escribe una canción cristiana completa estilo {estilo} sobre '{tema}'. Incluye Verso 1, Coro, Verso 2 y Puente. Que ministre."
            response = model.generate_content(prompt)
            st.write(response.text)

with tab3:
    beat = st.selectbox("Elige el beat:", ["Trap Cristiano 90BPM", "Worship 70BPM", "Boom Bap 85BPM", "Adoración 65BPM"])
    if st.button("GENERAR BEAT 🎵"):
        st.info(f"Beat: {beat} seleccionado. Próximo: conectamos Suno AI para que suene.")
        st.caption("Por ahora te da la descripción del beat para que lo uses")

with tab4:
    bio_tema = st.text_input("Tema de Biología:", placeholder="Ej: Mitocondria, ADN, Célula, Fotosíntesis")
    if st.button("EXPLICAME PROFE 🧬"):
        if bio_tema:
            prompt = f"Explícame '{bio_tema}' como si fuera un profe de barrio de RD. Fácil, con ejemplo de la vida real, y 1 pregunta de examen. Sin palabras difíciles."
            response = model.generate_content(prompt)
            st.success(response.text)

st.markdown("---")
st.caption("Hecho con Streamlit + Gemini por CEREBRO RABINO | Los Alcarrizos 2026")
