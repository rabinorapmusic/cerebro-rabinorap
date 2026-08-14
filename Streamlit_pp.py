import streamlit as st
import random

st.set_page_config(
    page_title="CEREBRO RABINO CABINA PRO", 
    page_icon="👑", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# DISEÑO NEGRO + DORADO + MORADO
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

.stApp {
    background: linear-gradient(135deg, #000, #1a0033, #000000);
    color: #FFD700;
}
h1, h2, h3 {
    font-family: 'Bebas Neue', sans-serif;
    color: #FFD700!important; 
    text-shadow: 0 0 15px #8A2BE2;
}
.stButton>button {
    background: linear-gradient(90deg, #8A2BE2, #FFD700);
    color: #000; 
    border-radius: 15px; 
    font-weight: bold;
    border: 2px solid #FFD700;
    width: 100%;
    height: 3em;
    font-size: 18px;
}
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background: #1a1a1a; 
    color: #FFD700; 
    border: 2px solid #8A2BE2;
    border-radius: 10px;
}
.stTabs [data-baseweb="tab-list"] {
    background: #1a0033;
    border-radius: 10px;
}
.stTabs [data-baseweb="tab"] {
    color: #FFD700;
}
</style>
""", unsafe_allow_html=True)

st.title("👑 CEREBRO RABINO CABINA PRO v12.0")
st.subheader("Tu estudio cristiano con IA | Para la gloria de Dios")

# SIDEBAR
with st.sidebar:
    st.image("https://via.placeholder.com/300x300/000000/FFD700?text=CEREBRO+RABINO", use_column_width=True)
    st.markdown("### CONFIGURACIÓN")
    versiculo = st.selectbox("Versículo del día", [
        "Filipenses 4:13 - Todo lo puedo en Cristo",
        "Salmos 23:1 - Jehová es mi pastor",
        "Isaías 40:31 - Los que esperan a Jehová"
    ])
    st.info(f"**Palabra:** {versiculo}")

tab1, tab2, tab3 = st.tabs(["📜 ESCRITOR PROFÉTICO", "🥁 BANCO DE BEATS", "🎛️ MEZCLADOR FINAL"])

# PESTAÑA 1: ESCRITOR
with tab1:
    st.header("Escribe como los profetas")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del Artista", "RabinoRap")
        tema = st.text_input("Tema Profético", "Victoria en Cristo")
    with col2:
        estilo = st.selectbox("Unción / Estilo", ["Rap Cristiano", "Drill Cristiano", "Adoración Trap", "Reggaeton Santo"])
        tono = st.selectbox("Tono", ["Guerrero", "Adoración", "Testimonio", "Evangelístico"])
    
    if st.button("SOLTAR LA LETRA 🔥"):
        with st.spinner("El Espíritu está escribiendo..."):
            intros = [f"Yo soy {nombre}, con fuego del cielo", f"Escucha {nombre}, viene palabra", f"Atención naciones, habla {nombre}"]
            versos = [
                f"Me levanto en fe porque Cristo es mi voz\nNada me detiene, camino con el Rey\n{tema} es mi porción, lo declaro hoy\nSu palabra es espada, corta toda ley",
                f"Desde Los Alcarrizos hasta las naciones\nLlevamos el mensaje con las nuevas generaciones\nNo es por fama, es por salvación\nCEREBRO RABINO activado con unción",
                f"Caen cadenas, se abren prisiones\nPorque Jesús trae las soluciones\n{tono} es mi misión\nLlevando almas a Sion"
            ]
            hooks = [
                f"{tema}, {tema}\nEn el nombre de Jesús yo venceré\n{tema}, {tema}\nSu promesa nunca falla, lo veré",
                f"Levanta las manos, declara\nQue Cristo es tu bandera\n{tema} en tu carrera\nVictoria completa y certera"
            ]
            bridges = [
                "Todo lo puedo en Cristo que me fortalece\nFilipenses 4:13, su poder permanece",
                "No es con espada ni con ejército\nEs con mi Espíritu dice el Señor"
            ]
            
            letra = f"""[INTRO]
{random.choice(intros)}

[VERSO 1]
{random.choice(versos)}

[HOOK]
{random.choice(hooks)}

[VERSO 2]
{random.choice(versos)}

[BRIDGE]
{random.choice(bridges)}

[HOOK FINAL]
{random.choice(hooks)}

[OUTRO]
Para la gloria de Dios. CEREBRO RABINO
"""
            st.text_area("TU LETRA SANTA:", letra, height=450)
            st.download_button("DESCARGAR LETRA .TXT", letra, file_name=f"{nombre}_{tema}.txt", mime="text/plain")
            st.success("Letra generada con unción ✅")

# PESTAÑA 2: BEATS
with tab2:
    st.header("Banco de Beats Cristiano")
    st.warning("⚠️ Streamlit Cloud no soporta IA de audio aún. Usa estos links para descargar beats.")
    
    beats = [
        {"nombre": "Drill Santo 90BPM", "link": "Busca en YouTube: 'drill cristiano 90bpm beat'"},
        {"nombre": "Trap Adoración 140BPM", "link": "Busca en YouTube: 'trap adoracion beat'"},
        {"nombre": "Rap Evangelístico 85BPM", "link": "Busca en YouTube: 'rap cristiano beat 85bpm'"}
    ]
    for beat in beats:
        st.markdown(f"**{beat['nombre']}**")
        st.code(beat['link'])
    
    st.info("Tip: Descarga el beat > Grábate con BandLab > Súbelo a DistroKid")

# PESTAÑA 3: MEZCLADOR
with tab3:
    st.header("Mezcla y Domina")
    st.markdown("""
    ### PASOS PARA SOLTAR TU TEMA:
    **1. LETRA** 
    Usa el Escritor Profético y descarga tu letra.
    
    **2. BEAT**
    Descarga un beat de la pestaña 2.
    
    **3. GRABACIÓN**
    Apps recomendadas: BandLab, FL Studio Mobile, GarageBand
    
    **4. MEZCLA**
    Ecualiza voces. Quita ruidos. Ponle reverb.
    
    **5. LANZAMIENTO**
    Súbelo a YouTube, Spotify, TikTok con el hashtag #CerebroRabino
    """)
    
    st.text_area("ANOTA TUS IDEAS:", placeholder="Ideas para el próximo tema...")

st.markdown("---")
st.markdown("<center>CEREBRO RABINO © 2026 | Hecho desde Los Alcarrizos para las naciones</center>", unsafe_allow_html=True)
