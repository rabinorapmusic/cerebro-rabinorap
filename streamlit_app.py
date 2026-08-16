import streamlit as st

# 1. CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="CEREBRO RABINO v6.3", page_icon="🧠")
st.title("🧠 CEREBRO RABINO HITMAKER v6.3")
st.write("Tu historia. Tu unción. Yo solo te ayudo a traducirla.")

# 2. LO QUE TÚ ESCRIBES
tema = st.text_input("¿De qué trata tu canción?")
flow = st.selectbox("Elige tu Flow", ["🙌 WORSHIP", "🔥 RAP", "🎸 ALABANZA", "🎤 TRAP"])

# 3. LA IA TRADUCE TU IDEA A MÚSICA
plantillas = {
    "🙌 WORSHIP": {"bpm": "70", "style": "Worship piano guitar", "acordes": "G Em C D"},
    "🔥 RAP": {"bpm": "90", "style": "Christian Rap 808", "acordes": "Am F C G"},
    "🎸 ALABANZA": {"bpm": "110", "style": "Praise guitar cajon", "acordes": "C G Am F"},
    "🎤 TRAP": {"bpm": "140", "style": "Christian Trap 808", "acordes": "Em C G D"}
}

# 4. BOTÓN QUE HACE TODO
if st.button("🚀 CREAR AHORA"):
    if tema == "":
        st.warning("Escribe primero tu tema")
    else:
        p = plantillas[flow]

        # LA IA ESCRIBE LA LETRA POR TI
        letra = f"[Verse]\n{tema}\nDios está conmigo\n\n[Chorus]\nTe adoro Señor\nUn verdadero adorador"

        # LA IA ESCRIBE EL PROMPT PARA SUNO
        prompt_suno = f"{p['style']}, {p['bpm']} BPM, Spanish\n{letra}"

        # LA IA ESCRIBE EL PROMPT PARA LA IMAGEN
        prompt_img = f"Album cover, {flow}, text {tema}, professional, 3000x3000"

        st.success("LISTO!")
        st.text_area("LETRA", letra)
        st.text_area("PROMPT SUNO", prompt_suno)
        st.text_area("PROMPT IMAGEN", prompt_img)
        st.info(f"ACORDES: {p['acordes']}")

# 5. BOTONES PARA PUBLICAR
st.divider()
st.write("SUBE TU CANCIÓN:")
col1, col2, col3 = st.columns(3)
col1.link_button("TikTok", "https://tiktok.com/upload")
col2.link_button("Instagram", "https://instagram.com")
col3.link_button("YouTube", "https://youtube.com/upload")
col1.link_button("Spotify", "https://artists.spotify.com")
col2.link_button("Apple/iPhone", "https://artists.apple.com")
col3.link_button("DistroKid", "https://distrokid.com")
