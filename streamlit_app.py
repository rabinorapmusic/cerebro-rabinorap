import streamlit as st
import os

# ============================================================
# 🎵 STREAMING HOUSE
# RABINO RAP — ARTIST DIGITAL HQ
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
ARTIST_IMAGE = "foto_artista.jpg"


# ============================================================
# CSS — NEON DIGITAL HOUSE
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800&display=swap');

* {
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 10% 15%,
            rgba(0,255,255,.18),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(255,0,140,.20),
            transparent 27%
        ),
        radial-gradient(
            circle at 50% 85%,
            rgba(130,0,255,.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #03030a,
            #090014,
            #020b12,
            #050009
        );

    background-attachment: fixed;
    color: white;
}

/* ============================================================
   OCULTAR ELEMENTOS STREAMLIT
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ============================================================
   GRID DIGITAL
   ============================================================ */

.stApp:before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    opacity: .15;

    background-image:
        linear-gradient(
            rgba(0,255,255,.08) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(0,255,255,.08) 1px,
            transparent 1px
        );

    background-size: 50px 50px;

    mask-image: linear-gradient(
        to bottom,
        black,
        transparent
    );

}


/* ============================================================
   LOGO
   ============================================================ */

.logo {

    text-align: center;

    font-family: 'Orbitron', sans-serif;

    font-size: clamp(
        38px,
        7vw,
        78px
    );

    font-weight: 900;

    letter-spacing: 7px;

    margin-top: 10px;

    background:
        linear-gradient(
            90deg,
            #00ffff,
            #00ff88,
            #ffffff,
            #ff00aa,
            #9b00ff,
            #00ffff
        );

    background-size: 400%;

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    animation:
        logoMove 8s linear infinite;

    filter:
        drop-shadow(
            0 0 18px
            rgba(0,255,255,.5)
        );
}

@keyframes logoMove {

    0% {
        background-position: 0%;
    }

    50% {
        background-position: 100%;
    }

    100% {
        background-position: 0%;
    }

}


/* ============================================================
   SUBTÍTULO
   ============================================================ */

.subtitle {

    text-align: center;

    color: #b8c7d9;

    letter-spacing: 5px;

    font-size: 12px;

    margin-bottom: 30px;

}


/* ============================================================
   ARTIST HERO
   ============================================================ */

.hero {

    position: relative;

    padding: 40px;

    border-radius: 35px;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            rgba(0,255,255,.12),
            rgba(150,0,255,.14),
            rgba(255,0,130,.10)
        );

    border:
        1px solid
        rgba(255,255,255,.18);

    box-shadow:
        0 0 50px
        rgba(0,255,255,.08),

        inset 0 0 60px
        rgba(255,255,255,.025);

    backdrop-filter:
        blur(20px);

}


/* ============================================================
   ARTIST PHOTO
   ============================================================ */

.artist-photo {

    width: 240px;

    height: 240px;

    object-fit: cover;

    border-radius: 50%;

    border:
        4px solid
        #00ffff;

    box-shadow:

        0 0 15px #00ffff,
        0 0 35px rgba(0,255,255,.6),
        0 0 80px rgba(255,0,180,.25);

}


/* ============================================================
   ARTIST NAME
   ============================================================ */

.artist-name {

    font-family:
        'Orbitron',
        sans-serif;

    font-size:
        clamp(
            30px,
            5vw,
            55px
        );

    font-weight: 900;

    letter-spacing: 4px;

    color: white;

    text-shadow:

        0 0 8px #00ffff,
        0 0 25px rgba(0,255,255,.7);

}


/* ============================================================
   LIVE BADGE
   ============================================================ */

.live {

    display: inline-block;

    padding:
        8px 15px;

    border-radius: 50px;

    color: #00ffb3;

    background:
        rgba(0,255,150,.08);

    border:
        1px solid
        rgba(0,255,150,.35);

    font-size: 11px;

    letter-spacing: 2px;

    box-shadow:
        0 0 15px
        rgba(0,255,150,.15);

}


/* ============================================================
   SECTION TITLES
   ============================================================ */

.section {

    font-family:
        'Orbitron',
        sans-serif;

    font-size: 25px;

    font-weight: 700;

    letter-spacing: 3px;

    margin:
        35px 0 20px;

    color: white;

    text-shadow:
        0 0 15px
        rgba(0,255,255,.45);

}


/* ============================================================
   PLATFORM CARDS
   ============================================================ */

.platform-card {

    min-height: 145px;

    padding: 25px;

    border-radius: 25px;

    background:
        rgba(255,255,255,.045);

    border:
        1px solid
        rgba(255,255,255,.12);

    transition:
        all .3s ease;

    margin-bottom: 20px;

    backdrop-filter:
        blur(15px);

}

.platform-card:hover {

    transform:
        translateY(-6px)
        scale(1.015);

    border-color:
        rgba(0,255,255,.65);

    box-shadow:

        0 10px 35px
        rgba(0,255,255,.12);

}


/* ============================================================
   PLATFORM ICON
   ============================================================ */

.platform-icon {

    font-size: 42px;

    margin-bottom: 8px;

}


/* ============================================================
   PLATFORM TITLE
   ============================================================ */

.platform-title {

    font-family:
        'Orbitron',
        sans-serif;

    font-weight: 700;

    font-size: 17px;

    letter-spacing: 1px;

}


/* ============================================================
   PLATFORM DESCRIPTION
   ============================================================ */

.platform-description {

    color: #8e9aaa;

    font-size: 11px;

    margin:
        5px 0 15px;

}


/* ============================================================
   LINK BUTTON
   ============================================================ */

a.neon-button {

    display: block;

    text-align: center;

    padding: 12px;

    border-radius: 12px;

    text-decoration: none !important;

    color: white !important;

    font-weight: 700;

    font-size: 12px;

    letter-spacing: 1px;

    background:
        linear-gradient(
            90deg,
            rgba(0,255,255,.13),
            rgba(150,0,255,.15)
        );

    border:
        1px solid
        rgba(255,255,255,.13);

    transition:
        all .25s ease;

}

a.neon-button:hover {

    color: #00ffff !important;

    border-color:
        #00ffff;

    box-shadow:
        0 0 18px
        rgba(0,255,255,.35);

    transform:
        translateY(-2px);

}


/* ============================================================
   COLORES ESPECIALES
   ============================================================ */

.spotify {
    box-shadow:
        inset 0 0 30px
        rgba(30,215,96,.08);
}

.apple {
    box-shadow:
        inset 0 0 30px
        rgba(255,255,255,.06);
}

.tiktok {
    box-shadow:
        inset 0 0 30px
        rgba(0,242,234,.08);
}

.instagram {
    box-shadow:
        inset 0 0 30px
        rgba(255,0,128,.10);
}

.youtube {
    box-shadow:
        inset 0 0 30px
        rgba(255,0,0,.09);
}

.distrokid {
    box-shadow:
        inset 0 0 30px
        rgba(0,255,170,.08);
}


/* ============================================================
   TOOL BOX
   ============================================================ */

.tool-box {

    padding: 30px;

    border-radius: 25px;

    background:
        linear-gradient(
            135deg,
            rgba(255,0,150,.08),
            rgba(120,0,255,.08),
            rgba(0,255,255,.06)
        );

    border:
        1px solid
        rgba(255,255,255,.12);

}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    text-align: center;

    margin-top: 70px;

    padding: 35px;

    color: #697383;

    font-size: 11px;

    letter-spacing: 3px;

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES
# ============================================================

def platform(
    css_class,
    icon,
    title,
    description,
    url
):

    st.markdown(
        f"""
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
            >
                OPEN PLATFORM →
            </a>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="logo">STREAMING HOUSE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'THE DIGITAL COMMAND CENTER FOR ARTISTS'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero">',
    unsafe_allow_html=True
)

hero_left, hero_right = st.columns(
    [1, 2],
    vertical_alignment="center"
)


with hero_left:

    if os.path.exists(ARTIST_IMAGE):

        st.image(
            ARTIST_IMAGE,
            width=240
        )

    else:

        st.markdown(
            """
            <div class="artist-photo"
                 style="
                 display:flex;
                 align-items:center;
                 justify-content:center;
                 font-size:80px;
                 background:
                 linear-gradient(
                    135deg,
                    #00ffff,
                    #8a00ff,
                    #ff0088
                 );
                 ">
                🎤
            </div>
            """,
            unsafe_allow_html=True
        )


with hero_right:

    st.markdown(
        '<span class="live">● SYSTEM ONLINE</span>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="artist-name">
            {ARTIST_NAME}
        </div>

        <p style="
            color:#9ca8b8;
            letter-spacing:3px;
            font-size:13px;
        ">
            {ARTIST_TAG}
        </p>

        <p style="
            color:#d1d8e0;
            line-height:1.8;
        ">
            One place to manage your music,
            distribution, social platforms,
            artist tools and digital presence.
        </p>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# STREAMING
# ============================================================

st.markdown(
    '<div class="section">🎧 STREAMING UNIVERSE</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    platform(
        "spotify",
        "🟢",
        "SPOTIFY",
        "Artist profile, music and analytics.",
        "https://artists.spotify.com/"
    )

with c2:

    platform(
        "apple",
        "🍎",
        "APPLE MUSIC",
        "Artist profile and music management.",
        "https://artists.apple.com/"
    )

with c3:

    platform(
        "youtube",
        "▶️",
        "YOUTUBE",
        "Video, music and creator studio.",
        "https://studio.youtube.com/"
    )

c4, c5, c6 = st.columns(3)

with c4:

    platform(
        "tiktok",
        "🎵",
        "TIKTOK",
        "Music discovery and artist presence.",
        "https://www.tiktok.com/"
    )

with c5:

    platform(
        "youtube",
        "🎶",
        "YOUTUBE MUSIC",
        "Music streaming platform.",
        "https://music.youtube.com/"
    )

with c6:

    platform(
        "spotify",
        "🟠",
        "AMAZON MUSIC",
        "Music streaming and artist tools.",
        "https://artists.amazonmusic.com/"
    )


# ============================================================
# SOCIAL
# ============================================================

st.markdown(
    '<div class="section">📱 SOCIAL COMMAND</div>',
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3)

with s1:

    platform(
        "instagram",
        "📸",
        "INSTAGRAM",
        "Build your artist community.",
        "https://www.instagram.com/"
    )

with s2:

    platform(
        "tiktok",
        "🎵",
        "TIKTOK",
        "Short-form music discovery.",
        "https://www.tiktok.com/"
    )

with s3:

    platform(
        "youtube",
        "▶️",
        "YOUTUBE",
        "Videos, Shorts and music.",
        "https://www.youtube.com/"
    )


# ============================================================
# DISTRIBUTION
# ============================================================

st.markdown(
    '<div class="section">💿 DISTRIBUTION HQ</div>',
    unsafe_allow_html=True
)

d1, d2, d3 = st.columns(3)

with d1:

    platform(
        "distrokid",
        "🚀",
        "DISTROKID",
        "Distribute music to digital stores.",
        "https://distrokid.com/"
    )

with d2:

    platform(
        "spotify",
        "💰",
        "ROYALTIES",
        "Artist rights and royalty resources.",
        "https://www.ascap.com/"
    )

with d3:

    platform(
        "apple",
        "🎼",
        "MUSIC RIGHTS",
        "Music industry rights resources.",
        "https://www.bmi.com/"
    )


# ============================================================
# ARTIST TOOLS
# ============================================================

st.markdown(
    '<div class="section">🎨 ARTIST LAB</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tool-box">',
    unsafe_allow_html=True
)

t1, t2, t3 = st.columns(3)


with t1:

    st.markdown("### ✍️ LYRIC LAB")

    lyrics = st.text_area(
        "Write your lyrics",
        placeholder="Start your next song...",
        height=180,
        label_visibility="collapsed"
    )

    if st.button(
        "SAVE LYRICS",
        key="lyrics"
    ):

        if lyrics.strip():

            with open(
                "lyrics.txt",
                "w",
                encoding="utf-8"
            ) as file:

                file.write(lyrics)

            st.success(
                "Lyrics saved."
            )

        else:

            st.warning(
                "Write something first."
            )


with t2:

    st.markdown("### 🎤 SONG IDEA")

    idea = st.text_input(
        "Song idea",
        placeholder="Example: street faith",
        label_visibility="collapsed"
    )

    genre = st.selectbox(
        "Genre",
        [
            "Dembow",
            "Hip Hop",
            "Trap",
            "Afrobeat",
            "Reggaeton",
            "Christian Rap"
        ]
    )

    if st.button(
        "GENERATE IDEA",
        key="idea"
    ):

        if idea:

            st.success(
                f"""
                {ARTIST_NAME} — {genre}

                Theme:
                {idea}

                Structure:
                INTRO → VERSE → CHORUS →
                VERSE → CHORUS → OUTRO
                """
            )

        else:

            st.warning(
                "Enter a song concept."
            )


with t3:

    st.markdown("### 🤖 MUSIC PROMPT")

    prompt = st.text_input(
        "Prompt",
        placeholder="Example: Dominican urban anthem",
        label_visibility="collapsed"
    )

    bpm = st.slider(
        "BPM",
        70,
        180,
        105
    )

    if st.button(
        "CREATE PROMPT",
        key="prompt"
    ):

        if prompt:

            final_prompt = f"""
{genre} production for {ARTIST_NAME}.

Concept:
{prompt}

Tempo:
{bpm} BPM

Style:
Modern, powerful, atmospheric,
deep bass, punchy drums,
professional commercial production,
strong memorable hook,
dynamic arrangement.

Structure:
Intro → Verse → Chorus →
Verse → Chorus → Bridge → Outro.
"""

            st.code(
                final_prompt,
                language="text"
            )

        else:

            st.warning(
                "Enter a concept."
            )

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ARTIST PROFILE
# ============================================================

st.markdown(
    '<div class="section">🌐 ARTIST PRESENCE</div>',
    unsafe_allow_html=True
)

p1, p2, p3, p4 = st.columns(4)

with p1:

    platform_button = """
    <a class="neon-button"
       href="https://www.instagram.com/Rabino_rap_oficial/"
       target="_blank">
       📸 INSTAGRAM
    </a>
    """

    st.markdown(
        platform_button,
        unsafe_allow_html=True
    )

with p2:

    st.markdown(
        """
        <a class="neon-button"
           href="https://open.spotify.com/"
           target="_blank">
           🟢 SPOTIFY
        </a>
        """,
        unsafe_allow_html=True
    )

with p3:

    st.markdown(
        """
        <a class="neon-button"
           href="https://www.youtube.com/"
           target="_blank">
           ▶️ YOUTUBE
        </a>
        """,
        unsafe_allow_html=True
    )

with p4:

    st.markdown(
        """
        <a class="neon-button"
           href="https://www.tiktok.com/"
           target="_blank">
           🎵 TIKTOK
        </a>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        STREAMING HOUSE ∞

        <br><br>

        RABINO RAP • DIGITAL MUSIC COMMAND CENTER

        <br>

        MUSIC • DISTRIBUTION • SOCIAL • CREATION

    </div>
    """,
    unsafe_allow_html=True
)
