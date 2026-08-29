import streamlit as st
import requests
import base64
import secrets
import hashlib
import base64
import time
from urllib.parse import urlencode

st.set_page_config(
    page_title="STREAMING HOUSE ∞",
    page_icon="🎵",
    layout="wide"
)

def S(k, d=""):
    try:
        v = st.secrets.get(k, d)
        return str(v).strip() if v else d
    except:
        return d

SPOTIFY_CLIENT_ID = S("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = S("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = S("SPOTIFY_REDIRECT_URI")

TIKTOK_CLIENT_KEY = S("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = S("TIKTOK_CLIENT_SECRET")
TIKTOK_REDIRECT_URI = S("TIKTOK_REDIRECT_URI")

YOUTUBE_API_KEY = S("YOUTUBE_API_KEY")
INSTAGRAM_ACCESS_TOKEN = S("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = S("INSTAGRAM_BUSINESS_ACCOUNT_ID")

if "spotify_access_token" not in st.session_state:
    st.session_state.spotify_access_token = ""

if "spotify_refresh_token" not in st.session_state:
    st.session_state.spotify_refresh_token = ""

if "spotify_expires_at" not in st.session_state:
    st.session_state.spotify_expires_at = 0

if "spotify_state" not in st.session_state:
    st.session_state.spotify_state = ""

if "spotify_pkce_verifier" not in st.session_state:
    st.session_state.spotify_pkce_verifier = ""

if "tiktok_state" not in st.session_state:
    st.session_state.tiktok_state = ""

if "tiktok_token" not in st.session_state:
    st.session_state.tiktok_token = ""

def spotify_authorize_url():
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(
            verifier.encode("utf-8")
        ).digest()
    ).decode("utf-8").rstrip("=")

    st.session_state.spotify_state = state
    st.session_state.spotify_pkce_verifier = verifier

    params = {
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "state": state,
        "scope": "user-read-private user-read-email",
        "code_challenge_method": "S256",
        "code_challenge": challenge
    }

    return (
        "https://accounts.spotify.com/authorize?"
        + urlencode(params)
    )

def spotify_exchange(code):
    try:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "client_id": SPOTIFY_CLIENT_ID,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": SPOTIFY_REDIRECT_URI,
                "code_verifier":
                    st.session_state.spotify_pkce_verifier
            },
            timeout=30
        )

        if response.status_code != 200:
            try:
                data = response.json()
            except:
                data = response.text
            return None, data

        return response.json(), None

    except Exception as e:
        return None, str(e)

def spotify_refresh():
    refresh = st.session_state.spotify_refresh_token

    if not refresh:
        return False

    try:
        raw = (
            f"{SPOTIFY_CLIENT_ID}:"
            f"{SPOTIFY_CLIENT_SECRET}"
        )

        encoded = base64.b64encode(
            raw.encode("utf-8")
        ).decode("utf-8")

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {encoded}",
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh
            },
            timeout=30
        )

        if response.status_code != 200:
            return False

        data = response.json()

        token = data.get("access_token")

        if not token:
            return False

        st.session_state.spotify_access_token = token
        st.session_state.spotify_expires_at = (
            time.time()
            + int(data.get("expires_in", 3600))
            - 60
        )

        if data.get("refresh_token"):
            st.session_state.spotify_refresh_token = (
                data["refresh_token"]
            )

        return True

    except:
        return False

def spotify_token():
    if (
        st.session_state.spotify_access_token
        and time.time()
        < st.session_state.spotify_expires_at
    ):
        return st.session_state.spotify_access_token

    if spotify_refresh():
        return st.session_state.spotify_access_token

    return ""

def spotify_api(path, params=None):
    token = spotify_token()

    if not token:
        return None, "SPOTIFY_NOT_CONNECTED"

    try:
        response = requests.get(
            "https://api.spotify.com/v1" + path,
            headers={
                "Authorization": f"Bearer {token}"
            },
            params=params,
            timeout=30
        )

        if response.status_code == 401:
            if spotify_refresh():
                token = st.session_state.spotify_access_token

                response = requests.get(
                    "https://api.spotify.com/v1" + path,
                    headers={
                        "Authorization":
                            f"Bearer {token}"
                    },
                    params=params,
                    timeout=30
                )

        if response.status_code != 200:
            try:
                data = response.json()
            except:
                data = response.text

            return None, data

        return response.json(), None

    except Exception as e:
        return None, str(e)

def spotify_search(q, kind):
    return spotify_api(
        "/search",
        {
            "q": q,
            "type": kind,
            "limit": 10
        }
    )

def tiktok_url():
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
        "https://www.tiktok.com/v2/auth/authorize/?"
        + urlencode(params)
    )

spotify_code = st.query_params.get("code")
spotify_state = st.query_params.get("state")

if (
    spotify_code
    and spotify_state
    and st.session_state.spotify_state
    and spotify_state == st.session_state.spotify_state
    and st.session_state.spotify_pkce_verifier
):

    token_data, token_error = spotify_exchange(
        spotify_code
    )

    if token_data:

        st.session_state.spotify_access_token = (
            token_data.get("access_token", "")
        )

        st.session_state.spotify_refresh_token = (
            token_data.get("refresh_token", "")
        )

        st.session_state.spotify_expires_at = (
            time.time()
            + int(
                token_data.get(
                    "expires_in",
                    3600
                )
            )
            - 60
        )

        st.session_state.spotify_state = ""
        st.session_state.spotify_pkce_verifier = ""

    st.query_params.clear()

spotify = spotify_token()

st.markdown(
    """
    <style>
    .stApp {
        background:
        radial-gradient(
            circle at 15% 0%,
            #202020 0%,
            #080808 45%,
            #000000 100%
        );
    }
    .block-container {
        max-width:1500px;
        padding-top:2rem;
    }
    .title {
        text-align:center;
        font-size:clamp(42px,7vw,82px);
        font-weight:950;
        letter-spacing:8px;
    }
    .infinity {
        text-align:center;
        font-size:110px;
        font-weight:950;
        line-height:.8;
    }
    .subtitle {
        text-align:center;
        color:#777;
        letter-spacing:4px;
        margin-bottom:35px;
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
    '<div class="subtitle">'
    'RABINO RAP • MUSIC • STREAMING • CONTROL'
    '</div>',
    unsafe_allow_html=True
)

a, b, c, d = st.columns(4)

with a:
    if spotify:
        st.success("🟢 SPOTIFY ONLINE")
    else:
        st.error("🔴 SPOTIFY OFFLINE")

with b:
    if (
        TIKTOK_CLIENT_KEY
        and TIKTOK_CLIENT_SECRET
        and TIKTOK_REDIRECT_URI
    ):
        st.success("🟢 TIKTOK READY")
    else:
        st.warning("🟡 TIKTOK")

with c:
    if YOUTUBE_API_KEY:
        st.success("🟢 YOUTUBE ONLINE")
    else:
        st.warning("🟡 YOUTUBE")

with d:
    if (
        INSTAGRAM_ACCESS_TOKEN
        and INSTAGRAM_BUSINESS_ACCOUNT_ID
    ):
        st.success("🟢 INSTAGRAM ONLINE")
    else:
        st.warning("🟡 INSTAGRAM")

st.divider()

st.header("🎵 SPOTIFY")

if not spotify:

    if (
        SPOTIFY_CLIENT_ID
        and SPOTIFY_CLIENT_SECRET
        and SPOTIFY_REDIRECT_URI
    ):

        st.link_button(
            "🔐 CONECTAR SPOTIFY",
            spotify_authorize_url(),
            use_container_width=True
        )

    else:

        st.error(
            "Faltan SPOTIFY_CLIENT_ID, "
            "SPOTIFY_CLIENT_SECRET o "
            "SPOTIFY_REDIRECT_URI."
        )

else:

    st.success("SPOTIFY AUTORIZADO")

    q1, q2 = st.columns([4,1])

    with q1:
        query = st.text_input(
            "Buscar",
            "Rabino Rap"
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
        "🔎 BUSCAR SPOTIFY",
        type="primary",
        use_container_width=True
    ):

        data, error = spotify_search(
            query,
            kind
        )

        if error:
            st.error(str(error))
        else:

            items = data.get(
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
                            width=140
                        )

                    st.subheader(
                        item.get("name", "")
                    )

                    st.write(
                        "Seguidores:",
                        item.get(
                            "followers",
                            {}
                        ).get(
                            "total",
                            0
                        )
                    )

                elif kind == "track":

                    st.subheader(
                        "🎵 " +
                        item.get("name", "")
                    )

                    st.write(
                        ", ".join(
                            x.get("name", "")
                            for x in item.get(
                                "artists",
                                []
                            )
                        )
                    )

                elif kind == "album":

                    st.subheader(
                        "💿 " +
                        item.get("name", "")
                    )

                elif kind == "playlist":

                    st.subheader(
                        "📂 " +
                        item.get("name", "")
                    )

                url = item.get(
                    "external_urls",
                    {}
                ).get(
                    "spotify"
                )

                if url:
                    st.link_button(
                        "ABRIR SPOTIFY",
                        url
                    )

                st.divider()

st.header("🎵 TIKTOK")

if (
    TIKTOK_CLIENT_KEY
    and TIKTOK_CLIENT_SECRET
    and TIKTOK_REDIRECT_URI
):

    st.link_button(
        "🔐 CONECTAR TIKTOK",
        tiktok_url(),
        use_container_width=True
    )

else:

    st.warning(
        "Configura los Secrets de TikTok."
    )

st.divider()

st.header("▶️ YOUTUBE")

if YOUTUBE_API_KEY:

    yq = st.text_input(
        "Buscar YouTube",
        "Rabino Rap"
    )

    if st.button(
        "BUSCAR YOUTUBE",
        use_container_width=True
    ):

        try:

            response = requests.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "q": yq,
                    "type": "video",
                    "maxResults": 10,
                    "key": YOUTUBE_API_KEY
                },
                timeout=30
            )

            if response.status_code == 200:

                for item in response.json().get(
                    "items",
                    []
                ):

                    title = item.get(
                        "snippet",
                        {}
                    ).get(
                        "title",
                        ""
                    )

                    video_id = item.get(
                        "id",
                        {}
                    ).get(
                        "videoId"
                    )

                    st.subheader(title)

                    if video_id:
                        st.video(
                            f"https://www.youtube.com/watch?v={video_id}"
                        )

            else:
                st.error(response.text)

        except Exception as e:
            st.error(str(e))

st.divider()

st.header("📸 INSTAGRAM")

if (
    INSTAGRAM_ACCESS_TOKEN
    and INSTAGRAM_BUSINESS_ACCOUNT_ID
):

    if st.button(
        "CONSULTAR INSTAGRAM",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"https://graph.facebook.com/v23.0/"
                f"{INSTAGRAM_BUSINESS_ACCOUNT_ID}",
                params={
                    "fields":
                    "id,username,name,"
                    "followers_count,"
                    "follows_count,"
                    "media_count",
                    "access_token":
                    INSTAGRAM_ACCESS_TOKEN
                },
                timeout=30
            )

            if response.status_code == 200:

                data = response.json()

                x, y, z = st.columns(3)

                with x:
                    st.metric(
                        "SEGUIDORES",
                        data.get(
                            "followers_count",
                            0
                        )
                    )

                with y:
                    st.metric(
                        "SIGUIENDO",
                        data.get(
                            "follows_count",
                            0
                        )
                    )

                with z:
                    st.metric(
                        "PUBLICACIONES",
                        data.get(
                            "media_count",
                            0
                        )
                    )

            else:
                st.error(response.text)

        except Exception as e:
            st.error(str(e))

st.divider()

st.markdown(
    '<div style="text-align:center;color:#555;padding:40px">'
    'STREAMING HOUSE ∞<br>RABINO RAP'
    '</div>',
    unsafe_allow_html=True
)
