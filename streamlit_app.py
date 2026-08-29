# ============================================================
# STREAMING HOUSE ∞
# RABINO RAP
# V1 — HUB DE STREAMING + DISTRIBUCIÓN
# ============================================================
#
# FUNCIONES:
# - Spotify API
# - Apple Music / iTunes Search API
# - YouTube
# - YouTube Music
# - Amazon Music
# - Deezer
# - TIDAL
# - SoundCloud
# - TikTok
# - Instagram
# - DistroKid
# - Spotify for Artists
# - Apple Music for Artists
# - Amazon Music for Artists
# - YouTube Studio
# - TikTok for Artists
# - Deezer for Creators
# - TIDAL Artist Home
# - SoundCloud for Artists
#
# IMPORTANTE:
# Las APIs privadas requieren sus propias credenciales.
# Nunca pongas secretos directamente en este archivo.
#
# ============================================================

import streamlit as st
import requests
import base64
import os
import urllib.parse
from typing import Optional


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="STREAMING HOUSE ∞",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DISEÑO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #151515 0%, #050505 35%, #000000 100%);
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

.house-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 3px;
    margin-bottom: 0;
}

.house-subtitle {
    text-align: center;
    color: #999;
    font-size: 15px;
    margin-bottom: 30px;
}

.infinity {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    margin-bottom: -10px;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    margin-top: 25px;
}

.track-card {
    background: linear-gradient(145deg, #151515, #090909);
    border-radius: 16px;
    padding: 15px;
    margin: 8px 0;
    border: 1px solid #292929;
}

.track-name {
    font-size: 19px;
    font-weight: 800;
}

.artist-name {
    color: #aaa;
    margin-top: 5px;
}

.status-card {
    background: #0d0d0d;
    border: 1px solid #252525;
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 10px;
}

.platform-card {
    background: #111;
    border: 1px solid #222;
    border-radius: 14px;
    padding: 10px;
    margin-bottom: 10px;
}

div.stButton > button,
div.stLinkButton > a {
    border-radius: 10px !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SECRETS
# ============================================================

def get_secret(name: str) -> str:
    """
    Busca primero en Streamlit Secrets.
    Si no existe, busca variable de entorno.
    """
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value).strip()
    except Exception:
        pass

    return os.getenv(name, "").strip()


# ============================================================
# SPOTIFY
# ============================================================

SPOTIFY_CLIENT_ID = get_secret("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = get_secret("SPOTIFY_CLIENT_SECRET")


@st.cache_data(ttl=3300)
def get_spotify_token() -> Optional[str]:

    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None

    credentials = (
        f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    )

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers=headers,
            data={
                "grant_type": "client_credentials"
            },
            timeout=20
        )

        if response.status_code != 200:
            return None

        return response.json().get("access_token")

    except Exception:
        return None


def spotify_search(query: str, token: str):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params={
                "q": query,
                "type": "track",
                "limit": 10
            },
            timeout=20
        )

        if response.status_code != 200:
            return []

        return response.json().get(
            "tracks",
            {}
        ).get(
            "items",
            []
        )

    except Exception:
        return []


# ============================================================
# APPLE MUSIC / ITUNES
# ============================================================

def apple_search(query: str):

    try:

        response = requests.get(
            "https://itunes.apple.com/search",
            params={
                "term": query,
                "media": "music",
                "entity": "song",
                "limit": 10
            },
            timeout=20
        )

        if response.status_code != 200:
            return []

        return response.json().get(
            "results",
            []
        )

    except Exception:
        return []


# ============================================================
# LINKS
# ============================================================

def encoded(query: str) -> str:
    return urllib.parse.quote(query)


def platform_links(query: str):

    q = encoded(query)

    return {

        "Spotify":
            f"https://open.spotify.com/search/{q}",

        "Apple Music":
            f"https://music.apple.com/search?term={q}",

        "YouTube Music":
            f"https://music.youtube.com/search?q={q}",

        "YouTube":
            f"https://www.youtube.com/results?search_query={q}",

        "Amazon Music":
            f"https://music.amazon.com/search/{q}",

        "Deezer":
            f"https://www.deezer.com/search/{q}",

        "TIDAL":
            f"https://listen.tidal.com/search?q={q}",

        "SoundCloud":
            f"https://soundcloud.com/search?q={q}",

        "TikTok":
            f"https://www.tiktok.com/search?q={q}",

        "Instagram":
            f"https://www.instagram.com/explore/search/keyword/?q={q}",

    }


# ============================================================
# ARTIST / BUSINESS LINKS
# ============================================================

ARTIST_TOOLS = {

    "DistroKid":
        "https://distrokid.com/",

    "Spotify for Artists":
        "https://artists.spotify.com/",

    "Apple Music for Artists":
        "https://artists.apple.com/",

    "YouTube Studio":
        "https://studio.youtube.com/",

    "Amazon Music for Artists":
        "https://artists.amazonmusic.com/",

    "Deezer for Creators":
        "https://creators.deezer.com/",

    "TIDAL Artist Home":
        "https://artists.tidal.com/",

    "SoundCloud for Artists":
        "https://artists.soundcloud.com/",

    "TikTok for Artists":
        "https://artists.tiktok.com/",

}


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="infinity">∞</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="house-title">STREAMING HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="house-subtitle">'
    'RABINO RAP • MUSIC • STREAMING • DISTRIBUTION'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# BUSCADOR
# ============================================================

st.markdown(
    '<div class="section-title">🔎 BUSCADOR GLOBAL</div>',
    unsafe_allow_html=True
)

query_input = st.text_input(
    "Buscar artista, canción o álbum",
    value="Rabino Rap",
    placeholder="Escribe artista o canción..."
)

if "query" not in st.session_state:
    st.session_state.query = query_input


if st.button(
    "🚀 BUSCAR EN TODAS LAS PLATAFORMAS",
    use_container_width=True,
    type="primary"
):

    st.session_state.query = query_input


query = st.session_state.get(
    "query",
    "Rabino Rap"
)


# ============================================================
# PLATAFORMAS DE BÚSQUEDA
# ============================================================

st.markdown(
    '<div class="section-title">🎧 PLATAFORMAS</div>',
    unsafe_allow_html=True
)

links = platform_links(query)

col1, col2, col3 = st.columns(3)


with col1:

    st.link_button(
        "🟢 Spotify",
        links["Spotify"],
        use_container_width=True
    )

    st.link_button(
        "🍎 Apple Music",
        links["Apple Music"],
        use_container_width=True
    )

    st.link_button(
        "▶️ YouTube Music",
        links["YouTube Music"],
        use_container_width=True

    )


with col2:

    st.link_button(
        "▶️ YouTube",
        links["YouTube"],
        use_container_width=True
    )

    st.link_button(
        "🟠 Amazon Music",
        links["Amazon Music"],
        use_container_width=True
    )

    st.link_button(
        "🔵 Deezer",
        links["Deezer"],
        use_container_width=True
    )


with col3:

    st.link_button(
        "🌊 TIDAL",
        links["TIDAL"],
        use_container_width=True
    )

    st.link_button(
        "☁️ SoundCloud",
        links["SoundCloud"],
        use_container_width=True
    )

    st.link_button(
        "🎵 TikTok",
        links["TikTok"],
        use_container_width=True
    )


st.link_button(
    "📸 Instagram",
    links["Instagram"],
    use_container_width=True
)


st.divider()


# ============================================================
# ESTADO DE SPOTIFY
# ============================================================

spotify_token = get_spotify_token()

st.markdown(
    '<div class="section-title">🔌 ESTADO DE CONEXIONES</div>',
    unsafe_allow_html=True
)

status1, status2 = st.columns(2)


with status1:

    if spotify_token:

        st.success(
            "🟢 Spotify API conectada"
        )

    else:

        st.warning(
            "🟡 Spotify API no configurada"
        )


with status2:

    st.success(
        "🟢 Apple Music Search disponible"
    )


# ============================================================
# RESULTADOS SPOTIFY
# ============================================================

if spotify_token:

    spotify_results = spotify_search(
        query,
        spotify_token
    )

    if spotify_results:

        st.markdown(
            '<div class="section-title">'
            '🟢 RESULTADOS REALES DE SPOTIFY'
            '</div>',
            unsafe_allow_html=True
        )

        for item in spotify_results:

            track_name = item.get(
                "name",
                "Sin título"
            )

            artists = ", ".join(
                artist.get("name", "")
                for artist in item.get("artists", [])
            )

            album = item.get(
                "album",
                {}
            )

            images = album.get(
                "images",
                []
            )

            image_url = (
                images[0]["url"]
                if images
                else None
            )

            spotify_url = (
                item.get("external_urls", {})
                .get("spotify", "")
            )

            col_img, col_info = st.columns(
                [1, 4]
            )

            with col_img:

                if image_url:

                    st.image(
                        image_url,
                        use_container_width=True
                    )

            with col_info:

                st.markdown(
                    f"""
                    <div class="track-card">
                        <div class="track-name">
                            {track_name}
                        </div>
                        <div class="artist-name">
                            {artists}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if spotify_url:

                    st.link_button(
                        "Abrir en Spotify",
                        spotify_url
                    )

                preview = item.get(
                    "preview_url"
                )

                if preview:

                    st.audio(preview)


# ============================================================
# RESULTADOS APPLE
# ============================================================

apple_results = apple_search(query)

if apple_results:

    st.markdown(
        '<div class="section-title">'
        '🍎 RESULTADOS REALES DE APPLE MUSIC'
        '</div>',
        unsafe_allow_html=True
    )

    for item in apple_results:

        track_name = item.get(
            "trackName",
            "Sin título"
        )

        artist_name = item.get(
            "artistName",
            "Artista desconocido"
        )

        artwork = item.get(
            "artworkUrl100"
        )

        track_url = item.get(
            "trackViewUrl"
        )

        col_img, col_info = st.columns(
            [1, 4]
        )

        with col_img:

            if artwork:

                st.image(
                    artwork,
                    use_container_width=True
                )

        with col_info:

            st.markdown(
                f"""
                <div class="track-card">
                    <div class="track-name">
                        {track_name}
                    </div>
                    <div class="artist-name">
                        {artist_name}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if track_url:

                st.link_button(
                    "Abrir en Apple Music",
                    track_url
                )


# ============================================================
# CENTRO DEL ARTISTA
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '🎤 CENTRO DEL ARTISTA'
    '</div>',
    unsafe_allow_html=True
)

st.caption(
    "Accesos oficiales para administrar perfiles, "
    "distribución y herramientas de artista."
)


artist_items = list(
    ARTIST_TOOLS.items()
)

for start in range(
    0,
    len(artist_items),
    3
):

    row = artist_items[
        start:start + 3
    ]

    columns = st.columns(3)

    for column, item in zip(
        columns,
        row
    ):

        name, url = item

        with column:

            st.link_button(
                name,
                url,
                use_container_width=True
            )


# ============================================================
# DISTRIBUCIÓN
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">'
    '📦 DISTRIBUCIÓN MUSICAL'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "Desde aquí puedes entrar a DistroKid para "
    "distribuir música y administrar lanzamientos."
)

st.link_button(
    "🚀 ABRIR DISTROKID",
    ARTIST_TOOLS["DistroKid"],
    use_container_width=True
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🎵 STREAMING HOUSE ∞"
    )

    st.markdown(
        "**Rabino Rap**"
    )

    st.divider()

    st.markdown(
        "### 🔐 APIs"
    )

    if spotify_token:

        st.success(
            "Spotify: CONECTADO"
        )

    else:

        st.error(
            "Spotify: DESCONECTADO"
        )

        st.caption(
            "Configura SPOTIFY_CLIENT_ID y "
            "SPOTIFY_CLIENT_SECRET en Secrets."
        )

    st.success(
        "Apple Search: ACTIVO"
    )

    st.divider()

    st.markdown(
        "### 🌐 Plataformas"
    )

    st.write(
        "🟢 Spotify"
    )

    st.write(
        "🍎 Apple Music"
    )

    st.write(
        "▶️ YouTube"
    )

    st.write(
        "🎵 YouTube Music"
    )

    st.write(
        "🟠 Amazon Music"
    )

    st.write(
        "🔵 Deezer"
    )

    st.write(
        "🌊 TIDAL"
    )

    st.write(
        "☁️ SoundCloud"
    )

    st.write(
        "🎵 TikTok"
    )

    st.write(
        "📸 Instagram"
    )

    st.divider()

    st.caption(
        "STREAMING HOUSE ∞"
    )

    st.caption(
        "RABINO RAP"
    )
