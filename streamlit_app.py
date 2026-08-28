# ============================================================
# STREAMING HOUSE ∞
# RABINO RAP
# V10 — SECRET CONTROL HOUSE
#
# TODO LO SENSIBLE VIENE DE STREAMLIT SECRETS
#
# SPOTIFY
#   Client Credentials
#   Búsqueda
#   Artistas
#   Tracks
#   Álbumes
#   Playlists
#   Detalles
#
# TIKTOK
#   OAuth 2.0 READY
#
# YOUTUBE
#   Data API READY
#
# INSTAGRAM
#   Graph API READY
#
# DISTROKID / SPOTIFY FOR ARTISTS
#   HUB
#
# SIN CREDENCIALES HARDCODEADAS
# ============================================================

import streamlit as st
import requests
import base64
import os
import time
from html import escape
from urllib.parse import urlencode


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="STREAMING HOUSE ∞",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 15% 5%,
            #1c1c1c 0%,
            #080808 38%,
            #000000 80%
        );
    color: white;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.3rem;
    padding-bottom: 4rem;
}

.house-title {
    text-align: center;
    font-size: clamp(38px, 6vw, 78px);
    font-weight: 950;
    letter-spacing: 8px;
    line-height: 1;
}

.infinity {
    text-align: center;
    font-size: 100px;
    font-weight: 950;
    line-height: .9;
    margin: 12px;
}

.house-subtitle {
    text-align: center;
    color: #777;
    font-size: 14px;
    letter-spacing: 3px;
    margin-bottom: 32px;
}

.section {
    font-size: 25px;
    font-weight: 950;
    letter-spacing: 2px;
    margin-top: 25px;
    margin-bottom: 15px;
}

.platform {
    background: linear-gradient(145deg, #151515, #080808);
    border: 1px solid #292929;
    border-radius: 18px;
    padding: 20px;
    min-height: 165px;
    box-shadow: 0 12px 40px rgba(0,0,0,.30);
}

.card {
    background: #0d0d0d;
    border: 1px solid #262626;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.result {
    background: #101010;
    border: 1px solid #292929;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 12px;
}

.metric {
    background: #101010;
    border: 1px solid #262626;
    border-radius: 15px;
    padding: 18px;
    text-align: center;
    min-height: 100px;
}

.metric-number {
    font-size: 27px;
    font-weight: 950;
}

.metric-label {
    color: #777;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.api-on {
    display: inline-block;
    background: #10351c;
    color: #63ef87;
    padding: 7px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 900;
}

.api-off {
    display: inline-block;
    background: #351313;
    color: #ff7777;
    padding: 7px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 900;
}

.api-ready {
    display: inline-block;
    background: #332b10;
    color: #ffd95a;
    padding: 7px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 900;
}

.small {
    color: #777;
    font-size: 12px;
}

.footer {
    text-align: center;
    color: #444;
    padding: 50px 10px 10px;
    letter-spacing: 2px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SECRET MANAGER
# ============================================================

def get_secret(name, default=""):

    try:
        value = st.secrets.get(name, default)

        if value is not None and str(value).strip():
            return str(value).strip()

    except Exception:
        pass

    return os.getenv(name, default)


def configured(*values):

    return all(
        bool(str(v).strip())
        for v in values
    )


def safe(value):

    if value is None:
        return ""

    return escape(str(value))


def fmt(value):

    try:
        return f"{int(value):,}"
    except Exception:
        return "0"


def request_error(response):

    try:

        data = response.json()

        if isinstance(data, dict):

            if "error" in data:

                error = data["error"]

                if isinstance(error, dict):

                    return (
                        error.get("message")
                        or error.get("error")
                        or error.get("error_description")
                        or str(error)
                    )

                return str(error)

            if "message" in data:
                return str(data["message"])

            return str(data)

    except Exception:
        pass

    return f"HTTP {response.status_code}"


# ============================================================
# SECRETS
# ============================================================

SPOTIFY_CLIENT_ID = get_secret(
    "SPOTIFY_CLIENT_ID"
)

SPOTIFY_CLIENT_SECRET = get_secret(
    "SPOTIFY_CLIENT_SECRET"
)

SPOTIFY_REDIRECT_URI = get_secret(
    "SPOTIFY_REDIRECT_URI"
)

TIKTOK_CLIENT_KEY = get_secret(
    "TIKTOK_CLIENT_KEY"
)

TIKTOK_CLIENT_SECRET = get_secret(
    "TIKTOK_CLIENT_SECRET"
)

TIKTOK_REDIRECT_URI = get_secret(
    "TIKTOK_REDIRECT_URI"
)

TIKTOK_ACCESS_TOKEN = get_secret(
    "TIKTOK_ACCESS_TOKEN"
)

YOUTUBE_API_KEY = get_secret(
    "YOUTUBE_API_KEY"
)

INSTAGRAM_ACCESS_TOKEN = get_secret(
    "INSTAGRAM_ACCESS_TOKEN"
)

INSTAGRAM_BUSINESS_ACCOUNT_ID = get_secret(
    "INSTAGRAM_BUSINESS_ACCOUNT_ID"
)

META_APP_ID = get_secret(
    "META_APP_ID"
)

META_APP_SECRET = get_secret(
    "META_APP_SECRET"
)

APP_BASE_URL = get_secret(
    "APP_BASE_URL",
    ""
).rstrip("/")


# ============================================================
# URLs
# ============================================================

URL_SPOTIFY = "https://open.spotify.com/"
URL_SPOTIFY_ARTISTS = "https://artists.spotify.com/"
URL_SPOTIFY_DEV = "https://developer.spotify.com/"

URL_DISTROKID = "https://distrokid.com/"

URL_TIKTOK = "https://www.tiktok.com/"
URL_TIKTOK_DEV = "https://developers.tiktok.com/"

URL_YOUTUBE = "https://www.youtube.com/"
URL_YOUTUBE_DEV = "https://console.cloud.google.com/"

URL_INSTAGRAM = "https://www.instagram.com/"
URL_INSTAGRAM_DEV = "https://developers.facebook.com/"


# ============================================================
# API ENDPOINTS
# ============================================================

SPOTIFY_TOKEN_URL = (
    "https://accounts.spotify.com/api/token"
)

SPOTIFY_API_URL = (
    "https://api.spotify.com/v1"
)

YOUTUBE_API_URL = (
    "https://www.googleapis.com/youtube/v3"
)

INSTAGRAM_API_URL = (
    "https://graph.facebook.com/v23.0"
)

TIKTOK_AUTH_URL = (
    "https://www.tiktok.com/v2/auth/authorize/"
)

TIKTOK_TOKEN_URL = (
    "https://open.tiktokapis.com/v2/oauth/token/"
)

TIKTOK_USER_INFO_URL = (
    "https://open.tiktokapis.com/v2/user/info/"
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULTS = {

    "spotify_token": None,
    "spotify_expiry": 0,

    "search_results": None,

    "selected_artist": None,
    "selected_album": None,
    "selected_track": None,

    "youtube_results": None,

    "instagram_data": None,

    "tiktok_data": None,

    "last_query": "Rabino Rap",

    "last_type": "artist",

    "tiktok_state": None,
}

for key, value in DEFAULTS.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# SPOTIFY CONFIG
# ============================================================

def spotify_configured():

    return configured(
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET
    )


# ============================================================
# SPOTIFY TOKEN
# ============================================================

def spotify_get_token():

    if not spotify_configured():

        return None

    if (
        st.session_state.spotify_token
        and time.time()
        < st.session_state.spotify_expiry
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

        "Authorization":
            f"Basic {encoded}",

        "Content-Type":
            "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type":
            "client_credentials"
    }

    try:

        response = requests.post(

            SPOTIFY_TOKEN_URL,

            headers=headers,

            data=data,

            timeout=20,
        )

        if response.status_code != 200:

            return None

        payload = response.json()

        token = payload.get(
            "access_token"
        )

        expires = int(
            payload.get(
                "expires_in",
                3600
            )
        )

        if token:

            st.session_state.spotify_token = token

            st.session_state.spotify_expiry = (
                time.time()
                + expires
                - 60
            )

        return token

    except requests.RequestException:

        return None


# ============================================================
# SPOTIFY REQUEST
# ============================================================

def spotify_request(
    endpoint,
    params=None
):

    token = spotify_get_token()

    if not token:

        return (
            None,
            "Spotify no pudo autenticar. "
            "Revisa SPOTIFY_CLIENT_ID y "
            "SPOTIFY_CLIENT_SECRET en Secrets."
        )

    headers = {
        "Authorization":
            f"Bearer {token}"
    }

    try:

        response = requests.get(

            f"{SPOTIFY_API_URL}{endpoint}",

            headers=headers,

            params=params,

            timeout=20,
        )

        if response.status_code == 401:

            st.session_state.spotify_token = None
            st.session_state.spotify_expiry = 0

            token = spotify_get_token()

            if not token:

                return (
                    None,
                    "Spotify rechazó las credenciales."
                )

            headers["Authorization"] = (
                f"Bearer {token}"
            )

            response = requests.get(

                f"{SPOTIFY_API_URL}{endpoint}",

                headers=headers,

                params=params,

                timeout=20,
            )

        if response.status_code == 429:

            retry = response.headers.get(
                "Retry-After",
                "unos segundos"
            )

            return (
                None,
                f"Spotify está limitando solicitudes. "
                f"Espera {retry}."
            )

        if response.status_code != 200:

            return (
                None,
                request_error(response)
            )

        return response.json(), None

    except requests.RequestException as error:

        return (
            None,
            f"Error de conexión con Spotify: {error}"
        )


# ============================================================
# SPOTIFY SEARCH
# ============================================================

def spotify_search(query, search_type):

    return spotify_request(
        "/search",
        {
            "q": query,
            "type": search_type,
            "limit": 10,
            "market": "DO",
        },
    )


def spotify_artist(artist_id):

    return spotify_request(
        f"/artists/{artist_id}"
    )


def spotify_artist_albums(artist_id):

    return spotify_request(
        f"/artists/{artist_id}/albums",
        {
            "include_groups":
                "album,single,compilation",
            "limit": 20,
            "market": "DO",
        },
    )


def spotify_track(track_id):

    return spotify_request(
        f"/tracks/{track_id}"
    )


def spotify_album(album_id):

    return spotify_request(
        f"/albums/{album_id}"
    )


# ============================================================
# TIKTOK OAUTH
# ============================================================

def tiktok_configured():

    return configured(
        TIKTOK_CLIENT_KEY,
        TIKTOK_CLIENT_SECRET,
        TIKTOK_REDIRECT_URI
    )


def tiktok_authorization_url():

    if not tiktok_configured():

        return None

    state = base64.urlsafe_b64encode(
        os.urandom(24)
    ).decode("utf-8").rstrip("=")

    st.session_state.tiktok_state = state

    params = {

        "client_key":
            TIKTOK_CLIENT_KEY,

        "response_type":
            "code",

        "scope":
            "user.info.basic",

        "redirect_uri":
            TIKTOK_REDIRECT_URI,

        "state":
            state,
    }

    return (
        f"{TIKTOK_AUTH_URL}"
        f"?{urlencode(params)}"
    )


def tiktok_exchange_code(code):

    if not tiktok_configured():

        return (
            None,
            "TikTok Secrets incompletos."
        )

    data = {

        "client_key":
            TIKTOK_CLIENT_KEY,

        "client_secret":
            TIKTOK_CLIENT_SECRET,

        "code":
            code,

        "grant_type":
            "authorization_code",

        "redirect_uri":
            TIKTOK_REDIRECT_URI,
    }

    try:

        response = requests.post(

            TIKTOK_TOKEN_URL,

            headers={
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },

            data=data,

            timeout=20,
        )

        if response.status_code != 200:

            return (
                None,
                request_error(response)
            )

        return response.json(), None

    except requests.RequestException as error:

        return None, str(error)


def tiktok_user_info(access_token):

    try:

        response = requests.get(

            TIKTOK_USER_INFO_URL,

            params={
                "fields":
                    "open_id,union_id,avatar_url,"
                    "display_name,username"
            },

            headers={
                "Authorization":
                    f"Bearer {access_token}"
            },

            timeout=20,
        )

        if response.status_code != 200:

            return (
                None,
                request_error(response)
            )

        return response.json(), None

    except requests.RequestException as error:

        return None, str(error)


# ============================================================
# PROCESAR CALLBACK TIKTOK
# ============================================================

tiktok_code = st.query_params.get("code")
tiktok_state = st.query_params.get("state")

if tiktok_code:

    if (
        tiktok_state
        and st.session_state.tiktok_state
        and tiktok_state
        == st.session_state.tiktok_state
    ):

        with st.spinner(
            "Conectando TikTok..."
        ):

            token_data, token_error = (
                tiktok_exchange_code(
                    tiktok_code
                )
            )

        if token_error:

            st.error(
                f"TikTok OAuth: {token_error}"
            )

        else:

            access_token = token_data.get(
                "access_token"
            )

            if access_token:

                user_data, user_error = (
                    tiktok_user_info(
                        access_token
                    )
                )

                if user_error:

                    st.warning(
                        f"TikTok autenticó, "
                        f"pero no se pudo consultar "
                        f"el perfil: {user_error}"
                    )

                else:

                    st.session_state.tiktok_data = (
                        user_data
                    )

                    st.success(
                        "TikTok conectado correctamente."
                    )

        st.query_params.clear()

    else:

        st.error(
            "TikTok rechazado: estado OAuth inválido."
        )


# ============================================================
# YOUTUBE
# ============================================================

def youtube_configured():

    return bool(
        YOUTUBE_API_KEY
    )


def youtube_search(query):

    if not youtube_configured():

        return (
            None,
            "YouTube API Key no configurada."
        )

    try:

        response = requests.get(

            f"{YOUTUBE_API_URL}/search",

            params={

                "part":
                    "snippet",

                "q":
                    query,

                "maxResults":
                    10,

                "type":
                    "video",

                "key":
                    YOUTUBE_API_KEY,
            },

            timeout=20,
        )

        if response.status_code != 200:

            return (
                None,
                request_error(response)
            )

        return response.json(), None

    except requests.RequestException as error:

        return None, str(error)


# ============================================================
# INSTAGRAM
# ============================================================

def instagram_configured():

    return configured(
        INSTAGRAM_ACCESS_TOKEN,
        INSTAGRAM_BUSINESS_ACCOUNT_ID
    )


def instagram_info():

    if not instagram_configured():

        return (
            None,
            "Instagram no configurado."
        )

    try:

        response = requests.get(

            f"{INSTAGRAM_API_URL}/"
            f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}",

            params={

                "fields":
                    "id,username,name,"
                    "profile_picture_url,"
                    "followers_count,"
                    "follows_count,"
                    "media_count",

                "access_token":
                    INSTAGRAM_ACCESS_TOKEN,
            },

            timeout=20,
        )

        if response.status_code != 200:

            return (
                None,
                request_error(response)
            )

        return response.json(), None

    except requests.RequestException as error:

        return None, str(error)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🎛️ CONTROL HOUSE"
    )

    st.markdown(
        "### API STATUS"
    )

    # SPOTIFY

    if spotify_configured():

        if spotify_get_token():

            st.markdown(
                '<span class="api-on">'
                '● SPOTIFY ONLINE'
                '</span>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                '<span class="api-off">'
                '● SPOTIFY ERROR'
                '</span>',
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            '<span class="api-off">'
            '● SPOTIFY SIN SECRETS'
            '</span>',
            unsafe_allow_html=True
        )

    # TIKTOK

    if tiktok_configured():

        st.markdown(
            '<span class="api-ready">'
            '● TIKTOK OAUTH READY'
            '</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="api-off">'
            '● TIKTOK SIN SECRETS'
            '</span>',
            unsafe_allow_html=True
        )

    # YOUTUBE

    if youtube_configured():

        st.markdown(
            '<span class="api-on">'
            '● YOUTUBE ONLINE'
            '</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="api-ready">'
            '● YOUTUBE HUB'
            '</span>',
            unsafe_allow_html=True
        )

    # INSTAGRAM

    if instagram_configured():

        st.markdown(
            '<span class="api-on">'
            '● INSTAGRAM ONLINE'
            '</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="api-ready">'
            '● INSTAGRAM HUB'
            '</span>',
            unsafe_allow_html=True
        )

    st.divider()

    st.write("🟢 HOUSE ONLINE")
    st.write("∞ RABINO RAP")
    st.write("☁️ CLOUD")
    st.write("🔐 SECRET CONTROL")
    st.write("⚡ API ENGINE V10")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="house-title">'
    'STREAMING HOUSE'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="infinity">∞</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="house-subtitle">'
    'RABINO RAP • MUSIC • DISTRIBUTION • '
    'STREAMING • CONTROL'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# PLATAFORMAS
# ============================================================

st.markdown(
    '<div class="section">'
    '🌐 PLATAFORMAS'
    '</div>',
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

with p1:

    st.markdown("""
    <div class="platform">
        <h2>🟢 Spotify</h2>
        <p>REAL API</p>
        <small>
        Catálogo, artistas,
        tracks y álbumes.
        </small>
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
        <h2>🎤 Spotify Artists</h2>
        <p>ARTIST HUB</p>
        <small>
        Herramientas oficiales
        para artistas.
        </small>
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
        <p>DISTRIBUTION HUB</p>
        <small>
        Distribución musical.
        </small>
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
        <p>OAUTH HUB</p>
        <small>
        Conexión OAuth 2.0.
        </small>
    </div>
    """, unsafe_allow_html=True)

    if tiktok_configured():

        auth_url = tiktok_authorization_url()

        if auth_url:

            st.link_button(
                "CONECTAR TIKTOK",
                auth_url,
                use_container_width=True
            )

    st.link_button(
        "ABRIR TIKTOK",
        URL_TIKTOK,
        use_container_width=True
    )


q1, q2, q3 = st.columns(3)

with q1:

    st.markdown("""
    <div class="platform">
        <h2>▶️ YouTube</h2>
        <p>DATA API</p>
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
        <p>GRAPH API</p>
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
        <h2>⚙️ DEVELOPERS</h2>
        <p>API CONTROL</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "SPOTIFY DEVELOPERS",
        URL_SPOTIFY_DEV,
        use_container_width=True
    )


# ============================================================
# HOUSE STATUS
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '📊 HOUSE STATUS'
    '</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown("""
    <div class="metric">
        <div class="metric-number">∞</div>
        <div class="metric-label">
        HOUSE
        </div>
    </div>
    """, unsafe_allow_html=True)


with m2:

    spotify_online = bool(
        spotify_get_token()
    )

    status = (
        "ONLINE"
        if spotify_online
        else "OFFLINE"
    )

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">
            {status}
            </div>
            <div class="metric-label">
            SPOTIFY
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m3:

    status = (
        "ONLINE"
        if youtube_configured()
        else "HUB"
    )

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">
            {status}
            </div>
            <div class="metric-label">
            YOUTUBE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m4:

    status = (
        "ONLINE"
        if instagram_configured()
        else "HUB"
    )

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">
            {status}
            </div>
            <div class="metric-label">
            INSTAGRAM
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TIKTOK STATUS
# ============================================================

if st.session_state.tiktok_data:

    st.divider()

    st.markdown(
        '<div class="section">'
        '🎵 TIKTOK CONECTADO'
        '</div>',
        unsafe_allow_html=True
    )

    tiktok_data = (
        st.session_state.tiktok_data
    )

    st.json(tiktok_data)


# ============================================================
# SPOTIFY ENGINE
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '🔎 SPOTIFY API ENGINE'
    '</div>',
    unsafe_allow_html=True
)

if not spotify_configured():

    st.warning(
        "Faltan SPOTIFY_CLIENT_ID y "
        "SPOTIFY_CLIENT_SECRET en Streamlit Secrets."
    )


c1, c2 = st.columns([4, 1])

with c1:

    query = st.text_input(
        "Buscar en Spotify",
        value=st.session_state.last_query
    )


with c2:

    search_type = st.selectbox(
        "Tipo",
        [
            "artist",
            "track",
            "album",
            "playlist"
        ]
    )


if st.button(
    "🔍 BUSCAR",
    type="primary",
    use_container_width=True
):

    if not query.strip():

        st.warning(
            "Escribe algo para buscar."
        )

    else:

        with st.spinner(
            "Consultando Spotify..."
        ):

            data, error = spotify_search(
                query.strip(),
                search_type
            )

        if error:

            st.error(error)

        else:

            st.session_state.search_results = data

            st.session_state.last_query = (
                query.strip()
            )

            st.session_state.last_type = (
                search_type
            )

            st.success(
                "Spotify respondió correctamente."
            )


# ============================================================
# RESULTADOS SPOTIFY
# ============================================================

if st.session_state.search_results:

    results = (
        st.session_state.search_results
    )

    st.markdown(
        '<div class="section">'
        '🎧 RESULTADOS'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ARTISTAS
    # --------------------------------------------------------

    artists = (
        results.get(
            "artists",
            {}
        ).get(
            "items",
            []
        )
    )

    for artist in artists:

        artist_id = artist.get("id")

        images = artist.get(
            "images",
            []
        )

        image = (
            images[0].get("url")
            if images
            else None
        )

        url = (
            artist.get(
                "external_urls",
                {}
            ).get(
                "spotify"
            )
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

                    <h3>
                    🎤 {safe(artist.get("name"))}
                    </h3>

                    <p>
                    👥 Seguidores:
                    {fmt(
                        artist.get(
                            "followers",
                            {}
                        ).get(
                            "total",
                            0
                        )
                    )}
                    </p>

                    <p>
                    🔥 Popularidad:
                    {artist.get("popularity", 0)}/100
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with a3:

            if url:

                st.link_button(
                    "SPOTIFY",
                    url,
                    use_container_width=True
                )

            if artist_id:

                if st.button(
                    "DETALLES",
                    key=f"artist_{artist_id}",
                    use_container_width=True
                ):

                    data, error = (
                        spotify_artist(
                            artist_id
                        )
                    )

                    if error:

                        st.error(error)

                    else:

                        st.session_state.selected_artist = data

                        albums, album_error = (
                            spotify_artist_albums(
                                artist_id
                            )
                        )

                        if not album_error:

                            st.session_state.selected_album = albums


    # --------------------------------------------------------
    # TRACKS
    # --------------------------------------------------------

    tracks = (
        results.get(
            "tracks",
            {}
        ).get(
            "items",
            []
        )
    )

    for track in tracks:

        album = track.get(
            "album",
            {}
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

        artists_text = ", ".join(
            a.get("name", "")
            for a in track.get(
                "artists",
                []
            )
        )

        url = (
            track.get(
                "external_urls",
                {}
            ).get(
                "spotify"
            )
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

                    <h3>
                    🎵 {safe(track.get("name"))}
                    </h3>

                    <p>
                    {safe(artists_text)}
                    </p>

                    <p>
                    💿 {safe(album.get("name"))}
                    </p>

                    <p>
                    🔥 Popularidad:
                    {track.get("popularity", 0)}/100
                    </p>

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

    albums = (
        results.get(
            "albums",
            {}
        ).get(
            "items",
            []
        )
    )

    for album in albums:

        images = album.get(
            "images",
            []
        )

        image = (
            images[0].get("url")
            if images
            else None
        )

        url = (
            album.get(
                "external_urls",
                {}
            ).get(
                "spotify"
            )
        )

        a1, a2 = st.columns(
            [1, 5]
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

                    <h3>
                    💿 {safe(album.get("name"))}
                    </h3>

                    <p>
                    Lanzamiento:
                    {safe(
                        album.get(
                            "release_date",
                            "N/D"
                        )
                    )}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            if url:

                st.link_button(
                    "VER EN SPOTIFY",
                    url
                )


# ============================================================
# ARTISTA SELECCIONADO
# ============================================================

if st.session_state.selected_artist:

    artist = (
        st.session_state.selected_artist
    )

    st.divider()

    st.markdown(
        '<div class="section">'
        '🎤 ARTISTA SELECCIONADO'
        '</div>',
        unsafe_allow_html=True
    )

    images = artist.get(
        "images",
        []
    )

    left, right = st.columns(
        [1, 3]
    )

    with left:

        if images:

            st.image(
                images[0].get("url"),
                width=220
            )


    with right:

        st.markdown(
            f"""
            <div class="card">

                <h1>
                {safe(artist.get("name"))}
                </h1>

                <p>
                👥 Seguidores:
                {fmt(
                    artist.get(
                        "followers",
                        {}
                    ).get(
                        "total",
                        0
                    )
                )}
                </p>

                <p>
                🔥 Popularidad:
                {artist.get("popularity", 0)}/100
                </p>

                <p>
                🎼 Géneros:
                {safe(
                    ", ".join(
                        artist.get(
                            "genres",
                            []
                        )
                    )
                )}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        url = (
            artist.get(
                "external_urls",
                {}
            ).get(
                "spotify"
            )
        )

        if url:

            st.link_button(
                "🎧 ABRIR ARTISTA",
                url
            )


# ============================================================
# ARTIST RELEASES
# ============================================================

if st.session_state.selected_album:

    st.markdown(
        "### 💿 LANZAMIENTOS"
    )

    albums = (
        st.session_state.selected_album.get(
            "items",
            []
        )
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
                f"**{safe(album.get('name'))}**"
            )

            st.caption(
                safe(
                    album.get(
                        "release_date",
                        ""
                    )
                )
            )

            url = (
                album.get(
                    "external_urls",
                    {}
                ).get(
                    "spotify"
                )
            )

            if url:

                st.link_button(
                    "ABRIR",
                    url,
                    use_container_width=True
                )


# ============================================================
# YOUTUBE CONTROL
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '▶️ YOUTUBE CONTROL'
    '</div>',
    unsafe_allow_html=True
)

if youtube_configured():

    yt_query = st.text_input(
        "Buscar en YouTube",
        value="Rabino Rap"
    )

    if st.button(
        "🔎 BUSCAR YOUTUBE",
        use_container_width=True
    ):

        data, error = youtube_search(
            yt_query
        )

        if error:

            st.error(error)

        else:

            st.session_state.youtube_results = data


    if st.session_state.youtube_results:

        for item in (
            st.session_state
            .youtube_results
            .get(
                "items",
                []
            )
        ):

            snippet = item.get(
                "snippet",
                {}
            )

            title = snippet.get(
                "title",
                "Video"
            )

            video_id = (
                item.get(
                    "id",
                    {}
                ).get(
                    "videoId"
                )
            )

            st.markdown(
                f"### ▶️ {safe(title)}"
            )

            if video_id:

                st.video(
                    f"https://www.youtube.com/watch?v={video_id}"
                )

else:

    st.info(
        "YouTube está preparado. "
        "Agrega YOUTUBE_API_KEY en Secrets."
    )


# ============================================================
# INSTAGRAM CONTROL
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '📸 INSTAGRAM CONTROL'
    '</div>',
    unsafe_allow_html=True
)

if instagram_configured():

    if st.button(
        "📊 CONSULTAR INSTAGRAM",
        use_container_width=True
    ):

        data, error = instagram_info()

        if error:

            st.error(error)

        else:

            st.session_state.instagram_data = data


    if st.session_state.instagram_data:

        data = (
            st.session_state.instagram_data
        )

        i1, i2, i3 = st.columns(3)

        with i1:

            st.metric(
                "Seguidores",
                fmt(
                    data.get(
                        "followers_count",
                        0
                    )
                )
            )

        with i2:

            st.metric(
                "Siguiendo",
                fmt(
                    data.get(
                        "follows_count",
                        0
                    )
                )
            )

        with i3:

            st.metric(
                "Publicaciones",
                fmt(
                    data.get(
                        "media_count",
                        0
                    )
                )
            )

        st.json(data)

else:

    st.info(
        "Instagram está preparado para Graph API. "
        "Agrega INSTAGRAM_ACCESS_TOKEN y "
        "INSTAGRAM_BUSINESS_ACCOUNT_ID en Secrets."
    )


# ============================================================
# DISTRIBUTION HUB
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '📦 DISTRIBUTION CONTROL'
    '</div>',
    unsafe_allow_html=True
)

d1, d2, d3 = st.columns(3)

with d1:

    st.markdown("""
    <div class="card">
        <h3>📦 DistroKid</h3>
        <p>Distribution Hub</p>
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
        <p>Artist Hub</p>
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
        <h3>∞ STREAMING HOUSE</h3>
        <p>Central Control</p>
    </div>
    """, unsafe_allow_html=True)

    st.success(
        "HOUSE ONLINE"
    )


# ============================================================
# SECRET CHECK
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '🔐 SECRET CONTROL'
    '</div>',
    unsafe_allow_html=True
)

secret_items = [

    (
        "Spotify Client ID",
        bool(SPOTIFY_CLIENT_ID)
    ),

    (
        "Spotify Client Secret",
        bool(SPOTIFY_CLIENT_SECRET)
    ),

    (
        "Spotify Redirect URI",
        bool(SPOTIFY_REDIRECT_URI)
    ),

    (
        "TikTok Client Key",
        bool(TIKTOK_CLIENT_KEY)
    ),

    (
        "TikTok Client Secret",
        bool(TIKTOK_CLIENT_SECRET)
    ),

    (
        "TikTok Redirect URI",
        bool(TIKTOK_REDIRECT_URI)
    ),

    (
        "YouTube API Key",
        bool(YOUTUBE_API_KEY)
    ),

    (
        "Instagram Access Token",
        bool(INSTAGRAM_ACCESS_TOKEN)
    ),

    (
        "Instagram Business Account ID",
        bool(INSTAGRAM_BUSINESS_ACCOUNT_ID)
    ),

    (
        "Meta App ID",
        bool(META_APP_ID)
    ),

    (
        "Meta App Secret",
        bool(META_APP_SECRET)
    ),
]

for label, active in secret_items:

    if active:

        st.markdown(
            f'<span class="api-on">'
            f'● {safe(label)}'
            f' — CONFIGURADO'
            f'</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f'<span class="api-off">'
            f'● {safe(label)}'
            f' — FALTA'
            f'</span>',
            unsafe_allow_html=True
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

STREAMING HOUSE ∞<br>
RABINO RAP<br><br>

MUSIC • DISTRIBUTION • STREAMING • CONTROL<br>
SECRET CONTROL • API ENGINE V10

</div>
""", unsafe_allow_html=True)
