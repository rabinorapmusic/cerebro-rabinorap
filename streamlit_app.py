# ============================================================
# STREAMING HOUSE ∞
# RABINO RAP
# ULTIMATE STREAMING HUB
#
# Spotify API + Apple Search
# Buscador global
# Plataformas digitales
# Centro del artista
# Diagnóstico real de Spotify
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
# ESTILO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at top left,
            #171717 0%,
            #080808 38%,
            #000000 100%
        );
    color: white;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

.house-infinity {
    text-align: center;
    font-size: 65px;
    font-weight: 900;
    line-height: 1;
}

.house-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    letter-spacing: 4px;
}

.house-subtitle {
    text-align: center;
    color: #999;
    font-size: 15px;
    margin-bottom: 30px;
}

.section-title {
    font-size: 23px;
    font-weight: 900;
    margin-top: 25px;
    margin-bottom: 15px;
}

.track-card {
    background:
        linear-gradient(
            145deg,
            #171717,
            #080808
        );
    border: 1px solid #292929;
    border-radius: 16px;
    padding: 16px;
    margin: 8px 0;
}

.track-name {
    font-size: 19px;
    font-weight: 900;
}

.artist-name {
    color: #aaa;
    margin-top: 5px;
}

.status-card {
    background: #101010;
    border: 1px solid #292929;
    border-radius: 15px;
    padding: 15px;
}

.small {
    color: #999;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 11px !important;
    font-weight: 800 !important;
}

div.stLinkButton > a {
    border-radius: 11px !important;
    font-weight: 800 !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SECRETS
# ============================================================

def get_secret(name: str) -> str:

    # Streamlit Secrets
    try:
        value = st.secrets.get(name, "")

        if value is not None:
            value = str(value).strip()

            if value:
                return value

    except Exception:
        pass

    # Variables de entorno
    try:
        return os.getenv(name, "").strip()
    except Exception:
        return ""


SPOTIFY_CLIENT_ID = get_secret(
    "SPOTIFY_CLIENT_ID"
)

SPOTIFY_CLIENT_SECRET = get_secret(
    "SPOTIFY_CLIENT_SECRET"
)


# ============================================================
# DIAGNÓSTICO DE SECRETOS
# ============================================================

def spotify_secret_status():

    return {
        "client_id": bool(SPOTIFY_CLIENT_ID),
        "client_secret": bool(SPOTIFY_CLIENT_SECRET),
        "client_id_length": len(SPOTIFY_CLIENT_ID),
        "client_secret_length": len(SPOTIFY_CLIENT_SECRET),
    }


# ============================================================
# SPOTIFY TOKEN
# ============================================================

def get_spotify_token():

    if not SPOTIFY_CLIENT_ID:

        return {
            "ok": False,
            "token": None,
            "status": "NO_CLIENT_ID",
            "message":
                "SPOTIFY_CLIENT_ID no está configurado."
        }

    if not SPOTIFY_CLIENT_SECRET:

        return {
            "ok": False,
            "token": None,
            "status": "NO_CLIENT_SECRET",
            "message":
                "SPOTIFY_CLIENT_SECRET no está configurado."
        }

    credentials = (
        f"{SPOTIFY_CLIENT_ID}:"
        f"{SPOTIFY_CLIENT_SECRET}"
    )

    encoded = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type":
            "application/x-www-form-urlencoded"
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

    except requests.exceptions.Timeout:

        return {
            "ok": False,
            "token": None,
            "status": "TIMEOUT",
            "message":
                "Spotify tardó demasiado en responder."
        }

    except requests.exceptions.ConnectionError:

        return {
            "ok": False,
            "token": None,
            "status": "CONNECTION_ERROR",
            "message":
                "No se pudo conectar con Spotify."
        }

    except Exception as e:

        return {
            "ok": False,
            "token": None,
            "status": "UNKNOWN_ERROR",
            "message": str(e)
        }


    # --------------------------------------------------------
    # RESPUESTA CORRECTA
    # --------------------------------------------------------

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
                        "Spotify API conectada correctamente.",
                    "expires_in":
                        data.get("expires_in", 0)
                }

        except Exception:
            pass


    # --------------------------------------------------------
    # ERROR DE SPOTIFY
    # --------------------------------------------------------

    try:

        error_data = response.json()

        spotify_error = error_data.get(
            "error",
            "unknown_error"
        )

        description = error_data.get(
            "error_description",
            "Sin descripción."
        )

    except Exception:

        spotify_error = "unknown_error"

        description = (
            response.text[:500]
            if response.text
            else "Sin respuesta."
        )


    if response.status_code == 400:

        if spotify_error == "invalid_client":

            message = (
                "Spotify rechazó las credenciales. "
                "Revisa Client ID y Client Secret. "
                "Si el Secret fue expuesto, genera uno nuevo."
            )

        else:

            message = description

    elif response.status_code == 401:

        message = (
            "Spotify devolvió 401 Unauthorized. "
            "Las credenciales no fueron aceptadas."
        )

    elif response.status_code == 403:

        message = (
            "Spotify devolvió 403 Forbidden."
        )

    elif response.status_code == 429:

        message = (
            "Spotify está limitando las solicitudes "
            "(rate limit). Espera y prueba nuevamente."
        )

    else:

        message = description


    return {
        "ok": False,
        "token": None,
        "status":
            f"HTTP_{response.status_code}",
        "spotify_error":
            spotify_error,
        "message":
            message
    }


# ============================================================
# BUSCAR SPOTIFY
# ============================================================

def spotify_search(
    query: str,
    token: str
):

    headers = {
        "Authorization":
            f"Bearer {token}"
    }

    params = {
        "q": query,
        "type": "track",
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
            error = response.json()
        except Exception:
            error = {}

        return {
            "ok": False,
            "items": [],
            "status":
                response.status_code,
            "error":
                error
        }

    except Exception as e:

        return {
            "ok": False,
            "items": [],
            "status":
                "CONNECTION_ERROR",
            "error":
                str(e)
        }


# ============================================================
# APPLE MUSIC SEARCH
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
# URL ENCODER
# ============================================================

def encode(query: str):

    return urllib.parse.quote(
        query,
        safe=""
    )


# ============================================================
# PLATAFORMAS
# ============================================================

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
            f"https://www.instagram.com/explore/search/keyword/?q={q}",
    }


# ============================================================
# CENTRO DEL ARTISTA
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
    '<div class="house-infinity">∞</div>',
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


# ============================================================
# BUSCADOR
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔎 BUSCADOR GLOBAL'
    '</div>',
    unsafe_allow_html=True
)

query_input = st.text_input(
    "Artista, canción o álbum",
    value="Rabino Rap",
    placeholder="Ejemplo: Rabino Rap"
)


if "query" not in st.session_state:

    st.session_state.query = (
        query_input
    )


if st.button(
    "🚀 BUSCAR EN TODAS LAS PLATAFORMAS",
    use_container_width=True,
    type="primary"
):

    st.session_state.query = (
        query_input
    )


query = st.session_state.query


# ============================================================
# LINKS
# ============================================================

links = platform_links(
    query
)


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


# ============================================================
# SPOTIFY CONNECTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔌 SPOTIFY API'
    '</div>',
    unsafe_allow_html=True
)


spotify = get_spotify_token()


if spotify["ok"]:

    st.success(
        "🟢 SPOTIFY CONECTADO"
    )

    st.caption(
        "La aplicación consiguió un Access Token de Spotify."
    )

    spotify_token = spotify["token"]

else:

    spotify_token = None

    st.error(
        "🔴 SPOTIFY NO CONECTADO"
    )

    st.warning(
        f"Diagnóstico: {spotify['status']}"
    )

    st.write(
        spotify["message"]
    )

    if spotify.get("spotify_error"):

        st.code(
            spotify["spotify_error"],
            language="text"
        )

    st.info(
        "No se muestran tus credenciales. "
        "Revisa los Secrets de Streamlit."
    )


# ============================================================
# RESULTADOS SPOTIFY
# ============================================================

if spotify_token:

    result = spotify_search(
        query,
        spotify_token
    )

    if result["ok"]:

        tracks = result["items"]

        st.markdown(
            '<div class="section-title">'
            '🟢 RESULTADOS SPOTIFY'
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


            col_img, col_info = st.columns(
                [1, 4]
            )


            with col_img:

                if image:

                    st.image(
                        image,
                        use_container_width=True
                    )


            with col_info:

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
            "Spotify respondió con un error "
            f"({result.get('status')})."
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


items = list(
    ARTIST_TOOLS.items()
)


for start in range(
    0,
    len(items),
    3
):

    row = items[
        start:start + 3
    ]

    cols = st.columns(3)

    for col, item in zip(
        cols,
        row
    ):

        name, url = item

        with col:

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
        "## 🔐 Spotify"
    )


    status = spotify_secret_status()


    if status["client_id"]:

        st.success(
            "Client ID detectado"
        )

        st.caption(
            f"Longitud: "
            f"{status['client_id_length']}"
        )

    else:

        st.error(
            "Client ID NO detectado"
        )


    if status["client_secret"]:

        st.success(
            "Client Secret detectado"
        )

        st.caption(
            f"Longitud: "
            f"{status['client_secret_length']}"
        )

    else:

        st.error(
            "Client Secret NO detectado"
        )


    st.divider()


    if spotify["ok"]:

        st.success(
            "🟢 API FUNCIONANDO"
        )

    else:

        st.error(
            "🔴 API CON ERROR"
        )

        st.caption(
            spotify["status"]
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
