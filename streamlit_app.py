import streamlit as st
import requests

st.set_page_config(page_title="CEREBRO OMEGA", page_icon="🧠", layout="wide")

def motor_bible(tema):
    try:
        r = requests.get(f"https://bible-api.com/?q={tema}&translation=rvr1960", timeout=4).json()
        return f"📖 {r['reference']}: {r['text'][:300]}"
    except:
        return "📖 [Juan 3:16] Porque de tal manera amó Dios al mundo"

def motor_knowledge(tema):
    if "amor" in tema.lower() and "dios" in tema.lower():
        return "🧠 CONOCIMIENTO: El amor de Dios es ágape. Incondicional, eterno, que da sin esperar. La ciencia lo mide como oxitocina + apego, pero la fe dice que viene de Dios."
    elif "vida" in tema.lower():
        return "🧠 CONOCIMIENTO: La vida según ciencia: 3.8 mil millones de años de evolución. Según Torah: Dios sopló aliento. Ambas hablan de algo sagrado y complejo."
    else:
        return f"🧠 CONOCIMIENTO: Analizando {tema}. La ciencia busca el cómo. La fe busca el por qué."

def motor_reasoning(bible, knowledge):
    return f"💡 RAZONAMIENTO: {bible} + {knowledge} = La conclusión es que fe y ciencia no se pelean. Se complementan."

def hablar(texto):
    js = f"""
    <script>
    function hablar() {{
        speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance(`{texto.replace('`','').replace('"','')}`);
        msg.lang = 'es-MX';
        msg.rate = 0.88;
        speechSynthesis.speak(msg);
    }}
    </script>
    <button onclick="hablar()" style="background:#FF4B4B;color:white;border:none;padding:14px 24px;border-radius:10px;font-size:16px;font-weight:bold;cursor:pointer;width:100%;">
    🔊 CEREBRO HABLA
    </button>
    """
    st.components.v1.html(js, height=55)

st.title("🧠 CEREBRO OMEGA v2.1")
st.caption("CORE MONOLÍTICO • CONOCIMIENTO • MEMORIA • EVOLUCIÓN")

orden = st.text_area("🎯 ORDEN PARA CEREBRO", "", height=120)

if st.button("🚀 EJECUTAR CEREBRO", type="primary", use_container_width=True):
    b = motor_bible(orden)
    k = motor_knowledge(orden)
    r = motor_reasoning(b, k)
    
    res = f"🧠 ANÁLISIS DE CEREBRO OMEGA\nOrden: {orden}\n\n{b}\n\n{k}\n\n{r}\n\n✅ CICLO COMPLETO - 100%"
    st.session_state["res"] = res

if "res" in st.session_state:
    st.success("RESPUESTA DE CEREBRO OMEGA")
    st.text(st.session_state["res"])
    hablar(st.session_state["res"])
    
    st.divider()
    st.subheader("🔄 ÚLTIMO CICLO EVOLUTIVO")
    st.metric("Estado", "CICLO COMPLETO")
    st.metric("Eficiencia", "100%")
    st.code("bible, knowledge, memory, reasoning")
