# ============================================================
# STREAMING HOUSE - V10 FIX MOBILE TITLE
# ============================================================
import streamlit as st, requests, base64, os

st.set_page_config(page_title="STREAMING HOUSE", page_icon="🎵", layout="wide")

st.markdown("""
<style>
.stApp { background: #000; color: white; }
.house-title {
    text-align: center;
    font-size: clamp(28px, 8vw, 55px);
    font-weight: 900;
    letter-spacing: 2px;
    line-height: 1.1;
    white-space: nowrap;
    margin-top: 20px;
}
.house-subtitle { text-align: center; color: #888; font-size: 14px; margin-bottom: 30px; letter-spacing: 1px; }
.result { background: #111; border: 1px solid #222; border-radius: 14px; padding: 14px; margin: 8px 0; }
.platform { background: #0f0f0f; border: 1px solid #222; border-radius: 16px; padding: 18px; text-align: center; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

if "spotify_token" not in st.session_state: st.session_state.spotify_token=None
if "search_results" not in st.session_state: st.session_state.search_results=None

def get_secret(n):
    try: return st.secrets.get(n,"")
    except: return os.getenv(n,"")

CID=get_secret("SPOTIFY_CLIENT_ID") or "4da888bafe5249b687e3ef7dd71e91db"
CSECRET=get_secret("SPOTIFY_CLIENT_SECRET") or "5b11feaa89d940f2ad9e558274a99659"

def get_token():
    cred=f"{CID}:{CSECRET}"
    enc=base64.b64encode(cred.encode()).decode()
    h={"Authorization":f"Basic {enc}","Content-Type":"application/x-www-form-urlencoded"}
    d={"grant_type":"client_credentials"}
    try:
        r=requests.post("https://accounts.spotify.com/api/token",headers=h,data=d,timeout=20)
        return r.json().get("access_token") if r.status_code==200 else None
    except: return None

def search_spotify(token, query, typ):
    headers={"Authorization":f"Bearer {token}"}
    params={"q":query,"type":typ,"limit":10,"market":"US"}
    try:
        r=requests.get("https://api.spotify.com/v1/search",headers=headers,params=params,timeout=20)
        if r.status_code==401:
            new=get_token()
            if new:
                st.session_state.spotify_token=new
                headers={"Authorization":f"Bearer {new}"}
                r=requests.get("https://api.spotify.com/v1/search",headers=headers,params=params,timeout=20)
        return r.json() if r.status_code==200 else None
    except: return None

if not st.session_state.spotify_token:
    st.session_state.spotify_token=get_token()

with st.sidebar:
    st.markdown("### ⚙️ CONTROL HOUSE")
    st.success("🟢 SPOTIFY ONLINE") if st.session_state.spotify_token else st.error("🔴 SPOTIFY OFFLINE")
    st.markdown("🟡 TIKTOK SECRETS")
    st.markdown("🟡 YOUTUBE HUB")
    st.markdown("🟡 INSTAGRAM HUB")
    st.divider()
    st.markdown("∞ RABINO RAP")
    st.markdown("☁️ CLOUD")
    st.markdown("🔐 SECRET CONTROL")
    st.markdown("⚡ API HOUSE")

st.markdown('<div class="house-title">STREAMING HOUSE</div>', unsafe_allow_html=True)
st.markdown('<div class="house-subtitle">RABINO RAP • MUSIC • DISTRIBUTION • CONTROL</div>', unsafe_allow_html=True)

st.markdown("### 🌐 PLATAFORMAS DIGITALES")
p1,p2=st.columns(2)
with p1:
    st.markdown('<div class="platform"><h3>🟢 Spotify</h3></div>', unsafe_allow_html=True)
    st.link_button("ABRIR", "https://open.spotify.com/", use_container_width=True)
    st.markdown('<div class="platform"><h3>▶️ YouTube</h3></div>', unsafe_allow_html=True)
    st.link_button("ABRIR", "https://youtube.com/", use_container_width=True)
with p2:
    st.markdown('<div class="platform"><h3>📦 DistroKid</h3></div>', unsafe_allow_html=True)
    st.link_button("ABRIR", "https://distrokid.com/", use_container_width=True)
    st.markdown('<div class="platform"><h3>📸 Instagram</h3></div>', unsafe_allow_html=True)
    st.link_button("ABRIR", "https://instagram.com/", use_container_width=True)

st.markdown("---")
st.markdown("### 🔎 SPOTIFY API ENGINE")
c1,c2=st.columns([3,1])
with c1: q=st.text_input("Buscar", "Rabino Rap", label_visibility="collapsed", placeholder="Buscar artista o canción")
with c2: typ=st.selectbox("Tipo", ["track","artist","album"], 0, label_visibility="collapsed")

if st.button("🔍 BUSCAR EN SPOTIFY", use_container_width=True, type="primary"):
    with st.spinner("Buscando..."):
        res=search_spotify(st.session_state.spotify_token, q, typ)
        st.session_state.search_results=res
        if res:
            cnt=len(res.get(f"{typ}s",{}).get("items",[]))
            st.success(f"{cnt} RESULTADOS") if cnt>0 else st.warning("0 RESULTADOS")

if st.session_state.search_results:
    res=st.session_state.search_results
    for key in ["tracks","artists","albums"]:
        if key in res and res[key]["items"]:
            for it in res[key]["items"]:
                name=it.get("name","")
                img=it.get("album",{}).get("images",[{}])[0].get("url","") if key=="tracks" else (it.get("images",[{}])[0].get("url","") if it.get("images") else "")
                url=it.get("external_urls",{}).get("spotify","")
                sub=it.get("artists",[{}])[0].get("name","") if key!="artists" else f"{it.get('followers',{}).get('total',0):,} seguidores"
                a1,a2,a3=st.columns([1,3,1])
                with a1:
                    if img: st.image(img, width=85)
                with a2:
                    st.markdown(f'<div class="result"><b>{name}</b><br><small>{sub}</small></div>', unsafe_allow_html=True)
                with a3:
                    if url: st.link_button("PLAY", url, use_container_width=True)
