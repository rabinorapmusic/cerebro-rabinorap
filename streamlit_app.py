# ============================================================
# STREAMING HOUSE ∞
# RABINO RAP
# V8 — ULTIMATE API HOUSE
#
# SPOTIFY
#   - Client Credentials
#   - User OAuth
#   - Profile
#   - Top Artists
#   - Top Tracks
#   - Search
#   - Artist
#   - Albums
#   - Tracks
#   - Playlists
#
# TIKTOK
#   - OAuth 2.0
#   - PKCE
#   - State protection
#   - Token exchange
#   - Token refresh
#   - User profile
#   - Video list
#
# YOUTUBE
#   - OAuth ready
#   - Data API ready
#   - Channel lookup
#   - Search
#
# INSTAGRAM
#   - Graph API ready
#   - Professional account lookup
#
# DISTROKID
#   - HUB
#
# SECURITY
#   - No credentials hardcoded
#   - Streamlit Secrets
#   - OAuth state
#   - PKCE
#
# NO VOLUMENES
# NO CREDENCIALES HARDCODEADAS
# ============================================================

import streamlit as st
import requests
import base64
import hashlib
import secrets
import time
from urllib.parse import urlencode
from html import escape


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="STREAMING HOUSE ∞",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 0%, #1b1b1b 0%, #090909 35%, #000000 80%);
    color: white;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

.house-title {
    text-align:center;
    font-size:clamp(38px,6vw,78px);
    font-weight:950;
    letter-spacing:8px;
    line-height:1;
}

.house-subtitle {
    text-align:center;
    color:#777;
    letter-spacing:3px;
    margin-top:12px;
    margin-bottom:30px;
}

.infinity {
    text-align:center;
    font-size:95px;
    font-weight:950;
    line-height:.9;
    margin:10px;
}

.section {
    font-size:25px;
    font-weight:950;
    letter-spacing:2px;
    margin-top:25px;
    margin-bottom:15px;
}

.platform,
.card,
.result,
.metric {
    background:linear-gradient(145deg,#151515,#080808);
    border:1px solid #292929;
    border-radius:18px;
    padding:20px;
    box-shadow:0 12px 40px rgba(0,0,0,.28);
}

.platform {
    min-height:170px;
    margin-bottom:10px;
}

.result {
    margin-bottom:12px;
}

.metric {
    text-align:center;
    min-height:100px;
}

.metric-number {
    font-size:28px;
    font-weight:950;
}

.metric-label {
    color:#777;
    font-size:11px;
    letter-spacing:1.5px;
    text-transform:uppercase;
}

.api-on {
    display:inline-block;
    background:#10351c;
    color:#63ef87;
    padding:7px 12px;
    border-radius:20px;
    font-weight:900;
    font-size:11px;
}

.api-off {
    display:inline-block;
    background:#351313;
    color:#ff7777;
    padding:7px 12px;
    border-radius:20px;
    font-weight:900;
    font-size:11px;
}

.api-ready {
    display:inline-block;
    background:#332b10;
    color:#ffd95a;
    padding:7px 12px;
    border-radius:20px;
    font-weight:900;
    font-size:11px;
}

.small-muted {
    color:#777;
    font-size:12px;
}

.footer {
    text-align:center;
    color:#444;
    padding:50px 10px 10px;
    letter-spacing:2px;
}

.stButton > button,
.stLinkButton > a {
    border-radius:12px !important;
    font-weight:800 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {

    # Spotify
    "spotify_app_token": None,
    "spotify_app_expiry": 0,
    "spotify_user_token": None,
    "spotify_user_refresh": None,
    "spotify_user_expiry": 0,
    "spotify_state": None,
    "spotify_pkce": None,

    # TikTok
    "tiktok_access_token": None,
    "tiktok_refresh_token": None,
    "tiktok_expiry": 0,
    "tiktok_state": None,
    "tiktok_pkce": None,
    "tiktok_user": None,
    "tiktok_videos": None,

    # YouTube
    "youtube_access_token": None,
    "youtube_refresh_token": None,
    "youtube_expiry": 0,
    "youtube_state": None,

    # Instagram
    "instagram_data": None,

    # Search
    "search_results": None,
    "last_query": "Rabino Rap",
    "last_type": "artist",

    # Artist
    "artist_data": None,
    "artist_albums": None,

    # Messages
    "last_error": None,
    "last_success": None,
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SECRETS
# ============================================================

def secret(name, default=""):

    try:

        value = st.secrets.get(name)

        if value:
            return str(value)

    except Exception:
        pass

    return default


# ============================================================
# CONFIG
# ============================================================

SPOTIFY_CLIENT_ID = secret("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = secret("SPOTIFY_CLIENT_SECRET")

TIKTOK_CLIENT_KEY = secret("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = secret("TIKTOK_CLIENT_SECRET")

YOUTUBE_CLIENT_ID = secret("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = secret("YOUTUBE_CLIENT_SECRET")

INSTAGRAM_ACCESS_TOKEN = secret("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = secret(
    "INSTAGRAM_BUSINESS_ACCOUNT_ID"
)

APP_BASE_URL = secret(
    "APP_BASE_URL",
    "http://localhost:8501"
).rstrip("/")


# ============================================================
# OFFICIAL URLS
# ============================================================

SPOTIFY_WEB = "https://open.spotify.com/"
SPOTIFY_ARTISTS = "https://artists.spotify.com/"
SPOTIFY_DEV = "https://developer.spotify.com/"

DISTROKID = "https://distrokid.com/"

TIKTOK_WEB = "https://www.tiktok.com/"
TIKTOK_DEV = "https://developers.tiktok.com/"

YOUTUBE_WEB = "https://www.youtube.com/"
YOUTUBE_DEV = "https://console.cloud.google.com/"

INSTAGRAM_WEB = "https://www.instagram.com/"
INSTAGRAM_DEV = "https://developers.facebook.com/"


# ============================================================
# CONSTANTS
# ============================================================

SPOTIFY_API = "https://api.spotify.com/v1"
SPOTIFY_ACCOUNTS = "https://accounts.spotify.com"

TIKTOK_AUTH = "https://www.tiktok.com/v2/auth/authorize/"
TIKTOK_TOKEN = "https://open.tiktokapis.com/v2/oauth/token/"
TIKTOK_API = "https://open.tiktokapis.com/v2"

YOUTUBE_API = "https://www.googleapis.com/youtube/v3"
YOUTUBE_AUTH = "https://accounts.google.com/o/oauth2/v2/auth"
YOUTUBE_TOKEN = "https://oauth2.googleapis.com/token"

INSTAGRAM_API = "https://graph.facebook.com/v23.0"


# ============================================================
# HELPERS
# ============================================================

def safe(value):

    if value is None:
        return ""

    return escape(str(value))


def number(value):

    try:
        return f"{int(value):,}"

    except Exception:
        return "0"


def configured(*values):

    return all(bool(v) for v in values)


def now():

    return time.time()


def random_state():

    return secrets.token_urlsafe(32)


def pkce_pair():

    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(
            verifier.encode("utf-8")
        ).digest()
    ).decode("utf-8").rstrip("=")

    return verifier, challenge


def api_error(response):

    try:

        data = response.json()

        if isinstance(data, dict):

            error = data.get("error")

            if isinstance(error, dict):

                return (
                    error.get("message")
                    or error.get("error_description")
                    or str(error)
                )

            return (
                data.get("message")
                or data.get("error_description")
                or str(data)
            )

    except Exception:
        pass

    return f"HTTP {response.status_code}"


# ============================================================
# SPOTIFY — APP TOKEN
# ============================================================

def spotify_app_token():

    if not configured(
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET
    ):
        return None

    if (
        st.session_state.spotify_app_token
        and now()
        < st.session_state.spotify_app_expiry
    ):

        return st.session_state.spotify_app_token

    credentials = (
        f"{SPOTIFY_CLIENT_ID}:"
        f"{SPOTIFY_CLIENT_SECRET}"
    )

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type":
            "application/x-www-form-urlencoded"
    }

    try:

        response = requests.post(
            f"{SPOTIFY_ACCOUNTS}/api/token",
            headers=headers,
            data={
                "grant_type":
                    "client_credentials"
            },
            timeout=20
        )

        if response.status_code != 200:

            return None

        data = response.json()

        token = data.get("access_token")

        expires = int(
            data.get("expires_in", 3600)
        )

        if token:

            st.session_state.spotify_app_token = token

            st.session_state.spotify_app_expiry = (
                now() + expires - 60
            )

        return token

    except requests.RequestException:

        return None


# ============================================================
# SPOTIFY — USER TOKEN
# ============================================================

def spotify_user_token():

    token = st.session_state.spotify_user_token

    if (
        token
        and now()
        < st.session_state.spotify_user_expiry
    ):

        return token

    refresh = st.session_state.spotify_user_refresh

    if not refresh:

        return None

    try:

        credentials = (
            f"{SPOTIFY_CLIENT_ID}:"
            f"{SPOTIFY_CLIENT_SECRET}"
        )

        encoded = base64.b64encode(
            credentials.encode()
        ).decode()

        response = requests.post(

            f"{SPOTIFY_ACCOUNTS}/api/token",

            headers={
                "Authorization":
                    f"Basic {encoded}",
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },

            data={
                "grant_type":
                    "refresh_token",
                "refresh_token":
                    refresh
            },

            timeout=20
        )

        if response.status_code != 200:

            return None

        data = response.json()

        token = data.get("access_token")

        expires = int(
            data.get("expires_in", 3600)
        )

        if token:

            st.session_state.spotify_user_token = token

            st.session_state.spotify_user_expiry = (
                now() + expires - 60
            )

            if data.get("refresh_token"):

                st.session_state.spotify_user_refresh = (
                    data["refresh_token"]
                )

        return token

    except requests.RequestException:

        return None


# ============================================================
# SPOTIFY — USER OAUTH
# ============================================================

SPOTIFY_SCOPES = " ".join([
    "user-read-private",
    "user-read-email",
    "user-top-read",
    "playlist-read-private",
    "playlist-read-collaborative"
])


def spotify_authorize_url():

    if not configured(
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET
    ):

        return None

    state = random_state()
    verifier, challenge = pkce_pair()

    st.session_state.spotify_state = state
    st.session_state.spotify_pkce = verifier

    params = {

        "client_id":
            SPOTIFY_CLIENT_ID,

        "response_type":
            "code",

        "redirect_uri":
            APP_BASE_URL,

        "state":
            state,

        "scope":
            SPOTIFY_SCOPES,

        "code_challenge_method":
            "S256",

        "code_challenge":
            challenge
    }

    return (
        f"{SPOTIFY_ACCOUNTS}/authorize?"
        f"{urlencode(params)}"
    )


def spotify_exchange_code(code):

    verifier = st.session_state.spotify_pkce

    if not verifier:

        return False, "PKCE no encontrado."

    try:

        response = requests.post(

            f"{SPOTIFY_ACCOUNTS}/api/token",

            data={

                "client_id":
                    SPOTIFY_CLIENT_ID,

                "grant_type":
                    "authorization_code",

                "code":
                    code,

                "redirect_uri":
                    APP_BASE_URL,

                "code_verifier":
                    verifier
            },

            timeout=20
        )

        if response.status_code != 200:

            return False, api_error(response)

        data = response.json()

        st.session_state.spotify_user_token = (
            data.get("access_token")
        )

        st.session_state.spotify_user_refresh = (
            data.get("refresh_token")
        )

        st.session_state.spotify_user_expiry = (
            now()
            + int(data.get("expires_in", 3600))
            - 60
        )

        st.session_state.spotify_state = None
        st.session_state.spotify_pkce = None

        return True, None

    except requests.RequestException as e:

        return False, str(e)


# ============================================================
# SPOTIFY REQUEST
# ============================================================

def spotify_request(
    endpoint,
    params=None,
    user=False
):

    token = (
        spotify_user_token()
        if user
        else spotify_app_token()
    )

    if not token:

        return None, (
            "Spotify no está autenticado "
            "para esta operación."
        )

    try:

        response = requests.get(

            f"{SPOTIFY_API}{endpoint}",

            headers={
                "Authorization":
                    f"Bearer {token}"
            },

            params=params,

            timeout=20
        )

        if response.status_code == 401 and not user:

            st.session_state.spotify_app_token = None
            st.session_state.spotify_app_expiry = 0

            token = spotify_app_token()

            if not token:

                return None, "Token Spotify inválido."

            response = requests.get(

                f"{SPOTIFY_API}{endpoint}",

                headers={
                    "Authorization":
                        f"Bearer {token}"
                },

                params=params,

                timeout=20
            )

        if response.status_code == 429:

            retry = response.headers.get(
                "Retry-After",
                "unos segundos"
            )

            return None, (
                f"Spotify está limitando solicitudes. "
                f"Espera {retry}."
            )

        if response.status_code != 200:

            return None, api_error(response)

        return response.json(), None

    except requests.RequestException as e:

        return None, str(e)


# ============================================================
# SPOTIFY FUNCTIONS
# ============================================================

def spotify_search(query, kind):

    return spotify_request(
        "/search",
        {
            "q": query,
            "type": kind,
            "limit": 10,
            "market": "DO"
        }
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
            "limit": 10,
            "market": "DO"
        }
    )


def spotify_track(track_id):

    return spotify_request(
        f"/tracks/{track_id}"
    )


def spotify_album(album_id):

    return spotify_request(
        f"/albums/{album_id}"
    )


def spotify_profile():

    return spotify_request(
        "/me",
        user=True
    )


def spotify_top_artists():

    return spotify_request(
        "/me/top/artists",
        {
            "limit": 20,
            "time_range": "medium_term"
        },
        user=True
    )


def spotify_top_tracks():

    return spotify_request(
        "/me/top/tracks",
        {
            "limit": 20,
            "time_range": "medium_term"
        },
        user=True
    )


# ============================================================
# TIKTOK — OAUTH
# ============================================================

TIKTOK_SCOPES = "user.info.basic,video.list"


def tiktok_authorize_url():

    if not configured(
        TIKTOK_CLIENT_KEY,
        TIKTOK_CLIENT_SECRET
    ):

        return None

    state = random_state()

    verifier, challenge = pkce_pair()

    st.session_state.tiktok_state = state
    st.session_state.tiktok_pkce = verifier

    params = {

        "client_key":
            TIKTOK_CLIENT_KEY,

        "response_type":
            "code",

        "scope":
            TIKTOK_SCOPES,

        "redirect_uri":
            APP_BASE_URL,

        "state":
            state,

        "code_challenge":
            challenge,

        "code_challenge_method":
            "S256"
    }

    return (
        f"{TIKTOK_AUTH}?"
        f"{urlencode(params)}"
    )


def tiktok_exchange_code(code):

    verifier = st.session_state.tiktok_pkce

    if not verifier:

        return False, "TikTok PKCE no encontrado."

    try:

        response = requests.post(

            TIKTOK_TOKEN,

            headers={
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },

            data={

                "client_key":
                    TIKTOK_CLIENT_KEY,

                "client_secret":
                    TIKTOK_CLIENT_SECRET,

                "code":
                    code,

                "grant_type":
                    "authorization_code",

                "redirect_uri":
                    APP_BASE_URL,

                "code_verifier":
                    verifier
            },

            timeout=20
        )

        if response.status_code != 200:

            return False, api_error(response)

        data = response.json()

        st.session_state.tiktok_access_token = (
            data.get("access_token")
        )

        st.session_state.tiktok_refresh_token = (
            data.get("refresh_token")
        )

        st.session_state.tiktok_expiry = (
            now()
            + int(data.get("expires_in", 86400))
            - 300
        )

        st.session_state.tiktok_state = None
        st.session_state.tiktok_pkce = None

        return True, None

    except requests.RequestException as e:

        return False, str(e)


def tiktok_refresh():

    refresh = st.session_state.tiktok_refresh_token

    if not refresh:

        return None

    try:

        response = requests.post(

            TIKTOK_TOKEN,

            headers={
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },

            data={

                "client_key":
                    TIKTOK_CLIENT_KEY,

                "client_secret":
                    TIKTOK_CLIENT_SECRET,

                "grant_type":
                    "refresh_token",

                "refresh_token":
                    refresh
            },

            timeout=20
        )

        if response.status_code != 200:

            return None

        data = response.json()

        token = data.get("access_token")

        if token:

            st.session_state.tiktok_access_token = token

            st.session_state.tiktok_refresh_token = (
                data.get(
                    "refresh_token",
                    refresh
                )
            )

            st.session_state.tiktok_expiry = (
                now()
                + int(data.get("expires_in", 86400))
                - 300
            )

        return token

    except requests.RequestException:

        return None


def tiktok_token():

    token = st.session_state.tiktok_access_token

    if (
        token
        and now()
        < st.session_state.tiktok_expiry
    ):

        return token

    return tiktok_refresh()


def tiktok_request(endpoint, params=None):

    token = tiktok_token()

    if not token:

        return None, "TikTok no está conectado."

    try:

        response = requests.get(

            f"{TIKTOK_API}{endpoint}",

            headers={
                "Authorization":
                    f"Bearer {token}"
            },

            params=params,

            timeout=20
        )

        if response.status_code != 200:

            return None, api_error(response)

        return response.json(), None

    except requests.RequestException as e:

        return None, str(e)


def tiktok_user():

    return tiktok_request(
        "/user/info/",
        {
            "fields":
                "open_id,union_id,"
                "avatar_url,display_name"
        }
    )


def tiktok_videos():

    return tiktok_request(
        "/video/list/",
        {
            "fields":
                "id,title,create_time,"
                "cover_image_url"
        }
    )


# ============================================================
# YOUTUBE — OAUTH
# ============================================================

YOUTUBE_SCOPES = (
    "https://www.googleapis.com/auth/youtube.readonly"
)


def youtube_configured():

    return configured(
        YOUTUBE_CLIENT_ID,
        YOUTUBE_CLIENT_SECRET
    )


def youtube_authorize_url():

    if not youtube_configured():

        return None

    state = random_state()

    st.session_state.youtube_state = state

    params = {

        "client_id":
            YOUTUBE_CLIENT_ID,

        "redirect_uri":
            APP_BASE_URL,

        "response_type":
            "code",

        "scope":
            YOUTUBE_SCOPES,

        "access_type":
            "offline",

        "prompt":
            "consent",

        "state":
            state
    }

    return (
        f"{YOUTUBE_AUTH}?"
        f"{urlencode(params)}"
    )


def youtube_exchange_code(code):

    try:

        response = requests.post(

            YOUTUBE_TOKEN,

            data={

                "code":
                    code,

                "client_id":
                    YOUTUBE_CLIENT_ID,

                "client_secret":
                    YOUTUBE_CLIENT_SECRET,

                "redirect_uri":
                    APP_BASE_URL,

                "grant_type":
                    "authorization_code"
            },

            timeout=20
        )

        if response.status_code != 200:

            return False, api_error(response)

        data = response.json()

        st.session_state.youtube_access_token = (
            data.get("access_token")
        )

        st.session_state.youtube_refresh_token = (
            data.get("refresh_token")
        )

        st.session_state.youtube_expiry = (
            now()
            + int(data.get("expires_in", 3600))
            - 60
        )

        return True, None

    except requests.RequestException as e:

        return False, str(e)


def youtube_token():

    token = st.session_state.youtube_access_token

    if (
        token
        and now()
        < st.session_state.youtube_expiry
    ):

        return token

    refresh = st.session_state.youtube_refresh_token

    if not refresh:

        return None

    try:

        response = requests.post(

            YOUTUBE_TOKEN,

            data={

                "client_id":
                    YOUTUBE_CLIENT_ID,

                "client_secret":
                    YOUTUBE_CLIENT_SECRET,

                "refresh_token":
                    refresh,

                "grant_type":
                    "refresh_token"
            },

            timeout=20
        )

        if response.status_code != 200:

            return None

        data = response.json()

        token = data.get("access_token")

        if token:

            st.session_state.youtube_access_token = token

            st.session_state.youtube_expiry = (
                now()
                + int(data.get("expires_in", 3600))
                - 60
            )

        return token

    except requests.RequestException:

        return None


def youtube_request(endpoint, params=None):

    token = youtube_token()

    if not token:

        return None, "YouTube no está conectado."

    try:

        response = requests.get(

            f"{YOUTUBE_API}{endpoint}",

            headers={
                "Authorization":
                    f"Bearer {token}"
            },

            params=params,

            timeout=20
        )

        if response.status_code != 200:

            return None, api_error(response)

        return response.json(), None

    except requests.RequestException as e:

        return None, str(e)


def youtube_channel():

    return youtube_request(
        "",
        {
            "part": "snippet,statistics",
            "mine": "true"
        }
    )


def youtube_search(query):

    return youtube_request(
        "/search",
        {
            "part": "snippet",
            "q": query,
            "maxResults": 10,
            "type": "video"
        }
    )


# ============================================================
# INSTAGRAM GRAPH API
# ============================================================

def instagram_configured():

    return configured(
        INSTAGRAM_ACCESS_TOKEN,
        INSTAGRAM_BUSINESS_ACCOUNT_ID
    )


def instagram_request(fields):

    if not instagram_configured():

        return None, "Instagram no configurado."

    try:

        response = requests.get(

            f"{INSTAGRAM_API}/"
            f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}",

            params={
                "fields": fields,
                "access_token":
                    INSTAGRAM_ACCESS_TOKEN
            },

            timeout=20
        )

        if response.status_code != 200:

            return None, api_error(response)

        return response.json(), None

    except requests.RequestException as e:

        return None, str(e)


# ============================================================
# PROCESS OAUTH CALLBACK
# ============================================================

query_params = st.query_params

oauth_code = query_params.get("code")
oauth_state = query_params.get("state")
oauth_error = query_params.get("error")


if oauth_error:

    st.error(
        f"OAuth error: {safe(oauth_error)}"
    )


if oauth_code and oauth_state:

    # Spotify
    if (
        st.session_state.spotify_state
        and oauth_state
        == st.session_state.spotify_state
    ):

        ok, error = spotify_exchange_code(
            oauth_code
        )

        if ok:

            st.success(
                "Spotify conectado correctamente."
            )

        else:

            st.error(
                f"Spotify OAuth: {safe(error)}"
            )

    # TikTok
    elif (
        st.session_state.tiktok_state
        and oauth_state
        == st.session_state.tiktok_state
    ):

        ok, error = tiktok_exchange_code(
            oauth_code
        )

        if ok:

            st.success(
                "TikTok conectado correctamente."
            )

        else:

            st.error(
                f"TikTok OAuth: {safe(error)}"
            )

    # YouTube
    elif (
        st.session_state.youtube_state
        and oauth_state
        == st.session_state.youtube_state
    ):

        ok, error = youtube_exchange_code(
            oauth_code
        )

        if ok:

            st.success(
                "YouTube conectado correctamente."
            )

        else:

            st.error(
                f"YouTube OAuth: {safe(error)}"
            )

    else:

        st.warning(
            "OAuth recibido, pero el state "
            "no coincide."
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎛️ CONTROL HOUSE")

    st.markdown("### API STATUS")

    # Spotify
    if configured(
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET
    ):

        if spotify_app_token():

            st.markdown(
                '<span class="api-on">'
                '● SPOTIFY API ONLINE'
                '</span>',
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                '<span class="api-off">'
                '● SPOTIFY API ERROR'
                '</span>',
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            '<span class="api-off">'
            '● SPOTIFY SIN CONFIGURAR'
            '</span>',
            unsafe_allow_html=True
        )

    # TikTok
    if configured(
        TIKTOK_CLIENT_KEY,
        TIKTOK_CLIENT_SECRET
    ):

        st.markdown(
            '<span class="api-ready">'
            '● TIKTOK OAUTH READY'
            '</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="api-off">'
            '● TIKTOK SIN CONFIGURAR'
            '</span>',
            unsafe_allow_html=True
        )

    # YouTube
    if youtube_configured():

        st.markdown(
            '<span class="api-ready">'
            '● YOUTUBE API READY'
            '</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="api-off">'
            '● YOUTUBE HUB'
            '</span>',
            unsafe_allow_html=True
        )

    # Instagram
    if instagram_configured():

        st.markdown(
            '<span class="api-on">'
            '● INSTAGRAM GRAPH ONLINE'
            '</span>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<span class="api-off">'
            '● INSTAGRAM HUB'
            '</span>',
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("### SISTEMA")

    st.write("🟢 STREAMING HOUSE")
    st.write("∞ RABINO RAP")
    st.write("☁️ CLOUD READY")
    st.write("🔐 SECRETS PROTECTED")
    st.write("⚡ API ENGINE V8")


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
# PLATFORMS
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
        <p>API + OAuth</p>
        <small>
        Catálogo, artista, canciones,
        álbumes, perfil y estadísticas.
        </small>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR SPOTIFY",
        SPOTIFY_WEB,
        use_container_width=True
    )

with p2:

    st.markdown("""
    <div class="platform">
        <h2>🎤 Spotify for Artists</h2>
        <p>Artist Hub</p>
        <small>
        Gestión del perfil y herramientas
        oficiales para artistas.
        </small>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR ARTIST HUB",
        SPOTIFY_ARTISTS,
        use_container_width=True
    )

with p3:

    st.markdown("""
    <div class="platform">
        <h2>📦 DistroKid</h2>
        <p>Distribution Hub</p>
        <small>
        Distribución y administración
        de lanzamientos.
        </small>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR DISTROKID",
        DISTROKID,
        use_container_width=True
    )

with p4:

    st.markdown("""
    <div class="platform">
        <h2>🎵 TikTok</h2>
        <p>OAuth + API</p>
        <small>
        Login, perfil y vídeos
        según permisos aprobados.
        </small>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR TIKTOK",
        TIKTOK_WEB,
        use_container_width=True
    )


q1, q2, q3, q4 = st.columns(4)

with q1:

    st.markdown("""
    <div class="platform">
        <h2>▶️ YouTube</h2>
        <p>Data API</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR YOUTUBE",
        YOUTUBE_WEB,
        use_container_width=True
    )

with q2:

    st.markdown("""
    <div class="platform">
        <h2>📸 Instagram</h2>
        <p>Graph API</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR INSTAGRAM",
        INSTAGRAM_WEB,
        use_container_width=True
    )

with q3:

    st.markdown("""
    <div class="platform">
        <h2>⚙️ TikTok Dev</h2>
        <p>Developer Hub</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR DEVELOPER",
        TIKTOK_DEV,
        use_container_width=True
    )

with q4:

    st.markdown("""
    <div class="platform">
        <h2>⚙️ YouTube Dev</h2>
        <p>Google Cloud</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR API",
        YOUTUBE_DEV,
        use_container_width=True
    )


# ============================================================
# STATUS
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
        <div class="metric-label">
            HOUSE
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:

    spotify_status = (
        "ONLINE"
        if spotify_app_token()
        else "OFFLINE"
    )

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">
                {spotify_status}
            </div>
            <div class="metric-label">
                SPOTIFY
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    tik_status = (
        "CONNECTED"
        if st.session_state.tiktok_access_token
        else "READY"
        if configured(
            TIKTOK_CLIENT_KEY,
            TIKTOK_CLIENT_SECRET
        )
        else "HUB"
    )

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">
                {tik_status}
            </div>
            <div class="metric-label">
                TIKTOK
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:

    yt_status = (
        "CONNECTED"
        if st.session_state.youtube_access_token
        else "READY"
        if youtube_configured()
        else "HUB"
    )

    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-number">
                {yt_status}
            </div>
            <div class="metric-label">
                YOUTUBE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SPOTIFY USER CONTROL
# ============================================================

st.divider()

st.markdown(
    '<div class="section">🎤 SPOTIFY USER CONTROL</div>',
    unsafe_allow_html=True
)

spotify_user = spotify_user_token()

if spotify_user:

    st.success(
        "Spotify conectado como usuario."
    )

    s1, s2, s3 = st.columns(3)

    with s1:

        if st.button(
            "👤 MI PERFIL",
            use_container_width=True
        ):

            data, error = spotify_profile()

            if error:

                st.error(error)

            elif data:

                st.json(data)

    with s2:

        if st.button(
            "🔥 TOP ARTISTAS",
            use_container_width=True
        ):

            data, error = spotify_top_artists()

            if error:

                st.error(error)

            elif data:

                for artist in data.get(
                    "items",
                    []
                ):

                    st.write(
                        f"🎤 {artist.get('name')}"
                    )

    with s3:

        if st.button(
            "🎵 TOP CANCIONES",
            use_container_width=True
        ):

            data, error = spotify_top_tracks()

            if error:

                st.error(error)

            elif data:

                for track in data.get(
                    "items",
                    []
                ):

                    names = ", ".join(
                        a.get("name", "")
                        for a in track.get(
                            "artists",
                            []
                        )
                    )

                    st.write(
                        f"🎵 {track.get('name')} "
                        f"— {names}"
                    )

else:

    if configured(
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET
    ):

        auth_url = spotify_authorize_url()

        if auth_url:

            st.link_button(
                "🔐 CONECTAR SPOTIFY",
                auth_url,
                use_container_width=True
            )

    else:

        st.info(
            "Configura Spotify Client ID "
            "y Client Secret."
        )


# ============================================================
# SPOTIFY SEARCH
# ============================================================

st.divider()

st.markdown(
    '<div class="section">🔎 SPOTIFY API ENGINE</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns([4, 1])

with c1:

    query = st.text_input(
        "Buscar",
        value=st.session_state.last_query
    )

with c2:

    kind = st.selectbox(
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
                kind
            )

        if error:

            st.error(error)

        else:

            st.session_state.search_results = data
            st.session_state.last_query = query
            st.session_state.last_type = kind

            st.success(
                "Búsqueda completada."
            )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.search_results:

    results = st.session_state.search_results

    st.markdown(
        '<div class="section">🎧 RESULTADOS</div>',
        unsafe_allow_html=True
    )

    for artist in results.get(
        "artists",
        {}
    ).get(
        "items",
        []
    ):

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

        url = artist.get(
            "external_urls",
            {}
        ).get(
            "spotify"
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
                    <h3>🎤 {safe(artist.get("name"))}</h3>
                    <p>
                    Seguidores:
                    {number(
                        artist.get(
                            "followers",
                            {}
                        ).get("total", 0)
                    )}
                    </p>
                    <p>
                    Popularidad:
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

                    data, error = spotify_artist(
                        artist_id
                    )

                    if error:

                        st.error(error)

                    else:

                        st.session_state.artist_data = data

                        albums, album_error = (
                            spotify_artist_albums(
                                artist_id
                            )
                        )

                        if not album_error:

                            st.session_state.artist_albums = (
                                albums
                            )


    for track in results.get(
        "tracks",
        {}
    ).get(
        "items",
        []
    ):

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

        url = track.get(
            "external_urls",
            {}
        ).get(
            "spotify"
        )

        artists = ", ".join(
            a.get("name", "")
            for a in track.get(
                "artists",
                []
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
                    <h3>🎵 {safe(track.get("name"))}</h3>
                    <p>{safe(artists)}</p>
                    <p>
                    Álbum:
                    {safe(album.get("name"))}
                    </p>
                    <p>
                    Popularidad:
                    {track.get("popularity", 0)}/100
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with t3:

            if url:

                st.link_button(
                    "ABRIR",
                    url,
                    use_container_width=True
                )


    for album in results.get(
        "albums",
        {}
    ).get(
        "items",
        []
    ):

        images = album.get(
            "images",
            []
        )

        image = (
            images[0].get("url")
            if images
            else None
        )

        url = album.get(
            "external_urls",
            {}
        ).get(
            "spotify"
        )

        st.markdown(
            f"""
            <div class="result">
                <h3>
                💿 {safe(album.get("name"))}
                </h3>
                <p>
                Lanzamiento:
                {safe(album.get("release_date"))}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if image:

            st.image(
                image,
                width=130
            )

        if url:

            st.link_button(
                "VER ÁLBUM",
                url
            )


# ============================================================
# SELECTED ARTIST
# ============================================================

if st.session_state.artist_data:

    artist = st.session_state.artist_data

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

                <h1>
                {safe(artist.get("name"))}
                </h1>

                <p>
                👥 Seguidores:
                {number(
                    artist.get(
                        "followers",
                        {}
                    ).get("total", 0)
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

        url = artist.get(
            "external_urls",
            {}
        ).get("spotify")

        if url:

            st.link_button(
                "🎧 ABRIR ARTISTA",
                url
            )


# ============================================================
# ARTIST ALBUMS
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

    for i, album in enumerate(albums):

        with cols[i % 5]:

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

            url = album.get(
                "external_urls",
                {}
            ).get("spotify")

            if url:

                st.link_button(
                    "ABRIR",
                    url,
                    use_container_width=True
                )


# ============================================================
# TIKTOK CONTROL
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '🎵 TIKTOK API CONTROL'
    '</div>',
    unsafe_allow_html=True
)

if st.session_state.tiktok_access_token:

    st.success(
        "TikTok conectado."
    )

    t1, t2 = st.columns(2)

    with t1:

        if st.button(
            "👤 PERFIL TIKTOK",
            use_container_width=True
        ):

            data, error = tiktok_user()

            if error:

                st.error(error)

            else:

                st.session_state.tiktok_user = data
                st.json(data)

    with t2:

        if st.button(
            "🎬 MIS VIDEOS",
            use_container_width=True
        ):

            data, error = tiktok_videos()

            if error:

                st.error(error)

            else:

                st.session_state.tiktok_videos = data
                st.json(data)

else:

    auth_url = tiktok_authorize_url()

    if auth_url:

        st.link_button(
            "🔐 CONECTAR TIKTOK",
            auth_url,
            use_container_width=True
        )

    else:

        st.info(
            "Configura las credenciales "
            "de TikTok en Secrets."
        )


# ============================================================
# YOUTUBE CONTROL
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '▶️ YOUTUBE API CONTROL'
    '</div>',
    unsafe_allow_html=True
)

if youtube_token():

    st.success(
        "YouTube conectado."
    )

    y1, y2 = st.columns(2)

    with y1:

        if st.button(
            "📺 MI CANAL",
            use_container_width=True
        ):

            data, error = youtube_channel()

            if error:

                st.error(error)

            else:

                st.json(data)

    with y2:

        yt_query = st.text_input(
            "Buscar en YouTube",
            value="Rabino Rap",
            key="youtube_search"
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

                for item in data.get(
                    "items",
                    []
                ):

                    title = (
                        item.get(
                            "snippet",
                            {}
                        ).get(
                            "title",
                            "Video"
                        )
                    )

                    video_id = (
                        item.get(
                            "id",
                            {}
                        ).get(
                            "videoId"
                        )
                    )

                    st.write(
                        f"▶️ {title}"
                    )

                    if video_id:

                        st.link_button(
                            "VER",
                            f"https://www.youtube.com/watch?v={video_id}"
                        )

else:

    auth_url = youtube_authorize_url()

    if auth_url:

        st.link_button(
            "🔐 CONECTAR YOUTUBE",
            auth_url,
            use_container_width=True
        )

    else:

        st.info(
            "Configura YOUTUBE_CLIENT_ID "
            "y YOUTUBE_CLIENT_SECRET."
        )


# ============================================================
# INSTAGRAM
# ============================================================

st.divider()

st.markdown(
    '<div class="section">'
    '📸 INSTAGRAM GRAPH CONTROL'
    '</div>',
    unsafe_allow_html=True
)

if instagram_configured():

    if st.button(
        "📊 CONSULTAR INSTAGRAM",
        use_container_width=True
    ):

        data, error = instagram_request(
            "id,username,name,profile_picture_url,"
            "followers_count,follows_count,media_count"
        )

        if error:

            st.error(error)

        else:

            st.session_state.instagram_data = data

    if st.session_state.instagram_data:

        st.json(
            st.session_state.instagram_data
        )

else:

    st.info(
        "Instagram está preparado para "
        "Graph API mediante credenciales "
        "de una cuenta profesional."
    )

    st.link_button(
        "⚙️ ABRIR META DEVELOPERS",
        INSTAGRAM_DEV,
        use_container_width=True
    )


# ============================================================
# DISTRIBUTION
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
        <p>
        Centro de distribución musical.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR DISTROKID",
        DISTROKID,
        use_container_width=True
    )

with d2:

    st.markdown("""
    <div class="card">
        <h3>🎤 Spotify for Artists</h3>
        <p>
        Administración del perfil artístico.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "ABRIR ARTIST HUB",
        SPOTIFY_ARTISTS,
        use_container_width=True
    )

with d3:

    st.markdown("""
    <div class="card">
        <h3>∞ STREAMING HOUSE</h3>
        <p>
        Panel central de Rabino Rap.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.success(
        "HOUSE ONLINE"
    )


# ============================================================
# API CONFIG
# ============================================================

with st.expander(
    "🔐 CONFIGURACIÓN DE SECRETS"
):

    st.code("""
# .streamlit/secrets.toml

SPOTIFY_CLIENT_ID = "TU_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "TU_CLIENT_SECRET"

TIKTOK_CLIENT_KEY = "TU_CLIENT_KEY"
TIKTOK_CLIENT_SECRET = "TU_CLIENT_SECRET"

YOUTUBE_CLIENT_ID = "TU_GOOGLE_CLIENT_ID"
YOUTUBE_CLIENT_SECRET = "TU_GOOGLE_CLIENT_SECRET"

INSTAGRAM_ACCESS_TOKEN = "TU_ACCESS_TOKEN"
INSTAGRAM_BUSINESS_ACCOUNT_ID = "TU_ACCOUNT_ID"

APP_BASE_URL = "https://TU-APP.streamlit.app"
""")

    st.warning(
        "NO pongas secretos dentro de "
        "streamlit_app.py. "
        "NO los publiques en GitHub."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

STREAMING HOUSE ∞<br>
RABINO RAP<br><br>

MUSIC • DISTRIBUTION • STREAMING • CONTROL<br>
API ENGINE V8 • CLOUD READY

</div>
""", unsafe_allow_html=True)
