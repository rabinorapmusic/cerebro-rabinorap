# ============================================================
# STREAMING HOUSE ∞
# RABINO RAP
# V7 — ULTIMATE API HOUSE
#
# Spotify API
# TikTok OAuth READY
# DistroKid HUB
# Spotify for Artists HUB
# YouTube HUB
# Instagram HUB
# TikTok HUB
#
# NO VOLUMENES
# NO CREDENCIALES HARDCODEADAS
# ============================================================

import streamlit as st
import requests
import base64
import os
import time
from urllib.parse import urlencode


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
# ESTILO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 15% 10%, #171717 0%, #080808 35%, #000000 75%);
    color: white;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

.house-title {
    text-align: center;
    font-size: clamp(38px, 6vw, 72px);
    font-weight: 950;
    letter-spacing: 7px;
    margin-bottom: 0;
}

.house-subtitle {
    text-align: center;
    color: #888;
    font-size: 15px;
    letter-spacing: 3px;
    margin-bottom: 35px;
}

.infinity {
    text-align: center;
    font-size: 80px;
    font-weight: 900;
    line-height: 1;
    margin: 10px;
}

.section {
    font-size: 25px;
    font-weight: 900;
    letter-spacing: 2px;
    margin-top: 25px;
}

.platform {
    background: linear-gradient(145deg, #151515, #090909);
    border: 1px solid #292929;
    border-radius: 18px;
    padding: 20px;
    min-height: 185px;
    box-shadow: 0 10px 35px rgba(0,0,0,.35);
}

.platform:hover {
    border-color: #555;
}

.card {
    background: #0d0d0d;
    border: 1px solid #252525;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.result {
    background: #101010;
    border: 1px solid #272727;
    border-radius: 15px;
    padding: 14px;
}

.api-on {
    background: #10351c;
    color: #63ef87;
    padding: 7px 12px;
    border-radius: 20px;
    font-weight: 800;
    font-size: 12px;
}

.api-off {
    background: #351313;
    color: #ff7777;
    padding: 7px 12px;
    border-radius: 20px;
    font-weight: 800;
    font-size: 12px;
}

.metric {
    background: #101010;
    border: 1px solid #242424;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}

.metric-number {
    font-size: 28px;
    font-weight: 900;
}

.metric-label {
    color: #777;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.footer {
    text-align: center;
    color: #555;
    padding: 40px 10px 10px;
    letter-spacing: 2px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "spotify_token": None,
    "spotify_token_expiry": 0,
    "search_results": None,
    "artist_data": None,
    "artist_albums": None,
    "last_query": "",
    "last_type": "track",
    "tiktok_state": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SECRET MANAGER
# ============================================================

def get_secret(name, default=""):
    try:
        value = st.secrets.get(name)
        if value:
            return value
    except Exception:
        pass

    return os.getenv(name, default)


# ============================================================
# API CONFIG
# ============================================================

SPOTIFY_CLIENT_ID = get_secret("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = get_secret("SPOTIFY_CLIENT_SECRET")

TIKTOK_CLIENT_KEY = get_secret("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = get_secret("TIKTOK_CLIENT_SECRET")

APP_BASE_URL = get_secret(
    "APP_BASE_URL",
    "http://localhost:8501"
)


# ============================================================
# URLS OFICIALES
# ============================================================

URL_SPOTIFY = "https://open.spotify.com/"
URL_SPOTIFY_ARTISTS = "https://artists.spotify.com/"
URL_DISTROKID = "https://distrokid.com/"
URL_TIKTOK = "https://www.tiktok.com/"
URL_YOUTUBE = "https://www.youtube.com/"
URL_INSTAGRAM = "https://www.instagram.com/"
URL_TIKTOK_DEV = "https://developers.tiktok.com/"


# ============================================================
# UTILIDADES
# ============================================================

def fmt_number(number):
    try:
        return f"{int(number):,}"
    except Exception:
        return "0"


def safe_text(value):
    if value is None:
        return ""
    return str(value)


def spotify_configured():
    return bool(
        SPOTIFY_CLIENT_ID and
        SPOTIFY_CLIENT_SECRET
    )


def tiktok_configured():
    return bool(
        TIKTOK_CLIENT_KEY and
        TIKTOK_CLIENT_SECRET
    )


# ============================================================
# SPOTIFY — TOKEN
# ============================================================

def spotify_get_token():

    if not spotify_configured():
        return None

    # Reutilizar token válido
    if (
        st.session_state.spotify_token
        and time.time() < st.session_state.spotify_token_expiry
    ):
        return st.session_state.spotify_token

    credentials = (
        f"{SPOTIFY_CLIENT_ID}:"
        f"{SPOTIFY_CLIENT_SECRET}"
    )

    encoded = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/x-www-form-urlencoded",
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
            return None

        payload = response.json()

        token = payload.get("access_token")
        expires = int(payload.get("expires_in", 3600))

        if token:
            st.session_state.spotify_token = token
            st.session_state.spotify_token_expiry = (
                time.time() + expires - 60
            )

        return token

    except requests.RequestException:
        return None


# ============================================================
# SPOTIFY — REQUEST ENGINE
# ============================================================

def spotify_request(endpoint, params=None):

    token = spotify_get_token()

    if not token:
        return None, "Spotify API no configurada."

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:

        response = requests.get(
            f"https://api.spotify.com/v1{endpoint}",
            headers=headers,
            params=params,
            timeout=20
        )

        # Token expirado
        if response.status_code == 401:

            st.session_state.spotify_token = None
            st.session_state.spotify_token_expiry = 0

            token = spotify_get_token()

            if not token:
                return None, "No se pudo renovar el token."

            headers["Authorization"] = f"Bearer {token}"

            response = requests.get(
                f"https://api.spotify.com/v1{endpoint}",
                headers=headers,
                params=params,
                timeout=20
            )

        if response.status_code == 429:
            return None, "Spotify está limitando temporalmente las solicitudes."

        if response.status_code != 200:
            return None, (
                f"Spotify respondió HTTP "
                f"{response.status_code}"
            )

        return response.json(), None

    except requests.RequestException as error:
        return None, f"Error de conexión: {error}"


# ============================================================
# SPOTIFY — SEARCH
# ============================================================

def spotify_search(query, search_type):

    params = {
        "q": query,
        "type": search_type,
        "limit": 10,
        "market": "DO"
    }

    return spotify_request(
        "/search",
        params
    )


# ============================================================
# SPOTIFY — ARTIST
# ============================================================

def spotify_artist(artist_id):

    return spotify_request(
        f"/artists/{artist_id}"
    )


# ============================================================
# SPOTIFY — ARTIST ALBUMS
# ============================================================

def spotify_artist_albums(artist_id):

    params = {
        "include_groups": "album,single,compilation",
        "limit": 10,
        "market": "DO"
    }

    return spotify_request(
        f"/artists/{artist_id}/albums",
        params
    )


# ============================================================
# SPOTIFY — TRACK
# ============================================================

def spotify_track(track_id):

    return spotify_request(
        f"/tracks/{track_id}"
    )


# ============================================================
# SPOTIFY — ALBUM
# ============================================================

def spotify_album(album_id):

    return spotify_request(
        f"/albums/{album_id}"
    )


# ============================================================
# TIKTOK OAUTH
# ============================================================

def tiktok_authorization_url():

    if not tiktok_configured():
        return None

    state = "streaming-house-rabino"

    params = {
        "client_key": TIKTOK_CLIENT_KEY,
        "response_type": "code",
        "scope": "user.info.basic",
        "redirect_uri": APP_BASE_URL,
        "state": state
    }

    return (
        "https://www.tiktok.com/v2/auth/authorize/"
        "?" + urlencode(params)
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎛️ CONTROL HOUSE")

    st.markdown("### API STATUS")

    if spotify_configured():

        token = spotify_get_token()

        if token:
            st.markdown(
                '<span class="api-on">● SPOTIFY API ONLINE</span>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<span class="api-off">● SPOTIFY API ERROR</span>',
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            '<span class="api-off">● SPOTIFY API SIN CONFIGURAR</span>',
            unsafe_allow_html=True
        )

    st.write("")

    if tiktok_configured():

        st.markdown(
            '<span class="api-on">● TIKTOK API READY</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="api-off">● TIKTOK API NO CONFIGURADA</span>',
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("### SISTEMA")

    st.write("🟢 Streaming House")
    st.write("∞ Rabino Rap")
    st.write("☁️ Cloud Ready")
    st.write("🔐 Secrets Protected")
    st.write("⚡ API Engine V7")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="house-title">STREAMING HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="infinity">∞</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="house-subtitle">'
    'RABINO RAP • MUSIC • DISTRIBUTION • STREAMING • CONTROL'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PLATAFORMAS
# ============================================================

st.markdown(
    '<div class="section">🌐 PLATAFORMAS</div>',
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

with p1:

    st.markdown("""
    <div class="platform">
        <h2>🟢 Spotify</h2>
        <p>Streaming + Web API</p>
        <small>Catálogo, artistas, canciones y álbumes.</small>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR SPOTIFY",
        URL_SPOTIFY,
        use_container_width=True
    )

with p2:

    st.markdown("""
    <div class="platform">
        <h2>🎤 Spotify for Artists</h2>
        <p>Artist Hub</p>
        <small>Administración y herramientas para artistas.</small>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR ARTIST HUB",
        URL_SPOTIFY_ARTISTS,
        use_container_width=True
    )

with p3:

    st.markdown("""
    <div class="platform">
        <h2>📦 DistroKid</h2>
        <p>Distribution Hub</p>
        <small>Distribución y administración musical.</small>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR DISTROKID",
        URL_DISTROKID,
        use_container_width=True
    )

with p4:

    st.markdown("""
    <div class="platform">
        <h2>🎵 TikTok</h2>
        <p>Social + API</p>
        <small>Perfil, contenido y herramientas de desarrollador.</small>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR TIKTOK",
        URL_TIKTOK,
        use_container_width=True
    )


# ============================================================
# SEGUNDA FILA
# ============================================================

q1, q2, q3 = st.columns(3)

with q1:

    st.markdown("""
    <div class="platform">
        <h2>▶️ YouTube</h2>
        <p>Video Hub</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR YOUTUBE",
        URL_YOUTUBE,
        use_container_width=True
    )

with q2:

    st.markdown("""
    <div class="platform">
        <h2>📸 Instagram</h2>
        <p>Social Hub</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR INSTAGRAM",
        URL_INSTAGRAM,
        use_container_width=True
    )

with q3:

    st.markdown("""
    <div class="platform">
        <h2>⚙️ TikTok Developers</h2>
        <p>API Hub</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR DEVELOPER",
        URL_TIKTOK_DEV,
        use_container_width=True
    )


# ============================================================
# MÉTRICAS DEL SISTEMA
# ============================================================

st.divider()

st.markdown(
    '<div class="section">📊 HOUSE STATUS</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="metric">
        <div class="metric-number">∞</div>
        <div class="metric-label">House</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    status = "ONLINE" if spotify_get_token() else "OFFLINE"

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">{status}</div>
            <div class="metric-label">Spotify API</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    tstatus = "READY" if tiktok_configured() else "HUB"

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">{tstatus}</div>
            <div class="metric-label">TikTok</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:

    count = 0

    if st.session_state.search_results:

        results = st.session_state.search_results

        for key in [
            "artists",
            "tracks",
            "albums"
        ]:

            count += len(
                results.get(key, {}).get(
                    "items",
                    []
                )
            )

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">{count}</div>
            <div class="metric-label">Resultados</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BUSCADOR
# ============================================================

st.divider()

st.markdown(
    '<div class="section">🔎 SPOTIFY API ENGINE</div>',
    unsafe_allow_html=True
)

if not spotify_configured():

    st.warning(
        "Spotify API no configurada. "
        "Agrega SPOTIFY_CLIENT_ID y "
        "SPOTIFY_CLIENT_SECRET en Streamlit Secrets."
    )

c1, c2 = st.columns([4, 1])

with c1:

    search_query = st.text_input(
        "Buscar",
        value=st.session_state.last_query or "Rabino Rap",
        placeholder="Rabino Rap"
    )

with c2:

    search_type = st.selectbox(
        "Tipo",
        [
            "artist",
            "track",
            "album",
            "playlist"
        ],
        index=0
    )


if st.button(
    "🔍 BUSCAR EN SPOTIFY",
    use_container_width=True,
    type="primary"
):

    if not search_query.strip():

        st.warning("Escribe algo para buscar.")

    else:

        with st.spinner("Conectando con Spotify..."):

            data, error = spotify_search(
                search_query.strip(),
                search_type
            )

        if error:

            st.error(error)

        else:

            st.session_state.search_results = data
            st.session_state.last_query = search_query
            st.session_state.last_type = search_type

            st.success("Búsqueda completada.")


# ============================================================
# RESULTADOS
# ============================================================

if st.session_state.search_results:

    results = st.session_state.search_results

    st.markdown(
        '<div class="section">🎧 RESULTADOS</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # ARTISTAS
    # --------------------------------------------------------

    for artist in results.get(
        "artists",
        {}
    ).get(
        "items",
        []
    ):

        artist_id = artist.get("id")
        name = artist.get("name", "Sin nombre")

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

        url = artist.get(
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

        image = (
            images[0].get("url")
            if images
            else None
        )

        a1, a2, a3 = st.columns(
            [1, 4, 1]
        )

        with a1:

            if image:
                st.image(
                    image,
                    width=110
                )

        with a2:

            st.markdown(
                f"""
                <div class="result">
                    <h3>🎤 {safe_text(name)}</h3>
                    <p>Seguidores:
                    {fmt_number(followers)}</p>
                    <p>Popularidad:
                    {popularity}/100</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with a3:

            if url:

                st.link_button(
                    "VER SPOTIFY",
                    url,
                    use_container_width=True
                )

            if artist_id:

                if st.button(
                    "DETALLES",
                    key=f"artist_{artist_id}",
                    use_container_width=True
                ):

                    artist_data, error = spotify_artist(
                        artist_id
                    )

                    if error:

                        st.error(error)

                    else:

                        st.session_state.artist_data = artist_data

                        albums, album_error = spotify_artist_albums(
                            artist_id
                        )

                        if not album_error:
                            st.session_state.artist_albums = albums


    # --------------------------------------------------------
    # TRACKS
    # --------------------------------------------------------

    for track in results.get(
        "tracks",
        {}
    ).get(
        "items",
        []
    ):

        track_id = track.get("id")
        name = track.get("name", "Sin título")

        artists = ", ".join(
            [
                a.get("name", "")
                for a in track.get(
                    "artists",
                    []
                )
            ]
        )

        album = track.get(
            "album",
            {}
        )

        album_name = album.get(
            "name",
            ""
        )

        images = album.get(
            "images",
            []
        )

        image = (
            images[0].get("url")
            if images
            else None
        )

        url = track.get(
            "external_urls",
            {}
        ).get(
            "spotify",
            ""
        )

        isrc = track.get(
            "external_ids",
            {}
        ).get(
            "isrc",
            "N/D"
        )

        popularity = track.get(
            "popularity",
            0
        )

        t1, t2, t3 = st.columns(
            [1, 4, 1]
        )

        with t1:

            if image:
                st.image(
                    image,
                    width=100
                )

        with t2:

            st.markdown(
                f"""
                <div class="result">
                    <h3>🎵 {safe_text(name)}</h3>
                    <p>{safe_text(artists)}</p>
                    <p>Álbum: {safe_text(album_name)}</p>
                    <p>ISRC: {safe_text(isrc)}</p>
                    <p>Popularidad: {popularity}/100</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with t3:

            if url:

                st.link_button(
                    "▶️ ABRIR",
                    url,
                    use_container_width=True
                )


    # --------------------------------------------------------
    # ALBUMS
    # --------------------------------------------------------

    for album in results.get(
        "albums",
        {}
    ).get(
        "items",
        []
    ):

        album_id = album.get("id")

        name = album.get(
            "name",
            "Sin título"
        )

        artists = ", ".join(
            [
                a.get("name", "")
                for a in album.get(
                    "artists",
                    []
                )
            ]
        )

        url = album.get(
            "external_urls",
            {}
        ).get(
            "spotify",
            ""
        )

        images = album.get(
            "images",
            []
        )

        image = (
            images[0].get("url")
            if images
            else None
        )

        release = album.get(
            "release_date",
            "N/D"
        )

        d1, d2, d3 = st.columns(
            [1, 4, 1]
        )

        with d1:

            if image:
                st.image(
                    image,
                    width=100
                )

        with d2:

            st.markdown(
                f"""
                <div class="result">
                    <h3>💿 {safe_text(name)}</h3>
                    <p>{safe_text(artists)}</p>
                    <p>Lanzamiento: {safe_text(release)}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with d3:

            if url:

                st.link_button(
                    "VER ÁLBUM",
                    url,
                    use_container_width=True
                )


# ============================================================
# ARTISTA SELECCIONADO
# ============================================================

if st.session_state.artist_data:

    artist = st.session_state.artist_data

    st.divider()

    st.markdown(
        '<div class="section">🎤 ARTISTA SELECCIONADO</div>',
        unsafe_allow_html=True
    )

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

    url = artist.get(
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

    a1, a2 = st.columns(
        [1, 3]
    )

    with a1:

        if images:

            st.image(
                images[0].get("url"),
                width=220
            )

    with a2:

        st.markdown(
            f"""
            <div class="card">
                <h1>{safe_text(name)}</h1>
                <p>👥 Seguidores:
                {fmt_number(followers)}</p>
                <p>🔥 Popularidad:
                {popularity}/100</p>
                <p>🎼 Géneros:
                {", ".join(genres) if genres else "N/D"}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if url:

            st.link_button(
                "🎧 ABRIR ARTISTA EN SPOTIFY",
                url
            )


# ============================================================
# ÁLBUMES DEL ARTISTA
# ============================================================

if st.session_state.artist_albums:

    st.markdown(
        "### 💿 LANZAMIENTOS"
    )

    albums = st.session_state.artist_albums.get(
        "items",
        []
    )

    cols = st.columns(5)

    for index, album in enumerate(albums):

        with cols[index % 5]:

            images = album.get(
                "images",
                []
            )

            if images:

                st.image(
                    images[0].get("url")
                )

            st.markdown(
                f"**{safe_text(album.get('name'))}**"
            )

            st.caption(
                safe_text(
                    album.get(
                        "release_date",
                        ""
                    )
                )
            )

            album_url = album.get(
                "external_urls",
                {}
            ).get(
                "spotify",
                ""
            )

            if album_url:

                st.link_button(
                    "ABRIR",
                    album_url,
                    use_container_width=True
                )


# ============================================================
# TIKTOK CONTROL
# ============================================================

st.divider()

st.markdown(
    '<div class="section">🎵 TIKTOK API CONTROL</div>',
    unsafe_allow_html=True
)

if tiktok_configured():

    st.success(
        "TikTok Developer credentials configuradas."
    )

    auth_url = tiktok_authorization_url()

    if auth_url:

        st.link_button(
            "🔐 CONECTAR TIKTOK",
            auth_url,
            use_container_width=True
        )

else:

    st.info(
        "TikTok está preparado para OAuth, "
        "pero necesita TIKTOK_CLIENT_KEY y "
        "TIKTOK_CLIENT_SECRET en Secrets."
    )

    st.link_button(
        "⚙️ ABRIR TIKTOK DEVELOPERS",
        URL_TIKTOK_DEV,
        use_container_width=True
    )


# ============================================================
# DISTRIBUTION CONTROL
# ============================================================

st.divider()

st.markdown(
    '<div class="section">📦 DISTRIBUTION CONTROL</div>',
    unsafe_allow_html=True
)

d1, d2, d3 = st.columns(3)

with d1:

    st.markdown("""
    <div class="card">
        <h3>📦 DistroKid</h3>
        <p>Centro de distribución musical.</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR DISTROKID",
        URL_DISTROKID,
        use_container_width=True
    )

with d2:

    st.markdown("""
    <div class="card">
        <h3>🎤 Spotify for Artists</h3>
        <p>Control del perfil artístico.</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR ARTIST HUB",
        URL_SPOTIFY_ARTISTS,
        use_container_width=True
    )

with d3:

    st.markdown("""
    <div class="card">
        <h3>🌐 Streaming House</h3>
        <p>Panel central de Rabino Rap.</p>
    </div>
    """, unsafe_allow_html=True)

    st.success(
        "HOUSE ONLINE"
    )


# ============================================================
# CONFIGURACIÓN
# ============================================================

with st.expander("🔐 CONFIGURACIÓN DE APIs"):

    st.code("""
# .streamlit/secrets.toml

SPOTIFY_CLIENT_ID = "TU_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "TU_CLIENT_SECRET"

TIKTOK_CLIENT_KEY = "TU_CLIENT_KEY"
TIKTOK_CLIENT_SECRET = "TU_CLIENT_SECRET"

APP_BASE_URL = "https://TU-APP.streamlit.app"
""")

    st.warning(
        "Nunca publiques estas credenciales dentro del "
        "streamlit_app.py ni las subas a GitHub."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    STREAMING HOUSE ∞<br>
    RABINO RAP<br>
    MUSIC • DISTRIBUTION • STREAMING • CONTROL
</div>
""", unsafe_allow_html=True)
