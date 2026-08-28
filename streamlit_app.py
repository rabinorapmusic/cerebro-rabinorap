import streamlit as st
import requests
import base64
import secrets
import hashlib
import time
from urllib.parse import urlencode

st.set_page_config(
    page_title="STREAMING HOUSE ∞",
    page_icon="🎵",
    layout="wide"
)

def secret(name, default=""):
    try:
        value = st.secrets.get(name)
        if value:
            return str(value).strip()
    except Exception:
        pass
    return default

SPOTIFY_CLIENT_ID = secret("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = secret("SPOTIFY_CLIENT_SECRET")

TIKTOK_CLIENT_KEY = secret("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = secret("TIKTOK_CLIENT_SECRET")
TIKTOK_REDIRECT_URI = secret("TIKTOK_REDIRECT_URI")

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

TIKTOK_AUTHORIZE_URL = "https://www.tiktok.com/v2/auth/authorize/"
TIKTOK_TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
TIKTOK_USER_URL = "https://open.tiktokapis.com/v2/user/info/"

if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = None

if "spotify_expiry" not in st.session_state:
    st.session_state.spotify_expiry = 0

if "spotify_status" not in st.session_state:
    st.session_state.spotify_status = ""

if "tiktok_state" not in st.session_state:
    st.session_state.tiktok_state = None

if "tiktok_token" not in st.session_state:
    st.session_state.tiktok_token = None

if "tiktok_user" not in st.session_state:
    st.session_state.tiktok_user = None

def spotify_token():

    if not SPOTIFY_CLIENT_ID:
        return None, "Falta SPOTIFY_CLIENT_ID."

    if not SPOTIFY_CLIENT_SECRET:
        return None, "Falta SPOTIFY_CLIENT_SECRET."

    if (
        st.session_state.spotify_token
        and time.time() < st.session_state.spotify_expiry
    ):
        return st.session_state.spotify_token, None

    credentials = (
        f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    )

    encoded = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    try:

        response = requests.post(
            SPOTIFY_TOKEN_URL,
            headers={
                "Authorization": f"Basic {encoded}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "client_credentials"
            },
            timeout=20
        )

        if response.status_code != 200:

            try:
                data = response.json()
            except Exception:
                data = response.text

            return None, (
                f"HTTP {response.status_code}: {data}"
            )

        data = response.json()

        token = data.get("access_token")

        if not token:
            return None, "Spotify no entregó access_token."

        expires = int(
            data.get("expires_in", 3600)
        )

        st.session_state.spotify_token = token
        st.session_state.spotify_expiry = (
            time.time() + expires - 60
        )

        return token, None

    except requests.RequestException as e:

        return None, f"Conexión Spotify: {e}"

def spotify_api(endpoint, params=None):

    token, error = spotify_token()

    if error:
        return None, error

    try:

        response = requests.get(
            f"{SPOTIFY_API_URL}{endpoint}",
            headers={
                "Authorization": f"Bearer {token}"
            },
            params=params,
            timeout=20
        )

        if response.status_code == 401:

            st.session_state.spotify_token = None
            st.session_state.spotify_expiry = 0

            token, error = spotify_token()

            if error:
                return None, error

            response = requests.get(
                f"{SPOTIFY_API_URL}{endpoint}",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                params=params,
                timeout=20
            )

        if response.status_code != 200:

            try:
                data = response.json()
            except Exception:
                data = response.text

            return None, (
                f"HTTP {response.status_code}: {data}"
            )

        return response.json(), None

    except requests.RequestException as e:

        return None, f"Conexión Spotify: {e}"

def spotify_search(query, kind):

    return spotify_api(
        "/search",
        {
            "q": query,
            "type": kind,
            "limit": 10,
            "market": "DO"
        }
    )

def spotify_artist(artist_id):

    return spotify_api(
        f"/artists/{artist_id}"
    )

def spotify_albums(artist_id):

    return spotify_api(
        f"/artists/{artist_id}/albums",
        {
            "include_groups": "album,single,compilation",
            "limit": 20,
            "market": "DO"
        }
    )

def spotify_track(track_id):

    return spotify_api(
        f"/tracks/{track_id}"
    )

def spotify_album(album_id):

    return spotify_api(
        f"/albums/{album_id}"
    )

def tiktok_ready():

    return bool(
        TIKTOK_CLIENT_KEY
        and TIKTOK_CLIENT_SECRET
        and TIKTOK_REDIRECT_URI
    )

def tiktok_login_url():

    state = secrets.token_urlsafe(32)

    st.session_state.tiktok_state = state

    params = {
        "client_key": TIKTOK_CLIENT_KEY,
        "response_type": "code",
        "scope": "user.info.basic",
        "redirect_uri": TIKTOK_REDIRECT_URI,
        "state": state
    }

    return (
        f"{TIKTOK_AUTHORIZE_URL}"
        f"?{urlencode(params)}"
    )

def tiktok_exchange(code):

    try:

        response = requests.post(
            TIKTOK_TOKEN_URL,
            headers={
                "Content-Type":
                "application/x-www-form-urlencoded"
            },
            data={
                "client_key": TIKTOK_CLIENT_KEY,
                "client_secret": TIKTOK_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": TIKTOK_REDIRECT_URI
            },
            timeout=20
        )

        if response.status_code != 200:

            try:
                data = response.json()
            except Exception:
                data = response.text

            return None, (
                f"HTTP {response.status_code}: {data}"
            )

        return response.json(), None

    except requests.RequestException as e:

        return None, f"TikTok conexión: {e}"

def tiktok_user(access_token):

    try:

        response = requests.get(
            TIKTOK_USER_URL,
            headers={
                "Authorization":
                f"Bearer {access_token}"
            },
            params={
                "fields":
                "open_id,display_name,username,avatar_url"
            },
            timeout=20
        )

        if response.status_code != 200:

            try:
                data = response.json()
            except Exception:
                data = response.text

            return None, (
                f"HTTP {response.status_code}: {data}"
            )

        return response.json(), None

    except requests.RequestException as e:

        return None, f"TikTok conexión: {e}"

code = st.query_params.get("code")
state = st.query_params.get("state")

if code and state:

    if state == st.session_state.tiktok_state:

        token_data, token_error = tiktok_exchange(
            code
        )

        if token_error:

            st.error(
                f"TikTok: {token_error}"
            )

        else:

            access_token = token_data.get(
                "access_token"
            )

            if access_token:

                st.session_state.tiktok_token = (
                    access_token
                )

                user_data, user_error = (
                    tiktok_user(
                        access_token
                    )
                )

                if user_error:

                    st.error(
                        f"TikTok: {user_error}"
                    )

                else:

                    st.session_state.tiktok_user = (
                        user_data
                    )

                    st.success(
                        "TikTok conectado."
                    )

            else:

                st.error(
                    "TikTok no entregó access_token."
                )

    else:

        st.error(
            "TikTok rechazó el estado OAuth."
        )

    st.query_params.clear()

st.markdown(
    """
    <style>
    .stApp {
        background:
        radial-gradient(
            circle at top left,
            #191919,
            #050505 55%,
            #000000
        );
        color: white;
    }

    .title {
        text-align: center;
        font-size: 64px;
        font-weight: 900;
        letter-spacing: 7px;
    }

    .infinity {
        text-align: center;
        font-size: 110px;
        font-weight: 900;
    }

    .subtitle {
        text-align: center;
        color: #888;
        letter-spacing: 4px;
    }

    .box {
        background: #101010;
        border: 1px solid #292929;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 15px;
    }

    .online {
        color: #55ff88;
        font-weight: 900;
    }

    .offline {
        color: #ff5555;
        font-weight: 900;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title">STREAMING HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="infinity">∞</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">RABINO RAP • CONTROL CENTER</div>',
    unsafe_allow_html=True
)

st.divider()

spotify, spotify_error = spotify_token()

s1, s2, s3 = st.columns(3)

with s1:

    if spotify:

        st.success("🟢 SPOTIFY ONLINE")

    else:

        st.error("🔴 SPOTIFY OFFLINE")

        if spotify_error:
            st.code(
                spotify_error
            )

with s2:

    if tiktok_ready():

        if st.session_state.tiktok_token:

            st.success(
                "🟢 TIKTOK CONNECTED"
            )

        else:

            st.warning(
                "🟡 TIKTOK READY"
            )

    else:

        st.error(
            "🔴 TIKTOK SECRETS FALTANTES"
        )

with s3:

    st.success(
        "🟢 HOUSE ONLINE"
    )

st.divider()

st.header("🎵 SPOTIFY")

if spotify:

    q1, q2 = st.columns(
        [4, 1]
    )

    with q1:

        query = st.text_input(
            "Buscar",
            value="Rabino Rap"
        )

    with q2:

        kind = st.selectbox(
            "Tipo",
            [
                "artist",
                "track",
                "album",
                "playlist"
            ]
        )

    if st.button(
        "🔍 BUSCAR EN SPOTIFY",
        type="primary",
        use_container_width=True
    ):

        if not query.strip():

            st.warning(
                "Escribe una búsqueda."
            )

        else:

            results, error = spotify_search(
                query.strip(),
                kind
            )

            if error:

                st.error(error)

            else:

                items = results.get(
                    f"{kind}s",
                    {}
                ).get(
                    "items",
                    []
                )

                if not items:

                    st.info(
                        "No se encontraron resultados."
                    )

                for item in items:

                    if kind == "artist":

                        images = item.get(
                            "images",
                            []
                        )

                        if images:

                            st.image(
                                images[0]["url"],
                                width=130
                            )

                        st.subheader(
                            item.get(
                                "name",
                                ""
                            )
                        )

                        st.write(
                            f"Seguidores: "
                            f"{item.get('followers', {}).get('total', 0):,}"
                        )

                        st.write(
                            f"Popularidad: "
                            f"{item.get('popularity', 0)}/100"
                        )

                    elif kind == "track":

                        st.subheader(
                            f"🎵 {item.get('name', '')}"
                        )

                        artists = ", ".join(
                            a.get("name", "")
                            for a in item.get(
                                "artists",
                                []
                            )
                        )

                        st.write(
                            artists
                        )

                    elif kind == "album":

                        st.subheader(
                            f"💿 {item.get('name', '')}"
                        )

                        st.write(
                            item.get(
                                "release_date",
                                ""
                            )
                        )

                    elif kind == "playlist":

                        st.subheader(
                            f"📂 {item.get('name', '')}"
                        )

                    url = item.get(
                        "external_urls",
                        {}
                    ).get(
                        "spotify"
                    )

                    if url:

                        st.link_button(
                            "ABRIR EN SPOTIFY",
                            url
                        )

                    st.divider()

else:

    st.warning(
        "Spotify no está conectado."
    )

st.header("🎵 TIKTOK")

if tiktok_ready():

    if st.session_state.tiktok_token:

        st.success(
            "TikTok conectado."
        )

        if st.session_state.tiktok_user:

            st.json(
                st.session_state.tiktok_user
            )

    else:

        login_url = tiktok_login_url()

        st.link_button(
            "🔐 CONECTAR TIKTOK",
            login_url,
            use_container_width=True
        )

else:

    st.warning(
        "Faltan los Secrets de TikTok."
    )

st.divider()

st.header("🔐 CONFIGURACIÓN")

st.write(
    "Spotify y TikTok leen sus credenciales "
    "exclusivamente desde Streamlit Secrets."
)

st.markdown(
    """
    <div class="box">
    <b>Spotify</b><br>
    Client ID + Client Secret
    <br><br>
    <b>TikTok</b><br>
    Client Key + Client Secret + Redirect URI
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "STREAMING HOUSE ∞ • RABINO RAP"
)
