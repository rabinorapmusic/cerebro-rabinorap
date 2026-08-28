import streamlit as st

# ============================================================
# STREAMING HOUSE
# Centro de control para artistas
# ============================================================

st.set_page_config(
    page_title="STREAMING HOUSE",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 50% -10%, #252525 0%, #0b0b0b 38%, #000000 80%);
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 20px;
    padding-bottom: 50px;
}

/* CABECERA */

.house-title {
    text-align: center;
    font-size: 58px;
    font-weight: 900;
    letter-spacing: 7px;
    margin-top: 10px;
    margin-bottom: 0;
}

.house-subtitle {
    text-align: center;
    font-size: 15px;
    letter-spacing: 5px;
    color: #aaaaaa;
    margin-bottom: 35px;
}

/* TARJETA ARTISTA */

.artist-card {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.10),
        rgba(255,255,255,0.025)
    );
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 25px;
    padding: 30px;
    text-align: center;
    margin-bottom: 35px;
    box-shadow: 0 15px 50px rgba(0,0,0,0.45);
}

.artist-name {
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 3px;
}

.artist-role {
    color: #aaa;
    letter-spacing: 3px;
    font-size: 13px;
}

/* SECCIONES */

.section-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* BOTONES */

div.stButton > button {
    width: 100%;
    min-height: 58px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.06);
    color: white;
    font-size: 16px;
    font-weight: 700;
    transition: 0.2s;
}

div.stButton > button:hover {
    border: 1px solid rgba(255,255,255,0.55);
    background: rgba(255,255,255,0.13);
    transform: translateY(-2px);
}

/* TARJETAS */

.platform-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 18px;
}

.platform-name {
    font-size: 21px;
    font-weight: 800;
}

.platform-description {
    color: #999;
    font-size: 13px;
    margin-top: 5px;
}

/* PANEL */

.control-panel {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px;
    padding: 25px;
    margin-top: 30px;
}

/* FOOTER */

.footer {
    text-align: center;
    margin-top: 55px;
    color: #666;
    letter-spacing: 3px;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CABECERA
# ============================================================

st.markdown(
    '<div class="house-title">STREAMING HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="house-subtitle">'
    'MUSIC • DISTRIBUTION • ARTIST CONTROL CENTER'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ARTISTA
# ============================================================

st.markdown("""
<div class="artist-card">
    <div class="artist-name">RABINO RAP</div>
    <div class="artist-role">
        ARTISTA • RAP • HIP HOP • DEMBOW • MÚSICA URBANA
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# STREAMING
# ============================================================

st.markdown(
    '<div class="section-title">🎧 PLATAFORMAS DE STREAMING</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">🟢 Spotify</div>
        <div class="platform-description">
        Música y perfil de artista
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR SPOTIFY",
        "https://open.spotify.com/",
        use_container_width=True
    )

with c2:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">🍎 Apple Music</div>
        <div class="platform-description">
        Streaming y perfil de artista
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR APPLE MUSIC",
        "https://music.apple.com/",
        use_container_width=True
    )

with c3:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">🟠 Amazon Music</div>
        <div class="platform-description">
        Streaming musical
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR AMAZON MUSIC",
        "https://music.amazon.com/",
        use_container_width=True
    )


# ============================================================
# REDES / CONTENIDO
# ============================================================

st.markdown(
    '<div class="section-title">📱 REDES Y CONTENIDO</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">🎵 TikTok</div>
        <div class="platform-description">
        Música, vídeos y promoción
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR TIKTOK",
        "https://www.tiktok.com/",
        use_container_width=True
    )

with c2:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">📸 Instagram</div>
        <div class="platform-description">
        Contenido y comunidad
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR INSTAGRAM",
        "https://www.instagram.com/",
        use_container_width=True
    )

with c3:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">▶️ YouTube</div>
        <div class="platform-description">
        Vídeos, Shorts y canal oficial
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR YOUTUBE",
        "https://www.youtube.com/",
        use_container_width=True
    )


# ============================================================
# DISTRIBUCIÓN
# ============================================================

st.markdown(
    '<div class="section-title">🚀 DISTRIBUCIÓN MUSICAL</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">🎼 DistroKid</div>
        <div class="platform-description">
        Distribución de música digital
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR DISTROKID",
        "https://distrokid.com/",
        use_container_width=True
    )

with c2:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">🎤 Spotify for Artists</div>
        <div class="platform-description">
        Estadísticas y administración del artista
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR SPOTIFY FOR ARTISTS",
        "https://artists.spotify.com/",
        use_container_width=True
    )

with c3:

    st.markdown("""
    <div class="platform-card">
        <div class="platform-name">🎵 Apple Music for Artists</div>
        <div class="platform-description">
        Datos y herramientas para artistas
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR APPLE FOR ARTISTS",
        "https://artists.apple.com/",
        use_container_width=True
    )


# ============================================================
# PANEL DEL ARTISTA
# ============================================================

st.markdown("""
<div class="control-panel">

<h2>🎛️ ARTIST CONTROL CENTER</h2>

<p style="color:#999;">
Organiza desde un solo lugar las herramientas principales
de tu carrera musical.
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# HERRAMIENTAS
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🎵\nMIS CANCIONES", use_container_width=True):
        st.info("Aquí conectaremos tu catálogo musical.")

with c2:
    if st.button("📊\nESTADÍSTICAS", use_container_width=True):
        st.info("Aquí conectaremos las estadísticas.")

with c3:
    if st.button("💰\nREGALÍAS", use_container_width=True):
        st.info("Aquí organizaremos tus regalías.")

with c4:
    if st.button("📢\nPROMOCIÓN", use_container_width=True):
        st.info("Aquí construiremos el centro de promoción.")


# ============================================================
# PERFIL
# ============================================================

st.markdown(
    '<div class="section-title">🔗 PERFIL DEL ARTISTA</div>',
    unsafe_allow_html=True
)

instagram = st.text_input(
    "Instagram",
    placeholder="https://www.instagram.com/tu_usuario"
)

spotify = st.text_input(
    "Spotify",
    placeholder="https://open.spotify.com/artist/..."
)

youtube = st.text_input(
    "YouTube",
    placeholder="https://www.youtube.com/@tu_canal"
)

if st.button(
    "💾 GUARDAR PERFIL",
    use_container_width=True
):

    st.success(
        "Perfil preparado. Los enlaces quedarán disponibles "
        "para integrarlos al panel."
    )


# ============================================================
# LANZAMIENTO
# ============================================================

st.markdown("""
<div class="control-panel">

<h2>🚀 PRÓXIMO LANZAMIENTO</h2>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    titulo = st.text_input(
        "Título de la canción",
        placeholder="Nombre del próximo tema"
    )

    fecha = st.date_input(
        "Fecha de lanzamiento"
    )

with col2:

    genero = st.selectbox(
        "Género",
        [
            "Dembow",
            "Hip Hop",
            "Rap",
            "Trap",
            "Afrobeat",
            "Reggaetón",
            "Cristiano",
            "Otro"
        ]
    )

    estado = st.selectbox(
        "Estado",
        [
            "Idea",
            "Grabando",
            "Mezcla",
            "Master",
            "Distribución",
            "Publicado"
        ]
    )

if st.button(
    "➕ REGISTRAR LANZAMIENTO",
    use_container_width=True
):

    if titulo:

        st.success(
            f"'{titulo}' registrado como próximo lanzamiento."
        )

    else:

        st.warning(
            "Escribe primero el título de la canción."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    STREAMING HOUSE ∞<br><br>
    RABINO RAP • ARTIST CONTROL CENTER
</div>
""", unsafe_allow_html=True)
