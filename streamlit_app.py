# STREAMING HOUSE - V14 FIX ERROR SEARCH
import streamlit as st
import requests
import base64
import os

st.set_page_config(page_title="STREAMING HOUSE", layout="wide")

st.markdown("""
<style>
.stApp { background: #000; color: white; }
.house-title { text-align: center; font-size: 30px; font-weight: 900; white-space: nowrap; }
.house-subtitle { text-align: center; color: #888; font-size: 11px; margin-bottom: 20px; }
.platform { background: #111; border: 1px solid #222; border-radius: 14px; padding: 12px; text-align: center; margin-bottom: 6px; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = None
if "search_results" not in st.session_state:
    st.session_state.search_results = None

def get_secret(n):
    try:
        return st.secrets.get(n, "")
    except:
        return os.getenv(n, "")

CID = get_secret("SPOTIFY_CLIENT_ID")
CSECRET = get_secret("SPOTIFY_CLIENT_SECRET")

# Si no hay secrets, usa las de respaldo
if not CID:
    CID = "4da888bafe5249b687e3ef7dd71e91db"
if not CSECRET:
    CSECRET = "5b11feaa89d940f2ad9e558274a99659"

def get_token():
    if not CID or not CSECRET:
        st.error("No hay CLIENT_ID / CLIENT_SECRET en Secrets")
        return None
    cred = f"{CID}:{CSECRET}"
    enc = base64.b64encode(cred.encode()).decode()
    h = {"Authorization": f"Basic {enc}", "Content-Type": "application/x-www-form-urlencoded"}
    d = {"grant_type": "client_credentials"}
    try:
        r = requests.post("https://accounts.spotify.com/api/token", headers=h, data=d, timeout=20)
        if r.status_code == 200:
            return r.json().get("access_token")
        else:
            st.sidebar.error(f"Token falló: {r.status_code}")
            st.sidebar.code(r.text[:300])
            return None
    except Exception as e:
        st.sidebar.error(f"Error token: {e}")
        return None

def search_spotify(token, query, typ):
    if not token:
        return None, "No hay token"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": typ, "limit": 10, "market": "US"}
    try:
        r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params, timeout=20)
        if r.status_code == 200:
            return r.json(), None
        elif r.status_code == 401:
            # Token expirado, renovar
            new = get_token()
            if new:
                st.session_state.spotify_token = new
                headers = {"Authorization": f"Bearer {new}"}
                r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params, timeout=20)
                if r.status_code == 200:
                    return r.json(), None
            return None, f"401 Unauthorized - {r.text[:200]}"
        else:
            return None, f"HTTP {r.status_code} - {r.text[:300]}"
    except Exception as e:
        return None, str(e)

if not st.session_state.spotify_token:
    st.session_state.spotify_token = get_token()

with st.sidebar:
    st.markdown("### CONTROL HOUSE")
    if st.session_state.spotify_token:
        st.success("SPOTIFY ONLINE")
    else:
        st.error("SPOTIFY OFFLINE - Revisa Secrets")
        if st.button("RECONECTAR"):
            st.session_state.spotify_token = get_token()
            st.rerun()

st.markdown('<div class="house-title">STREAMING HOUSE</div>', unsafe_allow_html=True)
st.markdown('<div class="house-subtitle">RABINO RAP - TODAS LAS TIENDAS</div>', unsafe_allow_html=True)

st.markdown("### TODAS LAS TIENDAS DIGITALES")
TIENDAS = [
    ("Spotify", "https://open.spotify.com/"),
    ("Apple Music", "https://music.apple.com/"),
    ("TikTok Music", "https://music.tiktok.com/"),
    ("YouTube Music", "https://music.youtube.com/"),
    ("Amazon Music", "https://music.amazon.com/"),
    ("Tidal", "https://tidal.com/"),
    ("Deezer", "https://www.deezer.com/"),
    ("SoundCloud", "https://soundcloud.com/"),
    ("YouTube", "https://youtube.com/"),
    ("Instagram", "https://instagram.com/"),
    ("Facebook", "https://facebook.com/"),
    ("Shazam", "https://www.shazam.com/"),
    ("Spotify Artists", "https://artists.spotify.com/"),
    ("Apple Artists", "https://artists.apple.com/"),
    ("DistroKid", "https://distrokid.com/"),
    ("Pandora", "https://www.pandora.com/"),
]

cols = st.columns(2)
for i, (nombre, link) in enumerate(TIENDAS):
    with cols[i % 2]:
        st.markdown(f'<div class="platform">{nombre}</div>', unsafe_allow_html=True)
        st.link_button(f"ABRIR {nombre}", link, use_container_width=True, key=f"btn_{i}")

st.divider()
st.markdown("### BUSCADOR SPOTIFY API")
q = st.text_input("Buscar", "Rabino Rap")
typ = st.selectbox("Tipo", ["track", "artist", "album"], 0)

if st.button("BUSCAR EN SPOTIFY", use_container_width=True, type="primary"):
    with st.spinner("Buscando..."):
        res, err = search_spotify(st.session_state.spotify_token, q, typ)
        if err:
            st.error(f"Error: {err}")
        else:
            st.session_state.search_results = res
            cnt = len(res.get(f"{typ}s", {}).get("items", []))
            if cnt > 0:
                st.success(f"{cnt} RESULTADOS")
            else:
                st.warning("0 RESULTADOS")

if st.session_state.search_results:
    res = st.session_state.search_results
    for key in ["tracks", "artists", "albums"]:
        if key in res and res[key].get("items"):
            for it in res[key]["items"]:
                name = it.get("name", "")
                url = it.get("external_urls", {}).get("spotify", "")
                sub = it.get("artists", [{}])[0].get("name", "") if key!= "artists" else ""
                img = ""
                if key == "tracks" and it.get("album", {}).get("images"):
                    img = it["album"]["images"][0]["url"]
                elif it.get("images"):
                    img = it["images"][0]["url"]
                a, b, c = st.columns([1, 3, 1])
                with a:
                    if img:
                        st.image(img, width=70)
                with b:
                    st.write(f"**{name}**")
                    if sub:
                        st.caption(sub)
                with c:
                    if url:
                        st.link_button("PLAY", url, use_container_width=True)
