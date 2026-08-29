import streamlit as st
import requests
import base64
import secrets
import time
from urllib.parse import urlencode

st.set_page_config(
    page_title="STREAMING HOUSE ∞",
    page_icon="🎵",
    layout="wide"
)

def secret(name, default=""):
    try:
        value = st.secrets.get(name, default)
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

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

TIKTOK_AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TIKTOK_TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = ""

if "spotify_expiry" not in st.session_state:
    st.session_state.spotify_expiry = 0

if "spotify_status" not in st.session_state:
    st.session_state.spotify_status = "NO CONFIGURADO"

if "spotify_results" not in st.session_state:
    st.session_state.spotify_results = None

if "youtube_results" not in st.session_state:
    st.session_state.youtube_results = None

if "tiktok_state" not in st.session_state:
    st.session_state.tiktok_state = ""

def valid(*values):
    return all(str(v).strip() for v in values)

def spotify_token():
    if not valid(
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET
    ):
        st.session_state.spotify_status = "NO CONFIGURADO"
        return None

    if (
        st.session_state.spotify_token
        and time.time() < st.session_state.spotify_expiry
    ):
        return st.session_state.spotify_token

    credentials = (
        SPOTIFY_CLIENT_ID
        + ":"
        + SPOTIFY_CLIENT_SECRET
    )

    encoded = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    try:
        response = requests.post(
            SPOTIFY_TOKEN_URL,
            headers={
                "Authorization": "Basic " + encoded,
                "Content-Type":
                    "application/x-www-form-urlencoded"
            },
            data={
                "grant_type":
                    "client_credentials"
            },
            timeout=20
        )

        if response.status_code != 200:
            st.session_state.spotify_status = (
                "CREDENCIALES RECHAZADAS"
            )
            st.session_state.spotify_token = ""
            return None

        data = response.json()
        token = data.get("access_token")

        if not token:
            st.session_state.spotify_status = (
                "TOKEN NO RECIBIDO"
            )
            return None

        expires = int(
            data.get(
                "expires_in",
                3600
            )
        )

        st.session_state.spotify_token = token
        st.session_state.spotify_expiry = (
            time.time()
            + expires
            - 60
        )

        st.session_state.spotify_status = "ONLINE"

        return token

    except requests.RequestException:
        st.session_state.spotify_status = (
            "CONEXIÓN FALLIDA"
        )
        return None

def spotify_request(endpoint, params=None):
    token = spotify_token()

    if not token:
        return None

    try:
        response = requests.get(
            SPOTIFY_API_URL + endpoint,
            headers={
                "Authorization":
                    "Bearer " + token
            },
            params=params,
            timeout=20
        )

        if response.status_code == 401:
            st.session_state.spotify_token = ""
            st.session_state.spotify_expiry = 0

            token = spotify_token()

            if not token:
                return None

            response = requests.get(
                SPOTIFY_API_URL + endpoint,
                headers={
                    "Authorization":
                        "Bearer " + token
                },
                params=params,
                timeout=20
            )

        if response.status_code != 200:
            return None

        return response.json()

    except requests.RequestException:
        return None

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
        TIKTOK_AUTH_URL
        + "?"
        + urlencode(params)
    )

def youtube_search(query):
    if not YOUTUBE_API_KEY:
        return None

    try:
        response = requests.get(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": 10,
                "key": YOUTUBE_API_KEY
            },
            timeout=20
        )

        if response.status_code != 200:
            return None

        return response.json()

    except requests.RequestException:
        return None

def instagram_info():
    if not valid(
        INSTAGRAM_ACCESS_TOKEN,
        INSTAGRAM_BUSINESS_ACCOUNT_ID
    ):
        return None

    try:
        response = requests.get(
            "https://graph.facebook.com/v23.0/"
            + INSTAGRAM_BUSINESS_ACCOUNT_ID,
            params={
                "fields":
                    "id,username,name,"
                    "profile_picture_url,"
                    "followers_count,"
                    "follows_count,"
                    "media_count",
                "access_token":
                    INSTAGRAM_ACCESS_TOKEN
            },
            timeout=20
        )

        if response.status_code != 200:
            return None

        return response.json()

    except requests.RequestException:
        return None

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
        color:white;
    }

    .block-container {
        max-width:1500px;
        padding-top:1.5rem;
    }

    .title {
        text-align:center;
        font-size:clamp(40px,7vw,82px);
        font-weight:950;
        letter-spacing:7px;
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
        letter-spacing:3px;
        margin-bottom:35px;
    }

    .section {
        font-size:26px;
        font-weight:950;
        letter-spacing:2px;
        margin:30px 0 18px;
    }

    .card {
        background:
        linear-gradient(145deg,#161616,#080808);
        border:1px solid #292929;
        border-radius:18px;
        padding:20px;
        margin-bottom:15px;
        min-height:130px;
    }

    .online {
        color:#55ff82;
        font-weight:900;
    }

    .ready {
        color:#ffd95a;
        font-weight:900;
    }

    .offline {
        color:#ff6666;
        font-weight:900;
    }

    .footer {
        text-align:center;
        color:#444;
        padding:50px 10px;
        letter-spacing:3px;
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
    'RABINO RAP • MUSIC • DISTRIBUTION • '
    'STREAMING • CONTROL'
    '</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.markdown("## 🎛️ CONTROL HOUSE")

    spotify_token()

    if st.session_state.spotify_status == "ONLINE":
        st.markdown(
            '<span class="online">● SPOTIFY ONLINE</span>',
            unsafe_allow_html=True
        )
    elif st.session_state.spotify_status == "NO CONFIGURADO":
        st.markdown(
            '<span class="ready">● SPOTIFY SECRETS</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="offline">● SPOTIFY OFFLINE</span>',
            unsafe_allow_html=True
        )

    if valid(
        TIKTOK_CLIENT_KEY,
        TIKTOK_CLIENT_SECRET,
        TIKTOK_REDIRECT_URI
    ):
        st.markdown(
            '<span class="online">● TIKTOK OAUTH</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="ready">● TIKTOK SECRETS</span>',
            unsafe_allow_html=True
        )

    if YOUTUBE_API_KEY:
        st.markdown(
            '<span class="online">● YOUTUBE ONLINE</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="ready">● YOUTUBE HUB</span>',
            unsafe_allow_html=True
        )

    if valid(
        INSTAGRAM_ACCESS_TOKEN,
        INSTAGRAM_BUSINESS_ACCOUNT_ID
    ):
        st.markdown(
            '<span class="online">● INSTAGRAM ONLINE</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="ready">● INSTAGRAM HUB</span>',
            unsafe_allow_html=True
        )

    st.divider()

    st.write("∞ RABINO RAP")
    st.write("☁️ CLOUD")
    st.write("🔐 SECRET CONTROL")
    st.write("⚡ API HOUSE")

st.markdown(
    '<div class="section">🌐 TIENDAS DIGITALES</div>',
    unsafe_allow_html=True
)

stores = [
    ("🎵 Spotify", "https://open.spotify.com/"),
    ("🍎 Apple Music", "https://music.apple.com/"),
    ("📦 Amazon Music", "https://music.amazon.com/"),
    ("🔵 Deezer", "https://www.deezer.com/"),
    ("🌊 TIDAL", "https://tidal.com/"),
    ("▶️ YouTube Music", "https://music.youtube.com/"),
    ("📻 Pandora", "https://www.pandora.com/"),
    ("🔊 SoundCloud", "https://soundcloud.com/"),
    ("🎧 Audiomack", "https://audiomack.com/"),
    ("🌍 Boomplay", "https://www.boomplay.com/"),
    ("🎶 Anghami", "https://www.anghami.com/"),
    ("💿 Qobuz", "https://www.qobuz.com/"),
    ("🎼 Napster", "https://www.napster.com/"),
    ("📱 TikTok", "https://www.tiktok.com/"),
    ("📸 Instagram", "https://www.instagram.com/"),
    ("📘 Facebook", "https://www.facebook.com/"),
    ("📡 iHeartRadio", "https://www.iheart.com/"),
    ("🔎 Shazam", "https://www.shazam.com/")
]

cols = st.columns(3)

for i, (name, url) in enumerate(stores):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="card">
            <h3>{name}</h3>
            <p>PLATAFORMA DIGITAL</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "ABRIR",
            url,
            use_container_width=True
        )

st.divider()

st.markdown(
    '<div class="section">📦 DISTRIBUCIÓN</div>',
    unsafe_allow_html=True
)

a, b, c = st.columns(3)

with a:
    st.markdown(
        """
        <div class="card">
        <h2>📦 DistroKid</h2>
        <p>Distribución musical</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.link_button(
        "ABRIR DISTROKID",
        "https://distrokid.com/",
        use_container_width=True
    )

with b:
    st.markdown(
        """
        <div class="card">
        <h2>🎤 Spotify for Artists</h2>
        <p>Artist Hub</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.link_button(
        "ABRIR SPOTIFY ARTISTS",
        "https://artists.spotify.com/",
        use_container_width=True
    )

with c:
    st.markdown(
        """
        <div class="card">
        <h2>🎵 TikTok Developers</h2>
        <p>OAuth / API</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.link_button(
        "ABRIR TIKTOK DEV",
        "https://developers.tiktok.com/",
        use_container_width=True
    )

st.divider()

st.markdown(
    '<div class="section">🎵 SPOTIFY ENGINE</div>',
    unsafe_allow_html=True
)

if st.session_state.spotify_status == "ONLINE":

    st.success(
        "🟢 Spotify conectado correctamente"
    )

    q1, q2 = st.columns([4, 1])

    with q1:
        query = st.text_input(
            "Buscar en Spotify",
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

            st.session_state.spotify_results = (
                spotify_search(
                    query.strip(),
                    kind
                )
            )

else:

    st.info(
        "Spotify se controla mediante "
        "SPOTIFY_CLIENT_ID y "
        "SPOTIFY_CLIENT_SECRET en Secrets."
    )

if st.session_state.spotify_results:

    data = st.session_state.spotify_results

    if kind == "artist":

        items = data.get(
            "artists",
            {}
        ).get(
            "items",
            []
        )

        for item in items:

            c1, c2 = st.columns(
                [1, 4]
            )

            with c1:
                images = item.get(
                    "images",
                    []
                )

                if images:
                    st.image(
                        images[0]["url"],
                        width=140
                    )

            with c2:

                st.subheader(
                    "🎤 "
                    + item.get(
                        "name",
                        ""
                    )
                )

                followers = item.get(
                    "followers",
                    {}
                ).get(
                    "total",
                    0
                )

                st.write(
                    f"Seguidores: {followers:,}"
                )

                st.write(
                    "Popularidad:",
                    item.get(
                        "popularity",
                        0
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
                        "ABRIR",
                        url
                    )

            st.divider()

    elif kind == "track":

        items = data.get(
            "tracks",
            {}
        ).get(
            "items",
            []
        )

        for item in items:

            st.subheader(
                "🎵 "
                + item.get(
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
                    "ABRIR TRACK",
                    url
                )

            st.divider()

    elif kind == "album":

        items = data.get(
            "albums",
            {}
        ).get(
            "items",
            []
        )

        for item in items:

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
                "💿 "
                + item.get(
                    "name",
                    ""
                )
            )

            st.write(
                item.get(
                    "release_date",
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
                    "ABRIR ÁLBUM",
                    url
                )

            st.divider()

    elif kind == "playlist":

        items = data.get(
            "playlists",
            {}
        ).get(
            "items",
            []
        )

        for item in items:

            st.subheader(
                "📂 "
                + item.get(
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
                    "ABRIR PLAYLIST",
                    url
                )

            st.divider()

st.markdown(
    '<div class="section">🎵 TIKTOK</div>',
    unsafe_allow_html=True
)

if valid(
    TIKTOK_CLIENT_KEY,
    TIKTOK_CLIENT_SECRET,
    TIKTOK_REDIRECT_URI
):

    st.success(
        "🟢 TikTok OAuth preparado"
    )

    st.link_button(
        "🔐 CONECTAR TIKTOK",
        tiktok_login_url(),
        use_container_width=True
    )

else:

    st.info(
        "Agrega los tres Secrets de TikTok "
        "para activar OAuth."
    )

st.divider()

st.markdown(
    '<div class="section">▶️ YOUTUBE</div>',
    unsafe_allow_html=True
)

if YOUTUBE_API_KEY:

    yt = st.text_input(
        "Buscar en YouTube",
        "Rabino Rap"
    )

    if st.button(
        "🔎 BUSCAR YOUTUBE",
        use_container_width=True
    ):

        st.session_state.youtube_results = (
            youtube_search(yt)
        )

    if st.session_state.youtube_results:

        for item in st.session_state.youtube_results.get(
            "items",
            []
        ):

            title = item.get(
                "snippet",
                {}
            ).get(
                "title",
                "Video"
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
                    "https://www.youtube.com/watch?v="
                    + video_id
                )

else:

    st.info(
        "YouTube permanece disponible como HUB."
    )

st.divider()

st.markdown(
    '<div class="section">📸 INSTAGRAM</div>',
    unsafe_allow_html=True
)

if valid(
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_BUSINESS_ACCOUNT_ID
):

    if st.button(
        "📊 CONSULTAR INSTAGRAM",
        use_container_width=True
    ):

        data = instagram_info()

        if data:

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "SEGUIDORES",
                    f"{data.get('followers_count', 0):,}"
                )

            with c2:
                st.metric(
                    "SIGUIENDO",
                    f"{data.get('follows_count', 0):,}"
                )

            with c3:
                st.metric(
                    "PUBLICACIONES",
                    f"{data.get('media_count', 0):,}"
                )

        else:
            st.error(
                "Instagram no respondió."
            )

else:

    st.info(
        "Instagram permanece disponible mediante Secrets."
    )

st.divider()

st.markdown(
    '<div class="section">⚙️ DEVELOPERS</div>',
    unsafe_allow_html=True
)

x1, x2, x3 = st.columns(3)

with x1:
    st.link_button(
        "SPOTIFY DEVELOPERS",
        "https://developer.spotify.com/",
        use_container_width=True
    )

with x2:
    st.link_button(
        "TIKTOK DEVELOPERS",
        "https://developers.tiktok.com/",
        use_container_width=True
    )

with x3:
    st.link_button(
        "YOUTUBE CONSOLE",
        "https://console.cloud.google.com/",
        use_container_width=True
    )

st.markdown(
    """
    <div class="footer">
    STREAMING HOUSE ∞<br>
    RABINO RAP<br><br>
    MUSIC • DISTRIBUTION • STREAMING • CONTROL
    </div>
    """,
    unsafe_allow_html=True
)
