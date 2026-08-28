import streamlit as st
import os
import textwrap


# ============================================================
# STREAMING HOUSE
# RABINO RAP
# ARTIST DIGITAL COMMAND CENTER
# ============================================================

st.set_page_config(
    page_title="STREAMING HOUSE | RABINO RAP",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

ARTIST_NAME = "RABINO RAP"
ARTIST_TAG = "ARTIST • MUSIC • DIGITAL EMPIRE"

IMAGE_FILES = [
    "foto_artista.jpg",
    "foto_artista.jpeg",
    "foto_artista.png",
    "rabino_rap.jpg",
    "rabino_rap.png"
]


# ============================================================
# BUSCAR FOTO
# ============================================================

def buscar_foto():

    for archivo in IMAGE_FILES:

        if os.path.exists(archivo):
            return archivo

    return None


ARTIST_IMAGE = buscar_foto()


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800&display=swap'
);


/* =========================================================
   GENERAL
========================================================= */

html, body, [class*="css"] {

    font-family: 'Poppins', sans-serif;

}

.stApp {

    min-height: 100vh;

    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(0,255,255,0.25),
            transparent 24%
        ),

        radial-gradient(
            circle at 95% 5%,
            rgba(255,0,170,0.25),
            transparent 25%
        ),

        radial-gradient(
            circle at 50% 50%,
            rgba(120,0,255,0.14),
            transparent 35%
        ),

        radial-gradient(
            circle at 80% 95%,
            rgba(0,255,130,0.15),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            #02030a 0%,
            #080014 40%,
            #001018 70%,
            #050008 100%
        );

    background-attachment: fixed;

    color: white;

}


/* =========================================================
   GRID
========================================================= */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    opacity: 0.12;

    background-image:

        linear-gradient(
            rgba(0,255,255,0.25) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,0,180,0.20) 1px,
            transparent 1px
        );

    background-size: 55px 55px;

}


/* =========================================================
   OCULTAR STREAMLIT
========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* =========================================================
   LOGO
========================================================= */

.logo {

    text-align: center;

    font-family: 'Orbitron', sans-serif;

    font-size: clamp(
        35px,
        7vw,
        78px
    );

    font-weight: 900;

    letter-spacing: 6px;

    margin-top: 15px;

    background:

        linear-gradient(
            90deg,
            #00ffff,
            #00ff88,
            #ffffff,
            #ff00cc,
            #9b00ff,
            #00ffff
        );

    background-size: 400% 100%;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation: logoAnimation 8s linear infinite;

    filter:
        drop-shadow(
            0 0 15px
            rgba(0,255,255,0.5)
        );

}


@keyframes logoAnimation {

    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }

}


.subtitle {

    text-align: center;

    color: #aeb9ca;

    font-size: 12px;

    letter-spacing: 5px;

    margin-bottom: 35px;

}


/* =========================================================
   HERO
========================================================= */

.hero {

    position: relative;

    overflow: hidden;

    padding: 40px;

    border-radius: 35px;

    background:

        linear-gradient(
            135deg,
            rgba(0,255,255,0.13),
            rgba(100,0,255,0.15),
            rgba(255,0,150,0.12)
        );

    border:
        1px solid
        rgba(255,255,255,0.16);

    box-shadow:

        0 0 60px
        rgba(0,255,255,0.08),

        inset 0 0 70px
        rgba(255,255,255,0.025);

    backdrop-filter: blur(20px);

}


/* =========================================================
   FOTO
========================================================= */

.artist-photo {

    width: 230px;

    height: 230px;

    object-fit: cover;

    border-radius: 50%;

    border:
        4px solid
        #00ffff;

    box-shadow:

        0 0 15px #00ffff,

        0 0 40px
        rgba(0,255,255,0.55),

        0 0 90px
        rgba(255,0,180,0.25);

}


/* =========================================================
   PLACEHOLDER FOTO
========================================================= */

.photo-placeholder {

    width: 230px;

    height: 230px;

    margin: auto;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 85px;

    background:

        linear-gradient(
            135deg,
            #00ffff,
            #7200ff,
            #ff0088
        );

    border:
        4px solid
        #ffffff;

    box-shadow:

        0 0 20px #00ffff,

        0 0 50px
        rgba(255,0,150,0.4);

}


/* =========================================================
   ARTIST NAME
========================================================= */

.artist-name {

    font-family: 'Orbitron', sans-serif;

    font-size: clamp(
        30px,
        5vw,
        58px
    );

    font-weight: 900;

    letter-spacing: 4px;

    text-shadow:

        0 0 10px
        rgba(0,255,255,0.8),

        0 0 30px
        rgba(0,255,255,0.4);

}


/* =========================================================
   LIVE
========================================================= */

.live {

    display: inline-block;

    padding:
        8px 15px;

    border-radius: 50px;

    color: #00ffb3;

    background:
        rgba(0,255,150,0.08);

    border:
        1px solid
        rgba(0,255,150,0.35);

    font-size: 11px;

    letter-spacing: 2px;

    box-shadow:
        0 0 18px
        rgba(0,255,150,0.18);

}


/* =========================================================
   SECCIONES
========================================================= */

.section-title {

    font-family: 'Orbitron', sans-serif;

    font-size: 25px;

    font-weight: 800;

    letter-spacing: 3px;

    margin-top: 42px;

    margin-bottom: 22px;

    text-shadow:
        0 0 15px
        rgba(0,255,255,0.45);

}


/* =========================================================
   PLATFORM CARD
========================================================= */

.platform-card {

    min-height: 225px;

    padding: 25px;

    margin-bottom: 20px;

    border-radius: 25px;

    background:
        rgba(255,255,255,0.055);

    border:
        1px solid
        rgba(255,255,255,0.13);

    backdrop-filter:
        blur(18px);

    box-shadow:

        0 10px 30px
        rgba(0,0,0,0.35);

    transition:
        transform 0.25s ease,
        border 0.25s ease,
        box-shadow 0.25s ease;

}


.platform-card:hover {

    transform:
        translateY(-7px);

    border-color:
        rgba(0,255,255,0.65);

    box-shadow:

        0 15px 45px
        rgba(0,255,255,0.15),

        0 0 25px
        rgba(255,0,180,0.08);

}


/* =========================================================
   ICON
========================================================= */

.platform-icon {

    font-size: 46px;

    line-height: 1;

    margin-bottom: 14px;

}


/* =========================================================
   PLATFORM TITLE
========================================================= */

.platform-title {

    font-family: 'Orbitron', sans-serif;

    font-size: 17px;

    font-weight: 800;

    letter-spacing: 1px;

    color: white;

}


/* =========================================================
   DESCRIPTION
========================================================= */

.platform-description {

    color: #9da9b8;

    font-size: 12px;

    line-height: 1.6;

    min-height: 38px;

    margin-top: 7px;

    margin-bottom: 17px;

}


/* =========================================================
   BUTTON
========================================================= */

.neon-button {

    display: block;

    width: 100%;

    padding: 13px;

    text-align: center;

    text-decoration: none !important;

    color: white !important;

    border-radius: 13px;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1px;

    background:

        linear-gradient(
            90deg,
            rgba(0,255,255,0.13),
            rgba(130,0,255,0.17),
            rgba(255,0,150,0.12)
        );

    border:
        1px solid
        rgba(255,255,255,0.16);

    transition:
        all 0.25s ease;

}


.neon-button:hover {

    color: #00ffff !important;

    border-color:
        #00ffff;

    box-shadow:

        0 0 20px
        rgba(0,255,255,0.35);

    transform:
        translateY(-2px);

}


/* =========================================================
   COLORES DE PLATAFORMAS
========================================================= */

.spotify {

    box-shadow:
        inset 0 0 40px
        rgba(30,215,96,0.08);

}

.apple {

    box-shadow:
        inset 0 0 40px
        rgba(255,255,255,0.07);

}

.youtube {

    box-shadow:
        inset 0 0 40px
        rgba(255,0,0,0.09);

}

.tiktok {

    box-shadow:
        inset 0 0 40px
        rgba(0,242,234,0.09);

}

.instagram {

    box-shadow:
        inset 0 0 40px
        rgba(255,0,128,0.10);

}

.distrokid {

    box-shadow:
        inset 0 0 40px
        rgba(0,255,150,0.08);

}

.amazon {

    box-shadow:
        inset 0 0 40px
        rgba(255,160,0,0.08);

}


/* =========================================================
   ARTIST LAB
========================================================= */

.lab {

    padding: 30px;

    border-radius: 28px;

    background:

        linear-gradient(
            135deg,
            rgba(0,255,255,0.07),
            rgba(120,0,255,0.09),
            rgba(255,0,160,0.07)
        );

    border:
        1px solid
        rgba(255,255,255,0.13);

    box-shadow:
        0 15px 45px
        rgba(0,0,0,0.25);

}


/* =========================================================
   FOOTER
========================================================= */

.footer {

    text-align: center;

    padding:
        55px 10px 25px;

    color: #697586;

    font-size: 11px;

    letter-spacing: 3px;

}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 768px) {

    .logo {

        font-size: 36px;

        letter-spacing: 3px;

    }

    .subtitle {

        font-size: 9px;

        letter-spacing: 3px;

    }

    .hero {

        padding: 25px 18px;

        border-radius: 25px;

    }

    .artist-name {

        font-size: 30px;

        text-align: center;

        margin-top: 20px;

    }

    .platform-card {

        min-height: auto;

    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# FUNCIÓN DE TARJETA
# ============================================================

def platform_card(
    css_class,
    icon,
    title,
    description,
    url
):

    html = f"""
<div class="platform-card {css_class}">

    <div class="platform-icon">
        {icon}
    </div>

    <div class="platform-title">
        {title}
    </div>

    <div class="platform-description">
        {description}
    </div>

    <a
        class="neon-button"
        href="{url}"
        target="_blank"
        rel="noopener noreferrer"
    >
        OPEN PLATFORM →
    </a>

</div>
"""

    # IMPORTANTE:
    # dedent elimina la indentación que hacía
    # que Streamlit mostrara el HTML como código.
    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="logo">
    STREAMING HOUSE
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="subtitle">
    THE DIGITAL COMMAND CENTER FOR ARTISTS
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero">',
    unsafe_allow_html=True
)

hero1, hero2 = st.columns(
    [1, 2],
    vertical_alignment="center"
)


with hero1:

    if ARTIST_IMAGE:

        st.markdown(
            f"""
<img
    src="data:image/jpeg;base64,"
    class="artist-photo"
>
""",
            unsafe_allow_html=True
        )

        # Streamlit maneja la imagen de forma segura
        st.image(
            ARTIST_IMAGE,
            width=230
        )

    else:

        st.markdown(
            """
<div class="photo-placeholder">
    🎤
</div>
""",
            unsafe_allow_html=True
        )


with hero2:

    st.markdown(
        """
<span class="live">
    ● SYSTEM ONLINE
</span>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
<div class="artist-name">
    {ARTIST_NAME}
</div>

<div style="
    color:#a9b4c4;
    letter-spacing:3px;
    font-size:12px;
    margin-top:8px;
">
    {ARTIST_TAG}
</div>

<p style="
    color:#d5dce5;
    line-height:1.8;
    max-width:700px;
    margin-top:20px;
">
    Welcome to your digital music command center.
    Manage your streaming platforms, social media,
    distribution, releases and creative tools
    from one place.
</p>
""",
        unsafe_allow_html=True
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# STREAMING
# ============================================================

st.markdown(
    """
<div class="section-title">
    🎧 STREAMING UNIVERSE
</div>
""",
    unsafe_allow_html=True
)


c1, c2, c3 = st.columns(3)


with c1:

    platform_card(
        "spotify",
        "🟢",
        "SPOTIFY",
        "Spotify for Artists, profile and music analytics.",
        "https://artists.spotify.com/"
    )


with c2:

    platform_card(
        "apple",
        "🍎",
        "APPLE MUSIC",
        "Manage your Apple Music artist presence.",
        "https://artists.apple.com/"
    )


with c3:

    platform_card(
        "youtube",
        "▶️",
        "YOUTUBE",
        "YouTube Studio, videos and creator tools.",
        "https://studio.youtube.com/"
    )


c4, c5, c6 = st.columns(3)


with c4:

    platform_card(
        "tiktok",
        "🎵",
        "TIKTOK",
        "Music discovery and creator platform.",
        "https://www.tiktok.com/"
    )


with c5:

    platform_card(
        "youtube",
        "🎶",
        "YOUTUBE MUSIC",
        "Music streaming and artist discovery.",
        "https://music.youtube.com/"
    )


with c6:

    platform_card(
        "amazon",
        "🟠",
        "AMAZON MUSIC",
        "Amazon Music for Artists.",
        "https://artists.amazonmusic.com/"
    )


# ============================================================
# SOCIAL MEDIA
# ============================================================

st.markdown(
    """
<div class="section-title">
    📱 SOCIAL COMMAND
</div>
""",
    unsafe_allow_html=True
)


s1, s2, s3 = st.columns(3)


with s1:

    platform_card(
        "instagram",
        "📸",
        "INSTAGRAM",
        "Build your artist community and reach.",
        "https://www.instagram.com/Rabino_rap_oficial/"
    )


with s2:

    platform_card(
        "tiktok",
        "🎵",
        "TIKTOK",
        "Create viral short-form music content.",
        "https://www.tiktok.com/"
    )


with s3:

    platform_card(
        "youtube",
        "▶️",
        "YOUTUBE CHANNEL",
        "Videos, Shorts and your artist channel.",
        "https://www.youtube.com/"
    )


# ============================================================
# DISTRIBUTION
# ============================================================

st.markdown(
    """
<div class="section-title">
    💿 DISTRIBUTION HQ
</div>
""",
    unsafe_allow_html=True
)


d1, d2, d3 = st.columns(3)


with d1:

    platform_card(
        "distrokid",
        "🚀",
        "DISTROKID",
        "Distribute your music to digital stores.",
        "https://distrokid.com/"
    )


with d2:

    platform_card(
        "spotify",
        "💰",
        "ROYALTIES",
        "Music rights and royalty resources.",
        "https://www.ascap.com/"
    )


with d3:

    platform_card(
        "apple",
        "🎼",
        "MUSIC RIGHTS",
        "Music industry rights resources.",
        "https://www.bmi.com/"
    )


# ============================================================
# ARTIST LAB
# ============================================================

st.markdown(
    """
<div class="section-title">
    🎨 ARTIST LAB
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    '<div class="lab">',
    unsafe_allow_html=True
)


lab1, lab2, lab3 = st.columns(3)


# ============================================================
# LYRIC LAB
# ============================================================

with lab1:

    st.markdown("### ✍️ LYRIC LAB")

    lyrics = st.text_area(
        "Lyrics",
        placeholder="Write your next song...",
        height=180,
        label_visibility="collapsed"
    )

    if st.button(
        "💾 SAVE LYRICS",
        use_container_width=True
    ):

        if
