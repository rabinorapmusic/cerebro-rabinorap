# ============================================================
# STREAMING HOUSE
# RABINO RAP
# PANEL CENTRAL DE DISTRIBUCIÓN + STREAMING
# ============================================================

import streamlit as st
import requests
import base64
import urllib.parse
import os
from datetime import datetime

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="STREAMING HOUSE",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #171717 0%, #050505 45%, #000000 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

.house-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    letter-spacing: 5px;
    margin-bottom: 0;
}

.house-subtitle {
    text-align: center;
    color: #999;
    font-size: 17px;
    margin-bottom: 35px;
}

.card {
    background: rgba(20,20,20,0.90);
    border: 1px solid #292929;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
}

.platform {
    background: #111;
    border: 1px solid #292929;
    border-radius: 16px;
    padding: 22px;
    min-height: 180px;
    transition: 0.2s;
}

.platform:hover {
    border-color: #777;
    transform: translateY(-2px);
}

.platform h3 {
    margin-top: 0;
}

.small {
    color: #999;
    font-size: 14px;
}

.status {
    padding: 8px 12px;
    border-radius: 20px;
    display: inline-block;
    font-size: 13px;
    font-weight: bold;
}

.connected {
    background: #123d1e;
    color: #56e57b;
}

.disconnected {
    background: #3d1212;
    color: #ff7777;
}

.result {
    background: #101010;
    border: 1px solid #292929;
    border-radius: 14px;
    padding: 18px;
    margin: 10px 0;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# VARIABLES
# ============================================================

if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = None

if "spotify_profile" not in st.session_state:
    st.session_state.spotify_profile = None

if "search_results" not in st.session_state:
    st.session_state.search_results = None

# ============================================================
# FUNCIONES SPOTIFY
# ============================================================

def spotify_get_token(client_id, client_secret):

    if not client_id or not client_secret:
        return None, "Faltan Client ID o Client Secret."

    credentials = f"{client_id}:{client_secret}"

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    try:

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers=headers,
            data=data,
            timeout=20
        )

        if response.status_code != 200:
            return None, response.text

        data = response.json()

        return data.get("access_token"), None

    except Exception as e:

        return None, str(e)


def spotify_search(token, query, search_type="artist"):

    if not token:
        return None

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": search_type,
        "limit": 10
    }

    try:

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params=params,
            timeout=20
        )

        if response.status_code != 200:
            return None

        return response.json()

    except Exception:
        return None


def spotify_artist(token, artist_id):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_id}",
            headers=headers,
            timeout=20
        )

        if response.status_code != 200:
            return None

        return response.json()

    except Exception:
        return None


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="house-title">STREAMING HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="house-subtitle">RABINO RAP • MUSIC • DISTRIBUTION • STREAMING • CONTROL</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎛️ CONTROL HOUSE")

    st.markdown("---")

    st.markdown("### 🎵 SPOTIFY API")

    spotify_client_id = st.text_input(
        "Spotify Client ID",
        type="password",
        key="spotify_client_id"
    )

    spotify_client_secret = st.text_input(
        "Spotify Client Secret",
        type="password",
        key="spotify_client_secret"
    )

    if st.button(
        "🔌 CONECTAR SPOTIFY",
        use_container_width=True
    ):

        token, error = spotify_get_token(
            spotify_client_id,
            spotify_client_secret
        )

        if token:

            st.session_state.spotify_token = token

            st.success("Spotify conectado.")

        else:

            st.session_state.spotify_token = None

            st.error("No se pudo conectar.")

            if error:
                st.caption(error)

    st.markdown("---")

    if st.session_state.spotify_token:

        st.markdown(
            '<span class="status connected">● SPOTIFY API CONECTADA</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="status disconnected">● SPOTIFY API DESCONECTADA</span>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.caption("STREAMING HOUSE")
    st.caption("RABINO RAP")
    st.caption("CEREBRO OMEGA")

# ============================================================
# PLATAFORMAS
# ============================================================

st.markdown("## 🌐 PLATAFORMAS")

p1, p2, p3, p4 = st.columns(4)

with p1:

    st.markdown("""
    <div class="platform">
        <h3>🟢 Spotify</h3>
        <p class="small">
        Streaming y consulta mediante Spotify Web API.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR SPOTIFY",
        "https://open.spotify.com/",
        use_container_width=True
    )

with p2:

    st.markdown("""
    <div class="platform">
        <h3>🎤 Spotify for Artists</h3>
        <p class="small">
        Gestión del perfil de artista y estadísticas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "SPOTIFY FOR ARTISTS",
        "https://artists.spotify.com/",
        use_container_width=True
    )

with p3:

    st.markdown("""
    <div class="platform">
        <h3>📦 DistroKid</h3>
        <p class="small">
        Distribución musical y administración de lanzamientos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR DISTROKID",
        "https://distrokid.com/",
        use_container_width=True
    )

with p4:

    st.markdown("""
    <div class="platform">
        <h3>🎵 TikTok</h3>
        <p class="small">
        Plataforma social y distribución de contenido musical.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR TIKTOK",
        "https://www.tiktok.com/",
        use_container_width=True
    )

# ============================================================
# INSTAGRAM
# ============================================================

st.markdown("")

p5, p6, p7, p8 = st.columns(4)

with p5:

    st.markdown("""
    <div class="platform">
        <h3>📸 Instagram</h3>
        <p class="small">
        Red social y promoción de contenido.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR INSTAGRAM",
        "https://www.instagram.com/",
        use_container_width=True
    )

with p6:

    st.markdown("""
    <div class="platform">
        <h3>▶️ YouTube</h3>
        <p class="small">
        Video, música y contenido oficial.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR YOUTUBE",
        "https://www.youtube.com/",
        use_container_width=True
    )

with p7:

    st.markdown("""
    <div class="platform">
        <h3>🎼 Apple Music</h3>
        <p class="small">
        Streaming y catálogo musical.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR APPLE MUSIC",
        "https://music.apple.com/",
        use_container_width=True
    )

with p8:

    st.markdown("""
    <div class="platform">
        <h3>☁️ Amazon Music</h3>
        <p class="small">
        Streaming y catálogo musical.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR AMAZON MUSIC",
        "https://music.amazon.com/",
        use_container_width=True
    )

# ============================================================
# BUSCADOR SPOTIFY
# ============================================================

st.markdown("---")

st.markdown("## 🔎 BUSCADOR SPOTIFY")

search_col1, search_col2 = st.columns([4, 1])

with search_col1:

    search_query = st.text_input(
        "Busca artista, canción o álbum",
        placeholder="Ejemplo: Rabino Rap"
    )

with search_col2:

    search_type = st.selectbox(
        "Tipo",
        ["artist", "track", "album"]
    )

if st.button(
    "🔍 BUSCAR EN SPOTIFY",
    use_container_width=True
):

    if not st.session_state.spotify_token:

        st.warning(
            "Primero conecta Spotify API desde el panel izquierdo."
        )

    elif not search_query:

        st.warning("Escribe algo para buscar.")

    else:

        result = spotify_search(
            st.session_state.spotify_token,
            search_query,
            search_type
        )

        st.session_state.search_results = result

# ============================================================
# RESULTADOS
# ============================================================

if st.session_state.search_results:

    results = st.session_state.search_results

    st.markdown("## 🎧 RESULTADOS")

    if "artists" in results:

        items = results["artists"]["items"]

        for artist in items:

            name = artist.get("name", "Sin nombre")

            artist_id = artist.get("id")

            popularity = artist.get("popularity", 0)

            followers = artist.get(
                "followers",
                {}
            ).get("total", 0)

            url = artist.get(
                "external_urls",
                {}
            ).get(
                "spotify",
                ""
            )

            images = artist.get("images", [])

            image_url = ""

            if images:
                image_url = images[0].get("url", "")

            c1, c2, c3 = st.columns([1, 3, 1])

            with c1:

                if image_url:

                    st.image(
                        image_url,
                        width=100
                    )

            with c2:

                st.markdown(
                    f"""
                    <div class="result">
                    <h3>{name}</h3>
                    <p>Seguidores: {followers:,}</p>
                    <p>Popularidad: {popularity}/100</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c3:

                if url:

                    st.link_button(
                        "🎧 VER",
                        url,
                        use_container_width=True
                    )

# ============================================================
# PANEL ARTISTA
# ============================================================

st.markdown("---")

st.markdown("## 🎤 ARTISTA")

artist_search = st.text_input(
    "Buscar perfil de artista",
    placeholder="Rabino Rap"
)

if st.button(
    "🎤 CONSULTAR ARTISTA",
    use_container_width=True
):

    if not st.session_state.spotify_token:

        st.error(
            "Conecta Spotify API primero."
        )

    elif not artist_search:

        st.warning(
            "Escribe el nombre del artista."
        )

    else:

        result = spotify_search(
            st.session_state.spotify_token,
            artist_search,
            "artist"
        )

        if result:

            artists = result.get(
                "artists",
                {}
            ).get(
                "items",
                []
            )

            if artists:

                artist = artists[0]

                st.session_state.spotify_profile = artist

            else:

                st.warning(
                    "No encontramos ese artista."
                )

# ============================================================
# MOSTRAR ARTISTA
# ============================================================

artist = st.session_state.spotify_profile

if artist:

    name = artist.get(
        "name",
        "Artista"
    )

    followers = artist.get(
        "followers",
        {}
    ).get(
        "total",
        0
    )

    popularity = artist.get(
        "popularity",
        0
    )

    genres = artist.get(
        "genres",
        []
    )

    spotify_url = artist.get(
        "external_urls",
        {}
    ).get(
        "spotify",
        ""
    )

    images = artist.get(
        "images",
        []
    )

    image_url = ""

    if images:

        image_url = images[0].get(
            "url",
            ""
        )

    a1, a2 = st.columns([1, 3])

    with a1:

        if image_url:

            st.image(
                image_url,
                width=250
            )

    with a2:

        st.markdown(
            f"# {name}"
        )

        st.metric(
            "Seguidores",
            f"{followers:,}"
        )

        st.metric(
            "Popularidad",
            f"{popularity}/100"
        )

        if genres:

            st.write(
                "Géneros:",
                ", ".join(genres)
            )

        if spotify_url:

            st.link_button(
                "🎧 ABRIR PERFIL SPOTIFY",
                spotify_url
            )

# ============================================================
# CENTRO DE LANZAMIENTOS
# ============================================================

st.markdown("---")

st.markdown("## 🚀 CENTRO DE LANZAMIENTOS")

release_name = st.text_input(
    "Nombre del lanzamiento"
)

release_artist = st.text_input(
    "Artista",
    value="Rabino Rap"
)

release_date = st.date_input(
    "Fecha del lanzamiento",
    value=datetime.now().date()
)

release_notes = st.text_area(
    "Notas del lanzamiento",
    placeholder="Información del lanzamiento..."
)

if st.button(
    "💾 PREPARAR LANZAMIENTO",
    use_container_width=True
):

    if not release_name:

        st.warning(
            "Escribe el nombre del lanzamiento."
        )

    else:

        st.success(
            f"Lanzamiento preparado: {release_name}"
        )

        st.json({
            "artista": release_artist,
            "lanzamiento": release_name,
            "fecha": str(release_date),
            "notas": release_notes
        })

# ============================================================
# CENTRO DE REDES
# ============================================================

st.markdown("---")

st.markdown("## 📲 CENTRO SOCIAL")

social_text = st.text_area(
    "Texto promocional",
    placeholder="Nuevo lanzamiento de Rabino Rap..."
)

s1, s2, s3, s4 = st.columns(4)

with s1:

    st.link_button(
        "📸 INSTAGRAM",
        "https://www.instagram.com/",
        use_container_width=True
    )

with s2:

    st.link_button(
        "🎵 TIKTOK",
        "https://www.tiktok.com/",
        use_container_width=True
    )

with s3:

    st.link_button(
        "▶️ YOUTUBE",
        "https://www.youtube.com/",
        use_container_width=True
    )

with s4:

    st.link_button(
        "🟢 SPOTIFY",
        "https://open.spotify.com/",
        use_container_width=True
    )

if social_text:

    st.markdown("### 📋 TEXTO")

    st.code(
        social_text,
        language="text"
    )

# ============================================================
# ESTADO DEL SISTEMA
# ============================================================

st.markdown("---")

st.markdown("## 🧠 ESTADO STREAMING HOUSE")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "SPOTIFY API",
        "ONLINE"
        if st.session_state.spotify_token
        else "OFFLINE"
    )

with c2:

    st.metric(
        "ARTISTA",
        "RABINO RAP"
    )

with c3:

    st.metric(
        "DISTRIBUCIÓN",
        "DISTROKID"
    )

with c4:

    st.metric(
        "SISTEMA",
        "ACTIVO"
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#666;padding:25px;">
        STREAMING HOUSE ∞<br>
        RABINO RAP<br>
        CEREBRO OMEGA
    </div>
    """,
    unsafe_allow_html=True
)
