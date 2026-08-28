import streamlit as st
import requests
import base64
import time

def get_secret(name, default=""):
    try:
        value = st.secrets.get(name)
        if value is not None:
            return str(value).strip()
    except Exception:
        pass
    return default

SPOTIFY_CLIENT_ID = get_secret("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = get_secret("SPOTIFY_CLIENT_SECRET")

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

if "spotify_token" not in st.session_state:
    st.session_state.spotify_token = None

if "spotify_expiry" not in st.session_state:
    st.session_state.spotify_expiry = 0

def spotify_get_token():

    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None, "Faltan SPOTIFY_CLIENT_ID o SPOTIFY_CLIENT_SECRET."

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
                f"Spotify HTTP {response.status_code}: {data}"
            )

        data = response.json()

        token = data.get("access_token")

        if not token:
            return None, "Spotify no devolvió access_token."

        expires = int(
            data.get("expires_in", 3600)
        )

        st.session_state.spotify_token = token

        st.session_state.spotify_expiry = (
            time.time() + expires - 60
        )

        return token, None

    except requests.RequestException as error:

        return None, f"Spotify conexión: {error}"

def spotify_request(endpoint, params=None):

    token, error = spotify_get_token()

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

            token, error = spotify_get_token()

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
                f"Spotify HTTP {response.status_code}: {data}"
            )

        return response.json(), None

    except requests.RequestException as error:

        return None, f"Spotify conexión: {error}"

def spotify_search(query, search_type="artist"):

    return spotify_request(
        "/search",
        {
            "q": query,
            "type": search_type,
            "limit": 10,
            "market": "DO"
        }
        )
