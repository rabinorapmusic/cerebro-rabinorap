import streamlit as st
import requests
import base64
import time

def get_secret(name, default=""):
    try:
        value = st.secrets.get(name, default)
        return str(value).strip() if value else default
    except Exception:
        return default

SPOTIFY_CLIENT_ID = get_secret("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = get_secret("SPOTIFY_CLIENT_SECRET")

TIKTOK_CLIENT_KEY = get_secret("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = get_secret("TIKTOK_CLIENT_SECRET")
TIKTOK_REDIRECT_URI = get_secret("TIKTOK_REDIRECT_URI")

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"

def spotify_token():
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        return None, "Faltan Secrets de Spotify."

    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    try:
        response = requests.post(
            SPOTIFY_TOKEN_URL,
            headers={
                "Authorization": f"Basic {encoded}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data={"grant_type": "client_credentials"},
            timeout=20
        )

        if response.status_code != 200:
            try:
                error = response.json()
            except Exception:
                error = response.text

            return None, f"Spotify {response.status_code}: {error}"

        data = response.json()
        token = data.get("access_token")

        if not token:
            return None, "Spotify no entregó access_token."

        return token, None

    except requests.RequestException as e:
        return None, f"Spotify conexión: {e}"

def spotify_search(query, search_type="artist"):
    token, error = spotify_token()

    if error:
        return None, error

    try:
        response = requests.get(
            f"{SPOTIFY_API_URL}/search",
            headers={
                "Authorization": f"Bearer {token}"
            },
            params={
                "q": query,
                "type": search_type,
                "limit": 10,
                "market": "DO"
            },
            timeout=20
        )

        if response.status_code != 200:
            try:
                data = response.json()
            except Exception:
                data = response.text

            return None, f"Spotify {response.status_code}: {data}"

        return response.json(), None

    except requests.RequestException as e:
        return None, f"Spotify conexión: {e}"

spotify, spotify_error = spotify_token()

if spotify:
    st.success("🟢 SPOTIFY ONLINE")
else:
    st.error(f"🔴 SPOTIFY: {spotify_error}")

st.title("STREAMING HOUSE ∞")
