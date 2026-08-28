import streamlit as st
import base64

# ============================================================
# STREAMING HOUSE ∞
# Rabino Rap — Digital Music Hub
# V1
# ============================================================

st.set_page_config(
    page_title="STREAMING HOUSE ∞ | Rabino Rap",
    page_icon="∞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CONFIGURACIÓN DE ENLACES
# CAMBIA LOS ENLACES POR LOS TUYOS
# ============================================================

LINKS = {
    "Spotify": "https://open.spotify.com/",
    "Spotify for Artists": "https://artists.spotify.com/",
    "DistroKid": "https://distrokid.com/",
    "TikTok": "https://www.tiktok.com/",
    "Instagram": "https://www.instagram.com/",
    "YouTube": "https://www.youtube.com/",
    "Apple Music": "https://music.apple.com/",
    "Amazon Music": "https://music.amazon.com/",
    "Deezer": "https://www.deezer.com/",
    "Audiomack": "https://audiomack.com/",
    "SoundCloud": "https://soundcloud.com/",
    "Facebook": "https://www.facebook.com/"
}

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% 10%, #172554 0%, transparent 35%),
        radial-gradient(circle at 10% 80%, #0f172a 0%, transparent 35%),
        radial-gradient(circle at 90% 80%, #1e1b4b 0%, transparent 35%),
        #020617;
    color: white;
}

/* Quitar menú */
#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Contenedor principal */
.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1300px;
}

/* TÍTULO */
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    letter-spacing: 8px;
    margin-bottom: 0;
}

.infinity {
    font-size: 75px;
    font-weight: 900;
    text-align: center;
    margin: -10px 0 5px 0;
}

.subtitle {
    text-align: center;
    font-size: 15px;
    letter-spacing: 5px;
    opacity: 0.75;
    margin-bottom: 35px;
}

/* TARJETA CENTRAL */
.artist-card {
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 30px;
    padding: 35px;
    text-align: center;
    box-shadow:
        0 0 35px rgba(99,102,241,0.18),
        inset 0 0 35px rgba(255,255,255,0.02);
    margin-bottom: 35px;
}

.artist-name {
    font-size: 35px;
    font-weight: 900;
    letter-spacing: 5px;
}

.artist-role {
    font-size: 13px;
    opacity: 0.65;
    letter-spacing: 4px;
}

/* FOTO */
.photo-frame {
    width: 230px;
    height: 230px;
    border-radius: 50%;
    margin: 0 auto 25px auto;
    overflow: hidden;
    border: 3px solid rgba(255,255,255,0.5);
    box-shadow: 0 0 45px rgba(129,140,248,0.5);
}

.photo-frame img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* SECCIONES */
.section-title {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 4px;
    margin: 40px 0 20px 0;
}

/* BOTONES */
div.stButton > button {
    width: 100%;
    height: 58px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.18);
    background: rgba(15,23,42,0.85);
    color: white;
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    letter-spacing: 1px;
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-3px);
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 0 25px rgba(129,140,248,0.35);
}

/* LINKS */
a.platform {
    display: block;
    text-decoration: none;
    text-align: center;
    padding: 18px 10px;
    margin: 7px 0;
    border-radius: 15px;
    background: rgba(15,23,42,0.85);
    border: 1px solid rgba(255,255,255,0.15);
    color: white !important;
    font-weight: 700;
    letter-spacing: 1px;
    transition: 0.25s;
}

a.platform:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 25px rgba(129,140,248,0.35);
    border-color: rgba(255,255,255,0.5);
}

/* ESTADÍSTICAS */
.stat-card {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
}

.stat-number {
    font-size: 30px;
    font-weight: 900;
}

.stat-label {
    font-size: 11px;
    opacity: 0.6;
    letter-spacing: 2px;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 60px;
    opacity: 0.45;
    font-size: 11px;
    letter-spacing: 3px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FOTO DEL ARTISTA
# ============================================================

def imagen_base64(uploaded_file):
    if uploaded_file is None:
        return None

    data = uploaded_file.getvalue()
    encoded = base64.b64encode(data).decode()

    return f"data:{uploaded_file.type};base64,{encoded}"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">STREAMING HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="infinity">∞</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">RABINO RAP — DIGITAL MUSIC HUB</div>',
    unsafe_allow_html=True
)


# ============================================================
# FOTO
# ============================================================

foto = st.file_uploader(
    "UPLOAD ARTIST PHOTO",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

imagen = imagen_base64(foto)


# ============================================================
# TARJETA DEL ARTISTA
# ============================================================

if imagen:

    st.markdown(
        f"""
        <div class="artist-card">

            <div class="photo-frame">
                <img src="{imagen}">
            </div>

            <div class="artist-name">
                RABINO RAP
            </div>

            <div class="artist-role">
                ARTIST • MUSIC • DIGITAL WORLD
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div class="artist-card">

            <div style="
                font-size:120px;
                font-weight:900;
                margin-bottom:15px;
            ">
                ∞
            </div>

            <div class="artist-name">
                RABINO RAP
            </div>

            <div class="artist-role">
                UPLOAD YOUR PHOTO TO ENTER THE HOUSE
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DIGITAL MUSIC
# ============================================================

st.markdown(
    '<div class="section-title">DIGITAL MUSIC</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<a class="platform" href="{LINKS["Spotify"]}" target="_blank">🎵 SPOTIFY</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<a class="platform" href="{LINKS["Spotify for Artists"]}" target="_blank">🎤 SPOTIFY FOR ARTISTS</a>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<a class="platform" href="{LINKS["DistroKid"]}" target="_blank">🚀 DISTROKID</a>',
        unsafe_allow_html=True
    )


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<a class="platform" href="{LINKS["Apple Music"]}" target="_blank">🍎 APPLE MUSIC</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<a class="platform" href="{LINKS["Amazon Music"]}" target="_blank">🔊 AMAZON MUSIC</a>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<a class="platform" href="{LINKS["Deezer"]}" target="_blank">🎧 DEEZER</a>',
        unsafe_allow_html=True
    )


# ============================================================
# SOCIAL WORLD
# ============================================================

st.markdown(
    '<div class="section-title">SOCIAL WORLD</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<a class="platform" href="{LINKS["TikTok"]}" target="_blank">🎬 TIKTOK</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<a class="platform" href="{LINKS["Instagram"]}" target="_blank">📸 INSTAGRAM</a>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<a class="platform" href="{LINKS["YouTube"]}" target="_blank">▶️ YOUTUBE</a>',
        unsafe_allow_html=True
    )


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f'<a class="platform" href="{LINKS["Facebook"]}" target="_blank">🔵 FACEBOOK</a>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'<a class="platform" href="{LINKS["Audiomack"]}" target="_blank">🎶 AUDIOMACK</a>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'<a class="platform" href="{LINKS["SoundCloud"]}" target="_blank">☁️ SOUNDCLOUD</a>',
        unsafe_allow_html=True
    )


# ============================================================
# ESTADÍSTICAS / HUB
# ============================================================

st.markdown(
    '<div class="section-title">RABINO RAP HUB</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">MUSIC</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">CREATIVITY</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">STREAMING</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">EVOLUTION</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        STREAMING HOUSE ∞<br><br>
        RABINO RAP — DIGITAL MUSIC HUB
    </div>
    """,
    unsafe_allow_html=True
)
