import streamlit as st
import requests
import base64
import time
import secrets
import hashlib
import urllib.parse

st.set_page_config(
    page_title="STREAMING HOUSE ∞",
    page_icon="🎵",
    layout="wide"
)

def secret(name, default=""):
    try:
        value = st.secrets.get(name)
        return str(value).strip() if value else default
    except Exception:
        return default

SPOTIFY_CLIENT_ID = secret("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = secret("SPOTIFY_CLIENT_SECRET")

TIKTOK_CLIENT_KEY = secret("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = secret("TIKTOK_CLIENT_SECRET")
TIKTOK_REDIRECT_URI = secret("TIKTOK_REDIRECT_URI")

YOUTUBE_API_KEY = secret("YOUTUBE_API_KEY")
INSTAGRAM_ACCESS_TOKEN = secret("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = secret("INSTAGRAM_BUSINESS_ACCOUNT_ID")

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

def spotify_token():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None, "SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET"

    if (
        st.session_state.spotify_token
        and time.time() < st.session_state.spotify_expiry
    ):
        return st.session_state.spotify_token, None

    try:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            auth=(
                SPOTIFY_CLIENT_ID,
                SPOTIFY_CLIENT_SECRET
            ),
            data={
                "grant_type": "client_credentials"
            },
            timeout=30
        )

        if response.status_code != 200:
            try:
                data = response.json()
                message = data.get(
                    "error_description",
                    data.get("error", response.text)
                )
            except Exception:
                message = response.text

            return None, f"{response.status_code}: {message}"

        data = response.json()
        token = data.get("access_token")

        if not token:
            return None, "Spotify no devolvió token"

        expires = int(
            data.get("expires_in", 3600)
        )

        st.session_state.spotify_token = token
        st.session_state.spotify_expiry = (
            time.time() + expires - 60
        )

        return token, None

    except Exception as e:
        return None, str(e)

def spotify_get(path, params=None):
    token, error = spotify_token()

    if error:
        return None, error

    try:
        response = requests.get(
            f"https://api.spotify.com/v1{path}",
            headers={
                "Authorization": f"Bearer {token}"
            },
            params=params,
            timeout=30
        )

        if response.status_code == 401:
            st.session_state.spotify_token = None
            st.session_state.spotify_expiry = 0
            token, error = spotify_token()

            if error:
                return None, error

            response = requests.get(
                f"https://api.spotify.com/v1{path}",
                headers={
                    "Authorization": f"Bearer {token}"
                },
                params=params,
                timeout=30
            )

        if response.status_code != 200:
            try:
                data = response.json()
            except Exception:
                data = response.text

            return None, f"{response.status_code}: {data}"

        return response.json(), None

    except Exception as e:
        return None, str(e)

def spotify_search(query, kind):
    return spotify_get(
        "/search",
        {
            "q": query,
            "type": kind,
            "limit": 10
        }
    )

def tiktok_login():
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(
            verifier.encode()
        ).digest()
    ).decode().rstrip("=")

    st.session_state.tiktok_state = state
    st.session_state.tiktok_verifier = verifier

    params = {
        "client_key": TIKTOK_CLIENT_KEY,
        "response_type": "code",
        "scope": "user.info.basic",
        "redirect_uri": TIKTOK_REDIRECT_URI,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256"
    }

    return (
        "https://www.tiktok.com/v2/auth/authorize/?"
        + urllib.parse.urlencode(params)
    )

st.markdown("""
<style>
.stApp {
    background:
    radial-gradient(
        circle at 20% 0%,
        #202020 0%,
        #080808 45%,
        #000000 100%
    );
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
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
    line-height:.75;
}

.subtitle {
    text-align:center;
    color:#777;
    letter-spacing:4px;
    margin-bottom:35px;
}

.card {
    background:#0c0c0c;
    border:1px solid #292929;
    border-radius:18px;
    padding:20px;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">STREAMING HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="infinity">∞</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">RABINO RAP • MUSIC • STREAMING • CONTROL</div>',
    unsafe_allow_html=True
)

spotify, spotify_error = spotify_token()

a, b, c, d = st.columns(4)

with a:
    if spotify:
        st.success("🟢 SPOTIFY ONLINE")
    else:
        st.error("🔴 SPOTIFY ERROR")

with b:
    if TIKTOK_CLIENT_KEY and TIKTOK_CLIENT_SECRET and TIKTOK_REDIRECT_URI:
        if st.session_state.tiktok_token:
            st.success("🟢 TIKTOK ONLINE")
        else:
            st.info("🟡 TIKTOK READY")
    else:
        st.warning("🟡 TIKTOK SECRETS")

with c:
    if YOUTUBE_API_KEY:
        st.success("🟢 YOUTUBE ONLINE")
    else:
        st.info("🟡 YOUTUBE")

with d:
    if INSTAGRAM_ACCESS_TOKEN and INSTAGRAM_BUSINESS_ACCOUNT_ID:
        st.success("🟢 INSTAGRAM ONLINE")
    else:
        st.info("🟡 INSTAGRAM")

st.divider()

st.header("🎵 SPOTIFY")

if spotify:

    q1, q2 = st.columns([4, 1])

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

        if query.strip():

            data, error = spotify_search(
                query.strip(),
                kind
            )

            if error:
                st.error(error)
            else:

                items = data.get(
                    f"{kind}s",
                    {}
                ).get(
                    "items",
                    []
                )

                for item in items:

                    if kind == "artist":

                        images = item.get(
                            "images",
                            []
                        )

                        col1, col2 = st.columns(
                            [1, 5]
                        )

                        with col1:
                            if images:
                                st.image(
                                    images[0]["url"]
                                )

                        with col2:
                            st.subheader(
                                item.get(
                                    "name",
                                    ""
                                )
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

                    elif kind == "track":

                        st.subheader(
                            "🎵 " +
                            item.get(
                                "name",
                                ""
                            )
                        )

                        artists = ", ".join(
                            artist.get(
                                "name",
                                ""
                            )
                            for artist in item.get(
                                "artists",
                                []
                            )
                        )

                        st.write(artists)

                        url = item.get(
                            "external_urls",
                            {}
                        ).get(
                            "spotify"
                        )

                        if url:
                            st.link_button(
                                "ABRIR",
                                url
                            )

                    elif kind == "album":

                        st.subheader(
                            "💿 " +
                            item.get(
                                "name",
                                ""
                            )
                        )

                        images = item.get(
                            "images",
                            []
                        )

                        if images:
                            st.image(
                                images[0]["url"],
                                width=180
                            )

                        st.write(
                            item.get(
                                "release_date",
                                ""
                            )
                        )

                    elif kind == "playlist":

                        st.subheader(
                            "📂 " +
                            item.get(
                                "name",
                                ""
                            )
                        )

                        st.write(
                            item.get(
                                "description",
                                ""
                            )
                        )

                    st.divider()

else:

    if spotify_error:
        st.error(
            f"Spotify no pudo conectarse: {spotify_error}"
        )

st.header("🎵 TIKTOK")

if (
    TIKTOK_CLIENT_KEY
    and TIKTOK_CLIENT_SECRET
    and TIKTOK_REDIRECT_URI
):

    if st.session_state.tiktok_token:

        st.success("🟢 TIKTOK CONECTADO")

    else:

        st.link_button(
            "🔐 CONECTAR TIKTOK",
            tiktok_login(),
            use_container_width=True
        )

else:

    st.warning(
        "Faltan Secrets de TikTok"
    )

st.divider()

st.header("▶️ YOUTUBE")

if YOUTUBE_API_KEY:

    youtube_query = st.text_input(
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
                    "q": youtube_query,
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

                    video_id = item.get(
                        "id",
                        {}
                    ).get(
                        "videoId"
                    )

                    title = item.get(
                        "snippet",
                        {}
                    ).get(
                        "title",
                        "Video"
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

else:

    st.info(
        "YouTube conectado mediante Secrets."
    )

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

else:

    st.info(
        "Instagram conectado mediante Secrets."
    )

st.divider()

st.markdown(
    '<div style="text-align:center;color:#555;padding:40px;letter-spacing:3px">'
    'STREAMING HOUSE ∞<br>RABINO RAP'
    '</div>',
    unsafe_allow_html=True
)
```0
