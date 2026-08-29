import streamlit as st
import requests
import base64
import os
import urllib.parse

st.set_page_config(page_title="STREAMING HOUSE", layout="wide")

st.markdown("""
<style>
.stApp{background:#000;color:white}
.house-title{text-align:center;font-size:24px;font-weight:900}
.track-card{background:#111;border-radius:15px;padding:15px;margin:10px 0;border:1px solid #333}
</style>
""", unsafe_allow_html=True)

# SECRETS
def get_secret(n):
    try:
        return st.secrets.get(n,"").strip()
    except:
        return os.getenv(n,"").strip()

CID=get_secret("SPOTIFY_CLIENT_ID")
CSECRET=get_secret("SPOTIFY_CLIENT_SECRET")

def get_token():
    if not CID or not CSECRET:
        return None
    enc=base64.b64encode(f"{CID}:{CSECRET}".encode()).decode()
    h={"Authorization":f"Basic {enc}","Content-Type":"application/x-www-form-urlencoded"}
    try:
        r=requests.post("https://accounts.spotify.com/api/token",headers=h,data={"grant_type":"client_credentials"},timeout=20)
        return r.json().get("access_token") if r.status_code==200 else None
    except:
        return None

token=get_token()

st.markdown('<div class="house-title">STREAMING HOUSE - RABINO RAP</div>', unsafe_allow_html=True)

# BUSCADOR
q=st.text_input("Buscar artista o cancion","Rabino Rap")
if st.button("BUSCAR EN TODAS LAS PLATAFORMAS",use_container_width=True,type="primary"):
    st.session_state.q=q

query=st.session_state.get("q","Rabino Rap")
q_enc=urllib.parse.quote(query)

# BOTONES DE TODAS LAS TIENDAS CON TU BUSQUEDA
st.markdown("### Abrir tu busqueda en:")
c1,c2,c3=st.columns(3)
with c1:
    st.link_button("Spotify",f"https://open.spotify.com/search/{q_enc}",use_container_width=True)
    st.link_button("Apple Music",f"https://music.apple.com/search?term={q_enc}",use_container_width=True)
    st.link_button("YouTube Music",f"https://music.youtube.com/search?q={q_enc}",use_container_width=True)
with c2:
    st.link_button("YouTube",f"https://www.youtube.com/results?search_query={q_enc}",use_container_width=True)
    st.link_button("Amazon Music",f"https://music.amazon.com/search/{q_enc}",use_container_width=True)
    st.link_button("Deezer",f"https://www.deezer.com/search/{q_enc}",use_container_width=True)
with c3:
    st.link_button("Tidal",f"https://listen.tidal.com/search?q={q_enc}",use_container_width=True)
    st.link_button("SoundCloud",f"https://soundcloud.com/search?q={q_enc}",use_container_width=True)
    st.link_button("TikTok",f"https://www.tiktok.com/search?q={q_enc}",use_container_width=True)

st.divider()

# RESULTADOS REALES
if token:
    h={"Authorization":f"Bearer {token}"}
    r=requests.get("https://api.spotify.com/v1/search",headers=h,params={"q":query,"type":"track","limit":6},timeout=20)
    if r.status_code==200:
        st.markdown("### Resultados Spotify:")
        for it in r.json()["tracks"]["items"]:
            img=it["album"]["images"][0]["url"] if it["album"]["images"] else ""
            col1,col2=st.columns([1,3])
            with col1:
                if img:
                    st.image(img,use_container_width=True)
            with col2:
                st.markdown(f"<div class='track-card'><b>{it['name']}</b><br>{it['artists'][0]['name']}<br><a href='{it['external_urls']['spotify']}' target='_blank'>Abrir en Spotify</a></div>",unsafe_allow_html=True)
                if it.get("preview_url"):
                    st.audio(it["preview_url"])

# Apple
r=requests.get("https://itunes.apple.com/search",params={"term":query,"media":"music","limit":6},timeout=20)
if r.status_code==200 and r.json().get("results"):
    st.markdown("### Resultados Apple Music:")
    for it in r.json()["results"]:
        col1,col2=st.columns([1,3])
        with col1:
            if it.get("artworkUrl100"):
                st.image(it["artworkUrl100"],use_container_width=True)
        with col2:
            st.markdown(f"<div class='track-card'><b>{it.get('trackName')}</b><br>{it.get('artistName')}<br><a href='{it.get('trackViewUrl')}' target='_blank'>Abrir en Apple Music</a></div>",unsafe_allow_html=True)
