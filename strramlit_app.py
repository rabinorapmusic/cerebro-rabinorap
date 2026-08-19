impor streamlit a st
impor json
importos
impormodules/alimentador
impor☆hashlib
fro datetime impor datetime
fro modules.alimentador importAlimentadorOmega
# =alimentador = AlimentadorOmega()===========================================================
# 🧠 CEREBRO OMEGA ∞
# Núcleo experimental en un solo archivo
# ============================================================
st.divider()

st.subheader("📡 ALIMENTAR CEREBRO OMEGA")

concepto_externo = st.text_input(
    "¿Qué quieres que CEREBRO OMEGA investigue?",
    placeholder="Ejemplo: inteligencia artificial"
)

ifst.button("🌐 BUSCAR CONOCIMIENTO"):

    i concepto_externo.strip():

        wit st.spinner("🧠 CEREBRO OMEGA está investigando..."):

            resultado = alimentador.alimentar(
                concepto_externo.strip()
            )

        ifresultado.get("ok"):

            conocimiento = resultado["memoria"]

            st.success(
                f"Información encontrada sobre: "
                f"{conocimiento['concepto']}"
            )

            st.write(
                conocimiento["informacion"]
            )

            st.caption(
                f"Fuente: {conocimiento['fuente']}"
            )

            st.info(
                "📚 Conocimiento preparado. "
                "Todavía no se ha escrito en la memoria."
            )

        els:

            st.error(
                resultado.get(
                    "error",
                    "No se pudo obtener información."
                )
            )

    els:

        st.warning(
            "Escribe un concepto primero."
            )
st.set_page_config(
    page_title="CEREBRO OMEGA",
    page_icon="🧠",
    layout="wide"
)

MEMORIA = "memoria_omega.json"


# ============================================================
# MEMORIA
# ============================================================

def cargar_memoria():
    if not os.path.exists(MEMORIA):
        return {
            "conocimiento": {},
            "experiencias": [],
            "ciclos": 0
        }

    tr:
        wit open(MEMORIA, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        datos.setdefault("conocimiento", {})
        datos.setdefault("experiencias", [])
        datos.setdefault("ciclos", 0)

        retur datos

    excep Exception:
        retur {
            "conocimiento": {},
            "experiencias": [],
            "ciclos": 0
        }


de guardar_memoria():
    withopen(MEMORIA, "w", encoding="utf-8") as archivo:
        json.dump(
            st.session_state.memoria,
            archivo,
            ensure_ascii=False,
            indent=2
        )


i "memoria" no inst.session_state:
    st.session_state.memoria = cargar_memoria()


# ============================================================
# IDENTIDAD
# ============================================================

def identidad():
    return {
        "nombre": "CEREBRO OMEGA",
        "version": "OMEGA",
        "estado": "ACTIVO",
        "principio": "APRENDER → RECORDAR → RAZONAR → EVOLUCIONAR → ∞"
    }


# ============================================================
# ANALIZADOR DE ORDEN
# ============================================================

def analizar_orden(texto):

    texto = texto.strip()

    if not texto:
        return {
            "tipo": "vacío",
            "intencion": "ninguna",
            "palabras": [],
            "huella": ""
        }

    limpio = texto.lower()

    palabras = re.findall(r"\b[\wáéíóúüñ]+\b", limpio)

    if any(x in limpio for x in [
        "aprende",
        "aprendizaje",
        "recuerda",
        "enseña",
        "memoriza"
    ]):
        intencion = "aprendizaje"

    elif any(x in limpio for x in [
        "quien",
        "qué",
        "que",
        "cómo",
        "como",
        "por qué",
        "porque",
        "explica"
    ]):
        intencion = "conocimiento"

    elif any(x in limpio for x in [
        "piensa",
        "razona",
        "analiza",
        "compara",
        "resuelve"
    ]):
        intencion = "razonamiento"

    elif any(x in limpio for x in [
        "evoluciona",
        "evolución",
        "mejora",
        "ciclo"
    ]):
        intencion = "evolución"

    else:
        intencion = "general"

    huella = hashlib.sha256(
        limpio.encode("utf-8")
    ).hexdigest()[:12]

    return {
        "tipo": "orden",
        "intencion": intencion,
        "palabras": palabras,
        "huella": huella
    }


# ============================================================
# RECUPERACIÓN DE CONOCIMIENTO
# ============================================================

def buscar_conocimiento(consulta):

    consulta = consulta.lower()

    encontrados = []

    for concepto, informacion in st.session_state.memoria[
        "conocimiento"
    ].items():

        if concepto.lower() in consulta:
            encontrados.append(
                f"📚 {concepto}: {informacion}"
            )

        else:
            palabras = concepto.lower().split()

            coincidencias = sum(
                1 for palabra in palabras
                if len(palabra) > 3 and palabra in consulta
            )

            if coincidencias:
                encontrados.append(
                    f"📚 {concepto}: {informacion}"
                )

    return encontrados


# ============================================================
# MOTOR DE RAZONAMIENTO
# ============================================================

def razonar(orden, analisis, conocimiento):

    resultado = []

    resultado.append(
        "🧠 CEREBRO OMEGA está procesando la orden."
    )

    resultado.append(
        f"🎯 Intención detectada: {analisis['intencion']}"
    )

    resultado.append(
        f"🔢 Palabras analizadas: {len(analisis['palabras'])}"
    )

    if conocimiento:
        resultado.append(
            "\n".join(conocimiento)
        )
    else:
        resultado.append(
            "📚 No encontré conocimiento almacenado relacionado."
        )

    if analisis["intencion"] == "aprendizaje":
        resultado.append(
            "💡 La orden parece estar relacionada con aprendizaje."
        )

    elif analisis["intencion"] == "razonamiento":
        resultado.append(
            "🔎 El cerebro está preparado para relacionar "
            "la información disponible."
        )

    elif analisis["intencion"] == "evolución":
        resultado.append(
            "♾️ La orden solicita ejecutar un ciclo evolutivo."
        )

    else:
        resultado.append(
            "⚙️ La orden fue recibida y procesada por el núcleo."
        )

    return "\n\n".join(resultado)


# ============================================================
# APRENDIZAJE
# ============================================================

def aprender(concepto, informacion):

    concepto = concepto.strip().lower()
    informacion = informacion.strip()

    if not concepto or not informacion:
        return False

    st.session_state.memoria["conocimiento"][concepto] = informacion

    st.session_state.memoria["experiencias"].append({
        "fecha": datetime.now().isoformat(),
        "concepto": concepto,
        "accion": "aprendizaje"
    })

    guardar_memoria()

    return True


# ============================================================
# EVOLUCIÓN
# ============================================================

def evolucionar():

    memoria = st.session_state.memoria

    memoria["ciclos"] += 1

    numero = memoria["ciclos"]

    conocimiento = len(memoria["conocimiento"])
    experiencias = len(memoria["experiencias"])

    memoria["experiencias"].append({
        "fecha": datetime.now().isoformat(),
        "accion": "ciclo_evolutivo",
        "ciclo": numero
    })

    guardar_memoria()

    return {
        "ciclo": numero,
        "conocimiento": conocimiento,
        "experiencias": experiencias
    }


# ============================================================
# VOZ
# ============================================================

def hablar(texto):

    texto_seguro = (
        texto.replace("\\", "")
        .replace("`", "")
        .replace("</script>", "")
        .replace("<script>", "")
    )

    codigo = f"""
    <script>
    function omegaHablar() {{
        window.speechSynthesis.cancel();

        const mensaje =
            new SpeechSynthesisUtterance(
                {json.dumps(texto_seguro, ensure_ascii=False)}
            );

        mensaje.lang = "es-ES";
        mensaje.rate = 0.9;
        mensaje.pitch = 0.8;

        window.speechSynthesis.speak(mensaje);
    }}

    omegaHablar();
    </script>

    <button onclick="omegaHablar()">
        🔊 REPETIR RESPUESTA
    </button>
    """

    st.components.v1.html(codigo, height=55)


# ============================================================
# ESTADO DEL CEREBRO
# ============================================================

def estado_cerebro():

    memoria = st.session_state.memoria

    return {
        "Estado": "🟢 ACTIVO",
        "Conocimiento": len(memoria["conocimiento"]),
        "Experiencias": len(memoria["experiencias"]),
        "Ciclos evolutivos": memoria["ciclos"]
    }


# ============================================================
# INTERFAZ
# ============================================================

st.title("🧠 CEREBRO OMEGA ∞")

st.caption(
    "APRENDER → RECORDAR → RAZONAR → EVOLUCIONAR → ∞"
)

st.divider()

estado = estado_cerebro()

a, b, c, d = st.columns(4)

with a:
    st.metric("ESTADO", estado["Estado"])

with b:
    st.metric("CONOCIMIENTO", estado["Conocimiento"])

with c:
    st.metric("EXPERIENCIAS", estado["Experiencias"])

with d:
    st.metric("CICLOS ∞", estado["Ciclos evolutivos"])


st.divider()


# ============================================================
# ORDEN
# ============================================================

st.subheader("🧠 CENTRO DE PENSAMIENTO")

orden = st.text_area(
    "Dale una orden a CEREBRO OMEGA:",
    placeholder=(
        "Ejemplo: analiza lo que sabes sobre música "
        "o recuerda qué es el rap"
    ),
    height=120
)

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "⚡ EJECUTAR ORDEN",
        use_container_width=True
    ):

        if not orden.strip():

            st.warning(
                "CEREBRO OMEGA necesita una orden."
            )

        else:

            analisis = analizar_orden(orden)

            conocimiento = buscar_conocimiento(orden)

            respuesta = razonar(
                orden,
                analisis,
                conocimiento
            )

            st.session_state.respuesta = respuesta
            st.session_state.ultimo_analisis = analisis


with col2:

    if st.button(
        "♾️ EJECUTAR CICLO EVOLUTIVO",
        use_container_width=True
    ):

        evolucion = evolucionar()

        st.session_state.respuesta = (
            "♾️ CICLO EVOLUTIVO COMPLETADO\n\n"
            f"🔄 Ciclo: {evolucion['ciclo']}\n"
            f"📚 Conocimiento: {evolucion['conocimiento']}\n"
            f"🧠 Experiencias: {evolucion['experiencias']}\n\n"
            "CEREBRO OMEGA registró el ciclo en su memoria."
        )

        st.rerun()


# ============================================================
# APRENDER
# ============================================================

st.divider()

st.subheader("📚 ENSEÑAR A CEREBRO OMEGA")

col1, col2 = st.columns(2)

with col1:

    concepto = st.text_input(
        "CONCEPTO",
        placeholder="Ejemplo: rap"
    )

with col2:

    informacion = st.text_input(
        "INFORMACIÓN",
        placeholder="Ejemplo: El rap utiliza ritmo, rima y métrica."
    )


if st.button(
    "💾 APRENDER Y RECORDAR",
    use_container_width=True
):

    if aprender(concepto, informacion):

        st.success(
            f"🧠 Aprendido: {concepto}"
        )

        st.rerun()

    else:

        st.warning(
            "Escribe un concepto y una información."
        )


# ============================================================
# RESPUESTA
# ============================================================

if "respuesta" in st.session_state:

    st.divider()

    st.subheader("🧠 RESPUESTA DE CEREBRO OMEGA")

    st.text(
        st.session_state.respuesta
    )

    hablar(
        st.session_state.respuesta
    )


# ============================================================
# DIAGNÓSTICO
# ============================================================

if "ultimo_analisis" in st.session_state:

    with st.expander("🔬 VER PROCESAMIENTO INTERNO"):

        analisis = st.session_state.ultimo_analisis

        st.json(analisis)


# ============================================================
# MEMORIA
# ============================================================

with st.expander("💾 MEMORIA DE CEREBRO OMEGA"):

    memoria = st.session_state.memoria

    if memoria["conocimiento"]:

        for concepto, informacion in memoria[
            "conocimiento"
        ].items():

            st.markdown(
                f"**🧠 {concepto}** → {informacion}"
            )

    else:

        st.info(
            "La memoria todavía está vacía."
        )


# ============================================================
# PIE
# ============================================================

st.divider()

st.caption(
    "🧠 CEREBRO OMEGA ∞ | "
    "Núcleo experimental de aprendizaje y evolución"
)
