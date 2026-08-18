import streamlit as st
import requests

st.set_page_config(page_title="CEREBRO OMEGA", page_icon="🧠")

def bible(tema):
    try:
        r = requests.get(f"https://bible-api.com/?q={tema}&translation=rvr1960", timeout=3).json()
        return f"[{r['reference']}] {r['text'][:250]}"
    except:
        return "[Salmos 19:1] Los cielos cuentan la gloria de Dios"

def paper(tema):
    try:
        r = requests.get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={tema}&retmax=1&retmode=json", timeout=3).json()
        ids = r.get("esearchresult", {}).get("idlist", [])
        return f"PubMed: {len(ids)}" if ids else ""
    except:
        return ""

def hablar(texto):
    js = f"""
    <script>
    function hablar() {{
        speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance(`{texto.replace('`','').replace('"','')}`);
        msg.lang = 'es-MX';
        msg.rate = 0.9;
        speechSynthesis.speak(msg);
    }}
    </script>
    <button onclick="hablar()" style="background:#FF4B4B;color:white;border:none;padding:14px 24px;border-radius:10px;font-size:16px;font-weight:bold;cursor:pointer;width:100%;">
    🔊 CEREBRO OMEGA HABLA
    </button>
    """
    st.components.v1.html(js, height=55)

st.title("🧠 CEREBRO OMEGA")

orden = st.text_area("ORDEN", "Explica ciencia y fe", height=100)

if st.button("EJECUTAR", type="primary", use_container_width=True):
    b = bible(orden)
    p = paper(orden)
    res = f"📖 {b}\n\n🔬 {p}"
    st.session_state["res"] = res

if "res" in st.session_state:
    st.text(st.session_state["res"])
    hablar(st.session_state["res"])
