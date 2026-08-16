import streamlit as st

st.set_page_config(page_title="CEREBRO RABINO v7.4", page_icon="🧠")
st.title("CEREBRO RABINO HITMAKER v7.4")

nombre_artista = st.text_input("Artist Name", "Rabino Rap")
link_ref = st.text_input("Reference Link", "")

tema = st.text_input("Song Topic", "Victoria en medio de dolor")
flow = st.selectbox("Style", ["RAP Testimonio", "TRAP Profundo", "WORSHIP Rap"])

if st.button("GENERATE", type="primary", use_container_width=True):
    if tema:
        prompt_suno = f"""[Style of Music]
Artist: {nombre_artista}
Genre: Christian Rap Spanish
Vocals: {nombre_artista} male voice, Dominican accent, powerful
Beat: {nombre_artista} type beat, 808, piano, strings
BPM: 90
Reference: {link_ref if link_ref else nombre_artista}

[Lyrics]
[Intro] {nombre_artista}
[Verse 1]
{tema}
[Chorus]
Victoria victoria en medio del dolor
{nombre_artista}
[Outro] {nombre_artista}

[Title] {tema}
"""

        prompt_img = f"Album cover, artist {nombre_artista}, title {tema}, man hoodie dark cathedral golden cross, 3000x3000"

        st.text_area("SUNO PROMPT", prompt_suno, height=300)
        st.text_area("IMAGE PROMPT", prompt_img, height=100)

        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.link_button("SUNO", "https://suno.com/")
        c2.link_button("UDIO", "https://udio.com/")
        c3.link_button("BING", "https://www.bing.com/images/create")
        c4, c5, c6 = st.columns(3)
        c4.link_button("TIKTOK", "https://www.tiktok.com/upload")
        c5.link_button("INSTAGRAM", "https://www.instagram.com/")
        c6.link_button("YOUTUBE", "https://studio.youtube.com/")
        c7, c8, c9 = st.columns(3)
        c7.link_button("SPOTIFY", "https://artists.spotify.com/")
        c8.link_button("APPLE", "https://artists.apple.com/")
        c9.link_button("DISTROKID", "https://distrokid.com/")
