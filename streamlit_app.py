import streamlit as st
import requests
import base64
import os
import urllib.parse

st.set_page_config(
    page_title="STREAMING HOUSE ∞",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp{
    background:
    radial-gradient(circle at top left,#181818 0%,#070707 40%,#000 100%);
    color:white;
}

.block-container{
    max-width:1400px;
    padding-top:2rem;
}

.infinity{
    text-align:center;
    font-size:64px;
    font-weight:900;
    line-height:1;
}

.house-title{
    text-align:center;
    font-size:42px;
    font-weight:900;
    letter-spacing:4px;
}

.house-subtitle{
    text-align:center;
    color:#999;
    margin-bottom:30px;
}

.section-title{
    font-size:23px;
    font-weight:900;
    margin-top:25px;
    margin-bottom:15px;
}

.track-card{
    background:linear-gradient(145deg,#171717,#090909);
    border:1px solid #292929;
    border-radius:16px;
    padding:16px;
    margin:8px 0;
}

.track-name{
    font-size:19px;
    font-weight:900;
}

.artist-name{
    color:#aaa;
    margin-top:5px;
}

</style>
""", unsafe_allow_html=True)


def get_secret(name):

    try:
        value = st.secrets.get(name, "")

        if value:
            return str(value).strip()

    except Exception:
        pass

    return os.getenv(name, "").strip()


SPOTIFY_CLIENT_ID = get_secret(
    "SPOTIFY_CLIENT_ID"
)

SPOTIFY_CLIENT_SECRET = get_secret(
    "SPOTIFY_CLIENT_SECRET"
)


def get_spotify_token():

    if not SPOTIFY_CLIENT_ID:
        return {
            "ok": False,
            "status": "NO_CLIENT_ID",
            "message": "SPOTIFY_CLIENT_ID no encontrado."
        }

    if not SPOTIFY_CLIENT_SECRET:
        return {
            "ok": False,
            "status": "NO_CLIENT_SECRET",
            "message": "SPOTIFY_CLIENT_SECRET no encontrado."
        }

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
            "https://accounts.spotify.com/api/token",
            headers=headers,
            data={
                "grant_type":
                "client_credentials"
            },
            timeout=20
        )

    except requests.exceptions.Timeout:

        return {
            "ok": False,
            "status": "TIMEOUT",
            "message":
            "Spotify tardó demasiado en responder."
        }

    except requests.exceptions.ConnectionError:

        return {
            "ok": False,
            "status": "CONNECTION_ERROR",
            "message":
            "No se pudo conectar con Spotify."
        }

    except Exception as e:

        return {
            "ok": False,
            "status": "UNKNOWN_ERROR",
            "message": str(e)
        }

    if response.status_code == 200:

        try:

            data = response.json()

            token = data.get(
                "access_token"
            )

            if token:

                return {
                    "ok": True,
                    "token": token,
                    "status": "CONNECTED",
                    "message":
                    "Spotify conectado."
                }

        except Exception:
            pass

    try:

        data = response.json()

        error = data.get(
            "error",
            "unknown_error"
        )

        description = data.get(
            "error_description",
            response.text
        )

    except Exception:

        error = "unknown_error"
        description = response.text

    return {
        "ok": False,
        "status":
        f"HTTP_{response.status_code}",
        "spotify_error":
        error,
        "message":
        description
    }


def spotify_search(query, token):

    headers = {
        "Authorization":
        f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": "track",
        "market": "US",
        "limit": 10
    }

    try:

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params=params,
            timeout=20
        )

        if response.status_code == 200:

            data = response.json()

            return {
                "ok": True,
                "items":
                data.get(
                    "tracks",
                    {}
                ).get(
                    "items",
                    []
                )
            }

        try:

            error_data = response.json()

        except Exception:

            error_data = {}

        return {
            "ok": False,
            "items": [],
            "status":
            response.status_code,
            "error":
            error_data,
            "message":
            response.text
        }

    except requests.exceptions.Timeout:

        return {
            "ok": False,
            "items": [],
            "status": "TIMEOUT",
            "error": {},
            "message":
            "La búsqueda de Spotify agotó el tiempo."
        }

    except requests.exceptions.ConnectionError:

        return {
            "ok": False,
            "items": [],
            "status":
            "CONNECTION_ERROR",
            "error": {},
            "message":
            "No se pudo conectar con Spotify."
        }

    except Exception as e:

        return {
            "ok": False,
            "items": [],
            "status":
            "UNKNOWN_ERROR",
            "error": {},
            "message": str(e)
        }


def apple_search(query):

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

        if response.status_code == 200:

            return response.json().get(
                "results",
                []
            )

    except Exception:
        pass

    return []


def encode(query):

    return urllib.parse.quote(
        query,
        safe=""
    )


def platform_links(query):

    q = encode(query)

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
        f"https://www.instagram.com/explore/search/keyword/?q={q}"
    }


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
    "https://artists.tiktok.com/"
}


st.markdown(
    '<div class="infinity">∞</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="house-title">'
    'STREAMING HOUSE'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="house-subtitle">'
    'RABINO RAP • MUSIC • STREAMING • DISTRIBUTION'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-title">'
    '🔎 BUSCADOR GLOBAL'
    '</div>',
    unsafe_allow_html=True
)


query_input = st.text_input(
    "Artista, canción o álbum",
    value="Rabino Rap",
    placeholder="Escribe artista o canción"
)


if "query" not in st.session_state:

    st.session_state.query = query_input


if st.button(
    "🚀 BUSCAR EN TODAS LAS PLATAFORMAS",
    use_container_width=True,
    type="primary"
):

    st.session_state.query = query_input


query = st.session_state.query


links = platform_links(query)


st.markdown(
    '<div class="section-title">'
    '🎧 PLATAFORMAS DIGITALES'
    '</div>',
    unsafe_allow_html=True
)


c1, c2, c3 = st.columns(3)


with c1:

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


with c2:

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


with c3:

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


spotify = get_spotify_token()


st.markdown(
    '<div class="section-title">'
    '🔌 SPOTIFY API'
    '</div>',
    unsafe_allow_html=True
)


if spotify["ok"]:

    st.success(
        "🟢 SPOTIFY API ACTIVA"
    )

    spotify_token = spotify["token"]

else:

    spotify_token = None

    st.error(
        "🔴 ERROR DE SPOTIFY"
    )

    st.warning(
        spotify.get(
            "status",
            "UNKNOWN"
        )
    )

    st.write(
        spotify.get(
            "message",
            "Error desconocido."
        )
    )


if spotify_token:

    result = spotify_search(
        query,
        spotify_token
    )

    if result["ok"]:

        tracks = result["items"]

        st.markdown(
            '<div class="section-title">'
            '🟢 RESULTADOS REALES DE SPOTIFY'
            '</div>',
            unsafe_allow_html=True
        )

        if not tracks:

            st.info(
                "Spotify no encontró resultados."
            )

        for track in tracks:

            name = track.get(
                "name",
                "Sin título"
            )

            artists = ", ".join(
                artist.get(
                    "name",
                    ""
                )
                for artist in track.get(
                    "artists",
                    []
                )
            )

            album = track.get(
                "album",
                {}
            )

            images = album.get(
                "images",
                []
            )

            image = (
                images[0]["url"]
                if images
                else None
            )

            spotify_url = (
                track.get(
                    "external_urls",
                    {}
                ).get(
                    "spotify"
                )
            )

            preview = track.get(
                "preview_url"
            )


            col1, col2 = st.columns(
                [1, 4]
            )


            with col1:

                if image:

                    st.image(
                        image,
                        use_container_width=True
                    )


            with col2:

                st.markdown(
                    f"""
                    <div class="track-card">
                        <div class="track-name">
                            {name}
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


                if preview:

                    st.audio(
                        preview
                    )


    else:

        st.error(
            "Spotify API respondió con "
            f"{result.get('status')}"
        )

        if result.get("error"):

            st.json(
                result["error"]
            )

        if result.get("message"):

            with st.expander(
                "Respuesta técnica de Spotify"
            ):

                st.code(
                    result["message"]
                )


# ============================================================
# APPLE MUSIC
# ============================================================

apple_results = apple_search(
    query
)


if apple_results:

    st.markdown(
        '<div class="section-title">'
        '🍎 RESULTADOS APPLE MUSIC'
        '</div>',
        unsafe_allow_html=True
    )


    for item in apple_results:

        name = item.get(
            "trackName",
            "Sin título"
        )

        artist = item.get(
            "artistName",
            "Artista desconocido"
        )

        artwork = item.get(
            "artworkUrl100"
        )

        url = item.get(
            "trackViewUrl"
        )


        col1, col2 = st.columns(
            [1, 4]
        )


        with col1:

            if artwork:

                st.image(
                    artwork,
                    use_container_width=True
                )


        with col2:

            st.markdown(
                f"""
                <div class="track-card">

                    <div class="track-name">
                        {name}
                    </div>

                    <div class="artist-name">
                        {artist}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            if url:

                st.link_button(
                    "Abrir en Apple Music",
                    url
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
# DISTROKID
# ============================================================

st.divider()


st.markdown(
    '<div class="section-title">'
    '📦 DISTRIBUCIÓN MUSICAL'
    '</div>',
    unsafe_allow_html=True
)


st.link_button(
    "🚀 ABRIR DISTROKID",
    ARTIST_TOOLS["DistroKid"],
    use_container_width=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🎵 STREAMING HOUSE ∞"
    )

    st.markdown(
        "**RABINO RAP**"
    )

    st.divider()


    st.markdown(
        "## 🔐 SPOTIFY"
    )


    if SPOTIFY_CLIENT_ID:

        st.success(
            "Client ID detectado"
        )

    else:

        st.error(
            "Client ID no detectado"
        )


    if SPOTIFY_CLIENT_SECRET:

        st.success(
            "Client Secret detectado"
        )

    else:

        st.error(
            "Client Secret no detectado"
        )


    st.divider()


    if spotify["ok"]:

        st.success(
            "🟢 SPOTIFY CONECTADO"
        )

    else:

        st.error(
            "🔴 SPOTIFY CON ERROR"
        )

        st.caption(
            spotify.get(
                "status",
                "UNKNOWN"
            )
        )


    st.divider()


    st.markdown(
        "### Plataformas"
    )

    st.write("🟢 Spotify")
    st.write("🍎 Apple Music")
    st.write("▶️ YouTube")
    st.write("🎵 YouTube Music")
    st.write("🟠 Amazon Music")
    st.write("🔵 Deezer")
    st.write("🌊 TIDAL")
    st.write("☁️ SoundCloud")
    st.write("🎵 TikTok")
    st.write("📸 Instagram")


    st.divider()


    st.caption(
        "STREAMING HOUSE ∞"
    )

    st.caption(
        "RABINO RAP"
    )
