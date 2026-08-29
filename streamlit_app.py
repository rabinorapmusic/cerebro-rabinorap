import streamlit as st
import requests
import base64
import os

st.set_page_config(page_title="STREAMING HOUSE", layout="wide")
st.markdown("<style>.stApp{background:#000;color:white}.house-title{text-align:center;font-size:22px;font-weight:900;letter-spacing:1px}.platform{background:#111;border:1px solid #222;border-radius:12px;padding:12px;text-align:center;margin-bottom:6px;font-size:13px;font-weight:700}</style>", unsafe_allow_html=True)

if "spotify_token" not in st.session_state: st.session_state.spotify_token=None

def get_secret(n):
    try: return st.secrets.get(n,"").strip()
    except: return os.getenv(n,"").strip()

CID=get_secret("SPOTIFY_CLIENT_ID")
CSECRET=get_secret("SPOTIFY_CLIENT_SECRET")

def get_token():
    if not CID or not CSECRET: return None
    enc=base64.b64encode(f"{CID}:{CSECRET}".encode()).decode()
    h={"Authorization":f"Basic {enc}","Content-Type":"application/x-www-form-urlencoded"}
    try:
        r=requests.post("https://accounts.spotify.com/api/token",headers=h,data={"grant_type":"client_credentials"},timeout=20)
        return r.json().get("access_token") if r.status_code==200 else None
    except: return None

if not st.session_state.spotify_token and CID and CSECRET:
    st.session_state.spotify_token=get_token()

with st.sidebar:
    st.markdown("### CONTROL HOUSE")
    if st.session_state.spotify_token: st.success("SPOTIFY ONLINE")
    else: st.error("OFFLINE - Apple funciona")

st.markdown('<div class="house-title">STREAMING HOUSE</div>', unsafe_allow_html=True)
st.caption("RABINO RAP - TODAS LAS PLATAFORMAS")

st.markdown("### 🌍 TODAS LAS TIENDAS DIGITALES")

# LISTA COMPLETA 16 TIENDAS
TIENDAS = [
    ("🟢 Spotify", "https://open.spotify.com/"),
    ("🍎 Apple Music", "https://music.apple.com/"),
    ("▶️ YouTube Music", "https://music.youtube.com/"),
    ("📦 Amazon Music", "https://music.amazon.com/"),
    ("🎧 Tidal", "https://tidal.com/"),
    ("🔵 Deezer", "https://www.deezer.com/"),
    ("🟠 SoundCloud", "https://soundcloud.com/"),
    ("🎵 TikTok Music", "https://music.tiktok.com/"),
    ("📱 TikTok", "https://www.tiktok.com/"),
    ("🔴 YouTube", "https://www.youtube.com/"),
    ("📸 Instagram", "https://www.instagram.com/"),
    ("📘 Facebook / Meta", "https://www.facebook.com/"),
    ("🎶 Shazam", "https://www.shazam.com/"),
    ("💿 Pandora", "https://www.pandora.com/"),
    ("🎤 Spotify for Artists", "https://artists.spotify.com/"),
    ("🍎 Apple for Artists", "https://artists.apple.com/"),
    ("📦 DistroKid", "https://distrokid.com/"),
    ("☁️ SoundCloud Pro", "https://soundcloud.com/pro"),
]

cols = st.columns(3)
for i, (nombre, link) in enumerate(TIENDAS):
    with cols[i % 3]:
        st.markdown(f'<div class="platform">{nombre}</div>', unsafe_allow_html=True)
        st.link_button("ABRIR", link, use_container_width=True, key=f"store_{i}")

st.divider()
st.markdown("### 🔎 BUSCADOR UNIVERSAL")
q=st.text_input("Buscar","Rabino Rap")

if st.button("BUSCAR EN TODAS",type="primary",use_container_width=True):
    if st.session_state.spotify_token:
        h={"Authorization":f"Bearer {st.session_state.spotify_token}"}
        r=requests.get("https://api.spotify.com/v1/search",headers=h,params={"q":q,"type":"track","limit":5},timeout=20)
        if r.status_code==200:
            st.write("**Spotify:**")
            for it in r.json()["tracks"]["items"]:
                st.write(f"🎵 {it['name']} - {it['artists'][0]['name']}")

    # Siempre funciona - iTunes
    r=requests.get("https://itunes.apple.com/search",params={"term":q,"media":"music","limit":8},timeout=20)
    if r.status_code==200 and r.json().get("results"):
        st.write("**Apple Music / iTunes:**")
        for it in r.json()["results"]:
            c1,c2=st.columns([1,4])
            with c1:
                if it.get("artworkUrl100"): st.image(it["artworkUrl100"],width=50)
            with c2:
                st.write(f"{it.get('trackName')} - {it.get('artistName')}")
