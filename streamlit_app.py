import streamlit as st
import sqlite3
from datetime import date
import pandas as pd

# ============================================================
# 🏠 STREAMING HOUSE
# MUSIC • DISTRIBUTION • ARTIST CONTROL CENTER
# RABINO RAP
#
# TODO EN UN SOLO ARCHIVO
# BASE DE DATOS SQLITE
# ============================================================

st.set_page_config(
    page_title="STREAMING HOUSE",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CONFIGURACIÓN
# ============================================================

DB_FILE = "streaming_house.db"

# ============================================================
# 🔗 ENLACES
# ============================================================

LINKS = {
    "spotify": "https://open.spotify.com/artist/7tVOfmt8UiTuwhATzPrdhA",
    "youtube": "https://youtube.com/@rabinorap",
    "tiktok": "https://www.tiktok.com/@rabinorap",
    "instagram": "https://www.instagram.com/rabino_rap_oficial/",

    "youtube_music": "https://music.youtube.com/",
    "apple": "https://music.apple.com/",
    "amazon": "https://music.amazon.com/",
    "deezer": "https://www.deezer.com/",
    "tidal": "https://tidal.com/",
    "pandora": "https://www.pandora.com/",
    "itunes": "https://www.apple.com/la/itunes/",
    "soundcloud": "https://soundcloud.com/",
    "audiomack": "https://audiomack.com/",
    "beatport": "https://www.beatport.com/",

    "distrokid": "https://distrokid.com/",
    "spotify_artists": "https://artists.spotify.com/",
    "apple_artists": "https://artists.apple.com/",
}

# ============================================================
# 💾 BASE DE DATOS
# ============================================================

def conectar():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def iniciar_db():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS canciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            proyecto TEXT,
            genero TEXT,
            fecha TEXT,
            estado TEXT,
            enlace TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS lanzamientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            fecha TEXT,
            genero TEXT,
            estado TEXT,
            notas TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS estadisticas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            plataforma TEXT,
            cancion TEXT,
            reproducciones INTEGER,
            seguidores INTEGER,
            notas TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS regalias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            plataforma TEXT,
            periodo TEXT,
            reproducciones INTEGER,
            ingresos REAL,
            moneda TEXT,
            notas TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS promociones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            campana TEXT,
            plataforma TEXT,
            presupuesto REAL,
            estado TEXT,
            resultado TEXT,
            notas TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS perfil (
            id INTEGER PRIMARY KEY,
            instagram TEXT,
            spotify TEXT,
            youtube TEXT,
            tiktok TEXT
        )
    """)

    cur.execute("""
        INSERT OR IGNORE INTO perfil
        (id, instagram, spotify, youtube, tiktok)
        VALUES (1, ?, ?, ?, ?)
    """, (
        LINKS["instagram"],
        LINKS["spotify"],
        LINKS["youtube"],
        LINKS["tiktok"]
    ))

    conn.commit()
    conn.close()


iniciar_db()

# ============================================================
# FUNCIONES DB
# ============================================================

def ejecutar(sql, parametros=()):

    conn = conectar()
    cur = conn.cursor()

    cur.execute(sql, parametros)

    conn.commit()
    conn.close()


def consultar(sql, parametros=()):

    conn = conectar()

    df = pd.read_sql_query(
        sql,
        conn,
        params=parametros
    )

    conn.close()

    return df


# ============================================================
# 🎨 DISEÑO
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 5%, #172554 0%, transparent 30%),
        radial-gradient(circle at 90% 95%, #581c87 0%, transparent 30%),
        linear-gradient(135deg, #020617, #050505 55%, #0f172a);
    color: white;
}

.block-container {
    max-width: 1250px;
    padding-top: 25px;
    padding-bottom: 60px;
}

.hero {
    text-align: center;
    padding: 50px 20px;
    border-radius: 28px;
    background: linear-gradient(
        135deg,
        rgba(15,23,42,.98),
        rgba(49,16,65,.95)
    );
    border: 1px solid rgba(255,255,255,.12);
    box-shadow: 0 0 45px rgba(124,58,237,.20);
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 50px;
    font-weight: 900;
    letter-spacing: 4px;
    margin: 0;
}

.hero p {
    color: #b8b8c8;
    letter-spacing: 3px;
}

.artist {
    padding: 25px;
    border-radius: 22px;
    background: rgba(255,255,255,.05);
    border: 1px solid rgba(255,255,255,.10);
    margin-bottom: 25px;
}

.artist h2 {
    margin: 0;
    font-size: 32px;
}

.section {
    font-size: 28px;
    font-weight: 900;
    margin-top: 35px;
    margin-bottom: 20px;
}

.card {
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,255,255,.10);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 12px;
    min-height: 140px;
}

.card h3 {
    margin-bottom: 8px;
}

.card p {
    color: #aaa;
}

.footer {
    text-align: center;
    color: #777;
    margin-top: 60px;
    padding: 30px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# 🏠 HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <h1>🏠 STREAMING HOUSE</h1>
    <p>MUSIC • DISTRIBUTION • ARTIST CONTROL CENTER</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="artist">
    <h2>🎤 RABINO RAP</h2>
    <p>ARTISTA • RAP • HIP HOP • DEMBOW • MÚSICA URBANA</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 📊 RESUMEN GENERAL
# ============================================================

canciones_total = consultar(
    "SELECT COUNT(*) AS total FROM canciones"
)["total"][0]

lanzamientos_total = consultar(
    "SELECT COUNT(*) AS total FROM lanzamientos"
)["total"][0]

reproducciones_total = consultar(
    "SELECT COALESCE(SUM(reproducciones),0) AS total FROM estadisticas"
)["total"][0]

regalias_total = consultar(
    "SELECT COALESCE(SUM(ingresos),0) AS total FROM regalias"
)["total"][0]

campanas_total = consultar(
    "SELECT COUNT(*) AS total FROM promociones"
)["total"][0]

st.markdown(
    '<div class="section">📊 RESUMEN DEL ARTISTA</div>',
    unsafe_allow_html=True
)

a, b, c, d, e = st.columns(5)

a.metric("🎵 CANCIONES", canciones_total)
b.metric("🚀 LANZAMIENTOS", lanzamientos_total)
c.metric("▶️ REPRODUCCIONES", f"{reproducciones_total:,}")
d.metric("💰 REGALÍAS", f"${regalias_total:,.2f}")
e.metric("📢 CAMPAÑAS", campanas_total)

# ============================================================
# 🌎 TIENDAS DIGITALES
# ============================================================

st.markdown(
    '<div class="section">🌎 TIENDAS DIGITALES</div>',
    unsafe_allow_html=True
)

stores = [
    ("🟢", "Spotify", "Tu perfil de artista", LINKS["spotify"]),
    ("▶️", "YouTube", "Tu canal oficial", LINKS["youtube"]),
    ("🎵", "YouTube Music", "Streaming musical", LINKS["youtube_music"]),
    ("🍎", "Apple Music", "Streaming musical", LINKS["apple"]),
    ("🟠", "Amazon Music", "Streaming musical", LINKS["amazon"]),
    ("🎵", "TikTok", "Tu perfil", LINKS["tiktok"]),
    ("🟣", "Deezer", "Streaming musical", LINKS["deezer"]),
    ("🔵", "TIDAL", "Streaming musical", LINKS["tidal"]),
    ("📻", "Pandora", "Radio y streaming", LINKS["pandora"]),
    ("🎼", "iTunes", "Música digital", LINKS["itunes"]),
    ("☁️", "SoundCloud", "Música y comunidad", LINKS["soundcloud"]),
    ("🌎", "Audiomack", "Streaming musical", LINKS["audiomack"]),
    ("🛒", "Beatport", "Tienda musical", LINKS["beatport"]),
]

for i in range(0, len(stores), 3):

    cols = st.columns(3)

    for col, store in zip(cols, stores[i:i+3]):

        icon, name, description, url = store

        with col:

            st.markdown(
                f"""
                <div class="card">
                    <h3>{icon} {name}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.link_button(
                f"ABRIR {name.upper()}",
                url,
                use_container_width=True
            )

# ============================================================
# 📱 REDES
# ============================================================

st.markdown(
    '<div class="section">📱 REDES Y CONTENIDO</div>',
    unsafe_allow_html=True
)

redes = [
    ("📸", "Instagram", LINKS["instagram"]),
    ("🎵", "TikTok", LINKS["tiktok"]),
    ("▶️", "YouTube", LINKS["youtube"]),
]

cols = st.columns(3)

for col, red in zip(cols, redes):

    icon, nombre, url = red

    with col:

        st.link_button(
            f"{icon} ABRIR {nombre.upper()}",
            url,
            use_container_width=True
        )

# ============================================================
# 🎼 DISTRIBUCIÓN
# ============================================================

st.markdown(
    '<div class="section">🎼 DISTRIBUCIÓN MUSICAL</div>',
    unsafe_allow_html=True
)

dist = [
    ("🎼 DistroKid", LINKS["distrokid"]),
    ("🟢 Spotify for Artists", LINKS["spotify_artists"]),
    ("🍎 Apple Music for Artists", LINKS["apple_artists"]),
]

cols = st.columns(3)

for col, item in zip(cols, dist):

    nombre, url = item

    with col:

        st.link_button(
            nombre,
            url,
            use_container_width=True
        )

# ============================================================
# 🎛️ CONTROL CENTER
# ============================================================

st.markdown(
    '<div class="section">🎛️ ARTIST CONTROL CENTER</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🎵 MIS CANCIONES",
    "🚀 LANZAMIENTOS",
    "📊 ESTADÍSTICAS",
    "💰 REGALÍAS",
    "📢 PROMOCIÓN",
    "👤 PERFIL"
])

# ============================================================
# 🎵 CANCIONES
# ============================================================

with tab1:

    st.subheader("🎵 Mis canciones")

    with st.form("form_cancion"):

        titulo = st.text_input(
            "Título de la canción"
        )

        proyecto = st.text_input(
            "Álbum / EP / Single"
        )

        genero = st.selectbox(
            "Género",
            [
                "Dembow",
                "Rap",
                "Hip Hop",
                "Trap",
                "Reggaetón",
                "Afrobeat",
                "Música Urbana",
                "Cristiano / Worship",
                "Otro"
            ]
        )

        fecha = st.date_input(
            "Fecha",
            value=date.today()
        )

        estado = st.selectbox(
            "Estado",
            [
                "Idea",
                "Escribiendo",
                "Grabando",
                "Producción",
                "Mezcla",
                "Masterización",
                "Listo",
                "Publicado"
            ]
        )

        enlace = st.text_input(
            "Enlace de la canción"
        )

        guardar = st.form_submit_button(
            "➕ GUARDAR CANCIÓN",
            use_container_width=True
        )

        if guardar:

            if titulo.strip():

                ejecutar("""
                    INSERT INTO canciones
                    (titulo, proyecto, genero, fecha, estado, enlace)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    titulo,
                    proyecto,
                    genero,
                    str(fecha),
                    estado,
                    enlace
                ))

                st.success(
                    "✅ Canción guardada correctamente."
                )

                st.rerun()

            else:

                st.warning(
                    "Escribe el título de la canción."
                )

    canciones = consultar("""
        SELECT
            id AS ID,
            titulo AS Título,
            proyecto AS Proyecto,
            genero AS Género,
            fecha AS Fecha,
            estado AS Estado,
            enlace AS Enlace
        FROM canciones
        ORDER BY id DESC
    """)

    if not canciones.empty:

        st.dataframe(
            canciones,
            use_container_width=True,
            hide_index=True
        )

        eliminar = st.number_input(
            "ID de canción para eliminar",
            min_value=0,
            step=1
        )

        if st.button(
            "🗑️ ELIMINAR CANCIÓN",
            use_container_width=True
        ):

            if eliminar > 0:

                ejecutar(
                    "DELETE FROM canciones WHERE id=?",
                    (eliminar,)
                )

                st.success("Canción eliminada.")
                st.rerun()

# ============================================================
# 🚀 LANZAMIENTOS
# ============================================================

with tab2:

    st.subheader("🚀 Próximo lanzamiento")

    with st.form("form_lanzamiento"):

        titulo = st.text_input(
            "Título del lanzamiento"
        )

        fecha = st.date_input(
            "Fecha de lanzamiento",
            value=date.today()
        )

        genero = st.selectbox(
            "Género del lanzamiento",
            [
                "Dembow",
                "Rap",
                "Hip Hop",
                "Trap",
                "Reggaetón",
                "Afrobeat",
                "Música Urbana",
                "Cristiano / Worship",
                "Otro"
            ]
        )

        estado = st.selectbox(
            "Estado",
            [
                "Idea",
                "En preparación",
                "Grabando",
                "Producción",
                "Listo",
                "Distribuido",
                "Publicado"
            ]
        )

        notas = st.text_area(
            "Notas"
        )

        guardar = st.form_submit_button(
            "➕ REGISTRAR LANZAMIENTO",
            use_container_width=True
        )

        if guardar:

            if titulo.strip():

                ejecutar("""
                    INSERT INTO lanzamientos
                    (titulo, fecha, genero, estado, notas)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    titulo,
                    str(fecha),
                    genero,
                    estado,
                    notas
                ))

                st.success(
                    "🚀 Lanzamiento registrado."
                )

                st.rerun()

            else:

                st.warning(
                    "Escribe el título."
                )

    lanzamientos = consultar("""
        SELECT
            id AS ID,
            titulo AS Título,
            fecha AS Fecha,
            genero AS Género,
            estado AS Estado,
            notas AS Notas
        FROM lanzamientos
        ORDER BY fecha DESC
    """)

    if not lanzamientos.empty:

        st.dataframe(
            lanzamientos,
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# 📊 ESTADÍSTICAS
# ============================================================

with tab3:

    st.subheader("📊 Estadísticas")

    with st.form("form_estadisticas"):

        fecha = st.date_input(
            "Fecha",
            value=date.today()
        )

        plataforma = st.selectbox(
            "Plataforma",
            [
                "Spotify",
                "YouTube",
                "YouTube Music",
                "TikTok",
                "Apple Music",
                "Amazon Music",
                "Deezer",
                "TIDAL",
                "Pandora",
                "SoundCloud",
                "Audiomack",
                "Otra"
            ]
        )

        cancion = st.text_input(
            "Canción"
        )

        reproducciones = st.number_input(
            "Reproducciones",
            min_value=0,
            step=1
        )

        seguidores = st.number_input(
            "Seguidores",
            min_value=0,
            step=1
        )

        notas = st.text_area(
            "Notas"
        )

        guardar = st.form_submit_button(
            "💾 GUARDAR ESTADÍSTICA",
            use_container_width=True
        )

        if guardar:

            ejecutar("""
                INSERT INTO estadisticas
                (fecha, plataforma, cancion,
                 reproducciones, seguidores, notas)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(fecha),
                plataforma,
                cancion,
                reproducciones,
                seguidores,
                notas
            ))

            st.success(
                "📊 Estadística guardada."
            )

            st.rerun()

    stats = consultar("""
        SELECT
            fecha AS Fecha,
            plataforma AS Plataforma,
            cancion AS Canción,
            reproducciones AS Reproducciones,
            seguidores AS Seguidores,
            notas AS Notas
        FROM estadisticas
        ORDER BY fecha DESC
    """)

    if not stats.empty:

        st.dataframe(
            stats,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📈 Reproducciones por plataforma")

        resumen = consultar("""
            SELECT
                plataforma AS Plataforma,
                SUM(reproducciones) AS Reproducciones
            FROM estadisticas
            GROUP BY plataforma
            ORDER BY Reproducciones DESC
        """)

        if not resumen.empty:

            resumen = resumen.set_index(
                "Plataforma"
            )

            st.bar_chart(
                resumen["Reproducciones"]
            )

# ============================================================
# 💰 REGALÍAS
# ============================================================

with tab4:

    st.subheader("💰 Regalías")

    with st.form("form_regalias"):

        fecha = st.date_input(
            "Fecha",
            value=date.today()
        )

        plataforma = st.selectbox(
            "Plataforma",
            [
                "Spotify",
                "YouTube",
                "Apple Music",
                "Amazon Music",
                "TikTok",
                "Deezer",
                "TIDAL",
                "Otra"
            ]
        )

        periodo = st.text_input(
            "Periodo",
            placeholder="Ejemplo: Agosto 2026"
        )

        reproducciones = st.number_input(
            "Reproducciones",
            min_value=0,
            step=1
        )

        ingresos = st.number_input(
            "Ingresos",
            min_value=0.0,
            step=0.01,
            format="%.2f"
        )

        moneda = st.selectbox(
            "Moneda",
            [
                "USD",
                "DOP",
                "EUR"
            ]
        )

        notas = st.text_area(
            "Notas"
        )

        guardar = st.form_submit_button(
            "💰 GUARDAR REGALÍA",
            use_container_width=True
        )

        if guardar:

            ejecutar("""
                INSERT INTO regalias
                (fecha, plataforma, periodo,
                 reproducciones, ingresos, moneda, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(fecha),
                plataforma,
                periodo,
                reproducciones,
                ingresos,
                moneda,
                notas
            ))

            st.success(
                "💰 Regalía guardada."
            )

            st.rerun()

    regalias = consultar("""
        SELECT
            fecha AS Fecha,
            plataforma AS Plataforma,
            periodo AS Periodo,
            reproducciones AS Reproducciones,
            ingresos AS Ingresos,
            moneda AS Moneda,
            notas AS Notas
        FROM regalias
        ORDER BY fecha DESC
    """)

    if not regalias.empty:

        st.dataframe(
            regalias,
            use_container_width=True,
            hide_index=True
        )

        total = regalias["Ingresos"].sum()

        st.metric(
            "💰 TOTAL REGISTRADO",
            f"{total:,.2f}"
        )

# ============================================================
# 📢 PROMOCIÓN
# ============================================================

with tab5:

    st.subheader("📢 Promoción")

    with st.form("form_promocion"):

        fecha = st.date_input(
            "Fecha",
            value=date.today()
        )

        campana = st.text_input(
            "Nombre de campaña"
        )

        plataforma = st.selectbox(
            "Plataforma",
            [
                "Instagram",
                "TikTok",
                "YouTube",
                "Spotify",
                "Facebook",
                "Otra"
            ]
        )

        presupuesto = st.number_input(
            "Presupuesto",
            min_value=0.0,
            step=0.01,
            format="%.2f"
        )

        estado = st.selectbox(
            "Estado",
            [
                "Planificada",
                "Activa",
                "Pausada",
                "Finalizada"
            ]
        )

        resultado = st.text_input(
            "Resultado"
        )

        notas = st.text_area(
            "Notas"
        )

        guardar = st.form_submit_button(
            "📢 GUARDAR CAMPAÑA",
            use_container_width=True
        )

        if guardar:

            ejecutar("""
                INSERT INTO promociones
                (fecha, campana, plataforma,
                 presupuesto, estado, resultado, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                str(fecha),
                campana,
                plataforma,
                presupuesto,
                estado,
                resultado,
                notas
            ))

            st.success(
                "📢 Campaña guardada."
            )

            st.rerun()

    promociones = consultar("""
        SELECT
            fecha AS Fecha,
            campana AS Campaña,
            plataforma AS Plataforma,
            presupuesto AS Presupuesto,
            estado AS Estado,
            resultado AS Resultado,
            notas AS Notas
        FROM promociones
        ORDER BY fecha DESC
    """)

    if not promociones.empty:

        st.dataframe(
            promociones,
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# 👤 PERFIL
# ============================================================

with tab6:

    st.subheader("👤 Perfil de Rabino Rap")

    perfil = consultar("""
        SELECT
            instagram,
            spotify,
            youtube,
            tiktok
        FROM perfil
        WHERE id=1
    """)

    valores = perfil.iloc[0]

    instagram = st.text_input(
        "📸 Instagram",
        value=valores["instagram"]
    )

    spotify = st.text_input(
        "🟢 Spotify",
        value=valores["spotify"]
    )

    youtube = st.text_input(
        "▶️ YouTube",
        value=valores["youtube"]
    )

    tiktok = st.text_input(
        "🎵 TikTok",
        value=valores["tiktok"]
    )

    if st.button(
        "💾 GUARDAR PERFIL",
        use_container_width=True
    ):

        ejecutar("""
            UPDATE perfil
            SET instagram=?,
                spotify=?,
                youtube=?,
                tiktok=?
            WHERE id=1
        """, (
            instagram,
            spotify,
            youtube,
            tiktok
        ))

        st.success(
            "✅ Perfil actualizado."
        )

        st.rerun()

    st.markdown("---")

    st.subheader("🔗 Accesos rápidos")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.link_button(
            "📸 INSTAGRAM",
            instagram,
            use_container_width=True
        )

    with c2:
        st.link_button(
            "🟢 SPOTIFY",
            spotify,
            use_container_width=True
        )

    with c3:
        st.link_button(
            "▶️ YOUTUBE",
            youtube,
            use_container_width=True
        )

    with c4:
        st.link_button(
            "🎵 TIKTOK",
            tiktok,
            use_container_width=True
        )

# ============================================================
# 🔄 ACTUALIZAR DATOS
# ============================================================

st.markdown("---")

if st.button(
    "🔄 ACTUALIZAR STREAMING HOUSE",
    use_container_width=True
):

    st.rerun()

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    <b>🏠 STREAMING HOUSE</b><br>
    MUSIC • DISTRIBUTION • ARTIST CONTROL CENTER<br><br>
    🎤 RABINO RAP © 2026
</div>
""", unsafe_allow_html=True)
