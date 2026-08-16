import streamlit as st
import pandas as pd

# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="CEREBRO RABINO PRO v5",
    layout="wide",
    page_icon="🧠"
)

st.title("🧠 CEREBRO RABINO PRO v5")
st.caption("🎤 Letras • 🥁 Beats • 🎧 Suno • 🎨 Portadas • 💾 Proyectos")

# ============================================================
# PESTAÑAS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "✍️ GENERADOR MUSICAL",
    "🎨 PORTADA",
    "🎰 IAS",
    "💾 MIS CANCIONES"
])

# ============================================================
# TAB 1 — GENERADOR MUSICAL
# ============================================================

with tab1:

    st.header("🔥 GENERADOR MUSICAL ULTRA")

    col1, col2 = st.columns(2)

    with col1:

        tema = st.text_area(
            "🎯 TEMA DE LA CANCIÓN",
            placeholder="Ej: Dios me levantó del lodo y convirtió mi dolor en propósito",
            height=120
        )

        sentimiento = st.selectbox(
            "❤️ SENTIMIENTO",
            [
                "Agradecido",
                "Dolorido",
                "Guerrero",
                "Victorioso",
                "Profundo",
                "Espiritual",
                "Esperanzador",
                "Épico",
                "Melancólico",
                "Inspirador"
            ]
        )

        genero = st.selectbox(
            "🎵 GÉNERO",
            [
                "Worship",
                "Trap Cristiano",
                "Rap",
                "Hip Hop",
                "Dembow Cristiano",
                "Drill Cristiano",
                "Reggaeton Cristiano",
                "Balada",
                "Afrobeat Cristiano"
            ]
        )

    with col2:

        bpm = st.slider(
            "⏱️ BPM",
            60,
            180,
            90
        )

        voz = st.selectbox(
            "🎙️ VOZ",
            [
                "Voz Masculina Profunda",
                "Voz Masculina Emocional",
                "Voz Masculina Agresiva",
                "Voz Femenina Dulce",
                "Voz Femenina Poderosa",
                "Coro Gospel",
                "Voz Principal + Coro Gospel"
            ]
        )

        instrumentos = st.multiselect(
            "🎹 INSTRUMENTOS",
            [
                "Piano",
                "Coro Gospel",
                "Strings",
                "Pads",
                "808",
                "Kick profundo",
                "Hi Hats",
                "Percusión latina",
                "Guitarra acústica",
                "Guitarra eléctrica",
                "Bajo",
                "Órgano",
                "Synth",
                "FX Cinemáticos"
            ],
            default=["Piano", "808", "Bajo"]
        )

    st.divider()

    col3, col4, col5 = st.columns(3)

    with col3:
        intensidad = st.slider(
            "🔥 INTENSIDAD",
            1,
            10,
            8
        )

    with col4:
        dominicano = st.checkbox(
            "🇩🇴 SABOR DOMINICANO"
        )

    with col5:
        imaginacion = st.checkbox(
            "🧠 MODO IMAGINACIÓN",
            value=True
        )

    concepto = st.text_input(
        "🎬 CONCEPTO VISUAL",
        placeholder="Ej: Un hombre saliendo del lodo hacia una ciudad iluminada"
    )

    mensaje = st.text_area(
        "💡 MENSAJE QUE QUIERES TRANSMITIR",
        placeholder="Ej: Quiero que alguien que esté sufriendo encuentre esperanza",
        height=80
    )

    # ========================================================
    # GENERADOR
    # ========================================================

    if st.button(
        "🚀 CREAR CANCIÓN ULTRA",
        type="primary",
        use_container_width=True
    ):

        if not tema.strip():

            st.warning("⚠️ Escribe primero el tema.")

        else:

            instrumentos_texto = (
                ", ".join(instrumentos)
                if instrumentos
                else "Instrumentación moderna"
            )

            # =================================================
            # LETRA
            # =================================================

            letra = f"""
[INTRO]

Yeah...
Esta canción nace de una historia real.

[VERSE 1]

Yo estaba perdido buscando una salida,
con muchas heridas cargando la vida.
Pensé que mi historia llegaba al final,
pero tu mano me volvió a levantar.

Cuando nadie estuvo, tú permaneciste,
cuando estaba abajo, tú me sostuviste.
Ahora miro atrás y puedo entender,
que cada batalla me hizo crecer.

[PRE-CHORUS]

Y aunque la noche quiera apagar mi fe,
sé que mañana volveré a vencer.

[CHORUS]

{tema}

Tú cambiaste mi historia,
convertiste mi derrota en victoria.
Cuando pensé que no podía más,
tu mano me enseñó a caminar.

{tema}

Hoy levanto mi voz,
porque después del dolor
todavía existe esperanza,
todavía existe amor.

[VERSE 2]

Hubo noches donde no pude dormir,
preguntándole a Dios por qué estaba allí.
Pero cada lágrima tuvo una razón,
cada cicatriz fortaleció mi corazón.

Ahora camino sin mirar atrás,
lo que perdí ya no me define jamás.
Tengo propósito, tengo dirección,
y llevo esperanza dentro del corazón.

[BRIDGE]

Aunque caiga, me levantaré.
Aunque llore, continuaré.
Aunque el mundo diga que no puedo,
con Dios yo sé que venceré.

[FINAL CHORUS]

{tema}

Ahora canto con más fuerza,
porque sobreviví la tormenta.
Lo que parecía mi final
se convirtió en un nuevo comienzo.

{tema}

Hoy levanto mi voz,
toda la gloria sea para Dios.

[OUTRO]

No fue suerte.
No fue casualidad.
Fue propósito.
"""

            # =================================================
            # CONCEPTO DEL BEAT
            # =================================================

            beat = f"""
🥁 CONCEPTO DEL BEAT

Género: {genero}
BPM: {bpm}
Sentimiento: {sentimiento}
Intensidad: {intensidad}/10

Instrumentos:
{instrumentos_texto}

INTRO:
Ambiente cinematográfico y progresivo.

VERSO:
Beat minimalista para dejar espacio a la voz.

PRE-CORO:
Agregar tensión progresivamente.

CORO:
Abrir completamente la producción.

BAJO:
Profundo, limpio y conectado con el kick.

BATERÍA:
Kick definido, snare fuerte y hi-hats dinámicos.

PUENTE:
Reducir instrumentos para crear contraste.

CORO FINAL:
Máxima energía de toda la canción.

OUTRO:
Final progresivo y emocional.
"""

            # =================================================
            # DIRECCIÓN VOCAL
            # =================================================

            direccion_vocal = f"""
🎙️ DIRECCIÓN VOCAL

Voz:
{voz}

Versos:
Interpretación íntima y emocional.

Pre-coro:
Aumentar progresivamente la intensidad.

Coro:
Interpretación poderosa y abierta.

Puente:
Mayor emoción y vulnerabilidad.

Coro final:
Máxima potencia vocal.

Adlibs:
Utilizar respuestas vocales y armonías
en las partes más importantes.
"""

            # =================================================
            # SUNO
            # =================================================

            suno = f"""
{genero}, {bpm} BPM, {sentimiento.lower()},
{voz.lower()}, professional studio production,
emotional and powerful performance,
{instrumentos_texto},
cinematic atmosphere,
dynamic arrangement,
strong memorable chorus,
deep bass,
modern drums,
wide stereo image,
clean professional mix,
spiritual inspirational energy,
powerful final chorus,
original composition,
commercial quality.
"""

            # =================================================
            # RESULTADO
            # =================================================

            proyecto = f"""
==================================================
🧠 CEREBRO RABINO PRO
PROYECTO MUSICAL
==================================================

TÍTULO / TEMA:
{tema}

GÉNERO:
{genero}

BPM:
{bpm}

SENTIMIENTO:
{sentimiento}

VOZ:
{voz}

==================================================
✍️ LETRA
==================================================

{letra}

==================================================
🥁 CONCEPTO DEL BEAT
==================================================

{beat}

==================================================
🎙️ DIRECCIÓN VOCAL
==================================================

{direccion_vocal}

==================================================
🎧 PROMPT PARA SUNO
==================================================

{suno}

==================================================
🎬 CONCEPTO VISUAL
==================================================

{concepto if concepto else "Crear una portada cinematográfica basada en el mensaje de la canción."}

==================================================
💡 MENSAJE
==================================================

{mensaje if mensaje else "Inspirar esperanza, fe y superación."}
"""

            # =================================================
            # MOSTRAR
            # =================================================

            st.success("🔥 ¡CANCIÓN CREADA!")

            st.subheader("🎵 PROYECTO COMPLETO")

            st.text_area(
                "Resultado",
                proyecto,
                height=700
            )

            # =================================================
            # BOTONES
            # =================================================

            nombre = (
                tema[:35]
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            colA, colB = st.columns(2)

            with colA:

                st.download_button(
                    "📥 DESCARGAR PROYECTO",
                    proyecto,
                    file_name=f"Rabino_Rap_{nombre}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with colB:

                st.download_button(
                    "🎧 DESCARGAR PROMPT SUNO",
                    suno,
                    file_name=f"Suno_{nombre}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            st.divider()

            st.subheader("🥁 PROMPT DEL BEAT")

            st.code(beat, language="text")

            st.subheader("🎧 PROMPT SUNO")

            st.code(suno, language="text")

            st.balloons()


# ============================================================
# TAB 2 — PORTADA
# ============================================================

with tab2:

    st.header("🎨 GENERADOR DE PORTADA")

    st.write(
        "Sube tu foto y crea el concepto profesional de portada."
    )

    uploaded_img = st.file_uploader(
        "📸 SUBE TU FOTO",
        type=["jpg", "jpeg", "png"]
    )

    titulo_portada = st.text_input(
        "🎵 TÍTULO",
        placeholder="Ej: Dios me levantó"
    )

    if uploaded_img:

        st.image(
            uploaded_img,
            caption="Tu foto",
            width=250
        )

        prompt_portada = f"""
Professional Christian music album cover.

Artist: Rabino Rap
Title: {titulo_portada if titulo_portada else "Nuevo lanzamiento"}

Create a cinematic and premium music cover.

Use the uploaded person's face as visual reference.

Powerful expression.
Professional lighting.
High-end photography.
Cinematic atmosphere.
Christian symbolism.
Dramatic depth.
Premium color grading.
Modern hip-hop aesthetic.
Professional album artwork.

Square format.
3000x3000 pixels.
No watermark.
No unnecessary objects.
"""

        st.text_area(
            "🎨 PROMPT PROFESIONAL",
            prompt_portada,
            height=300
        )

        st.link_button(
            "🎨 ABRIR BING IMAGE CREATOR",
            "https://www.bing.com/images/create"
        )


# ============================================================
# TAB 3 — IAS
# ============================================================

with tab3:

    st.header("🎰 PANEL DE HERRAMIENTAS IA")

    st.link_button(
        "🎵 SUNO",
        "https://suno.com/create"
    )

    st.link_button(
        "🔥 UDIO",
        "https://udio.com/create"
    )

    st.info(
        "Puedes utilizar los prompts generados en la TAB 1."
    )


# ============================================================
# TAB 4 — CANCIONES
# ============================================================

with tab4:

    st.header("💾 MIS CANCIONES")

    st.info(
        "🚧 Sistema de biblioteca automática próximamente."
    )

    st.write(
        "Aquí podremos guardar títulos, letras, prompts, "
        "BPM y proyectos completos."
)
