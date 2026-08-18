""" CEREBRO OMEGA v3.0 EDICIÓN COMPLETA - TODO EN 1 Motor + Música + Bible + Voz + Exportar + Acordes """
import streamlit as st
import json, time, hashlib
from pathlib import Path
from typing import Any, Dict, List
import io

# ========== MOTOR EVOLUTIVO ==========
class EvolutionEngine:
    VERSION = "3.0"
    def __init__(self, storage_dir: str = "data/cerebro"):
        self.storage_dir = Path(storage_dir); self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.memory_file = self.storage_dir / "evolution_memory.json"
        self.cycles_file = self.storage_dir / "evolution_cycles.json"
        self.memory = self._load_json(self.memory_file, {"facts": [], "learned": [], "improvements": []})
        self.cycles = self._load_json(self.cycles_file, {"total": 0, "history": []})

    def _load_json(self, path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not path.exists(): self._save_json(path, default); return default
            with path.open("r", encoding="utf-8") as file: return json.load(file)
        except: return default
    def _save_json(self, path: Path, data: Dict[str, Any]) -> None:
        with open(path, "w", encoding="utf-8") as file: json.dump(data, file, ensure_ascii=False, indent=2)
    def _make_id(self, text: str) -> str: return hashlib.sha256(f"{text}:{time.time_ns()}".encode()).hexdigest()[:16]
    def evaluate(self, result: Any) -> Dict[str, Any]:
        text = str(result).strip();
        if not text: return {"score": 0.0, "quality": "EMPTY", "useful": False}
        score = 0.5 + min(len(text)/1000, 0.3) + (0.2 if "Dios" in text else 0)
        score = min(score, 1.0); quality = "EXCELLENT" if score >= 0.8 else "GOOD" if score >= 0.6 else "AVERAGE" if score >= 0.4 else "LOW"
        return {"score": round(score, 4), "quality": quality, "useful": score >= 0.6}
    def run_cycle(self, input_text: str, processor_result: Any) -> Dict[str, Any]:
        started = time.time(); evaluation = self.evaluate(processor_result)
        learning = {"id": self._make_id(input_text), "input": input_text, "score": evaluation["score"], "timestamp": time.time()}
        self.memory["learned"].append(learning);
        if len(self.memory["learned"]) > 1000: self.memory["learned"] = self.memory["learned"][-1000:]
        self._save_json(self.memory_file, self.memory)
        self.cycles["total"] += 1
        cycle = {"cycle": self.cycles["total"], "input": input_text, "result": str(processor_result)[:2000], "evaluation": evaluation, "duration_ms": round((time.time() - started) * 1000, 2), "timestamp": time.time()}
        self.cycles["history"].append(cycle);
        if len(self.cycles["history"]) > 500: self.cycles["history"] = self.cycles["history"][-500:]
        self._save_json(self.cycles_file, self.cycles); return cycle
    def diagnostics(self) -> Dict[str, Any]: return {"status": "ACTIVE", "version": self.VERSION, "cycles": self.cycles["total"], "learned": len(self.memory["learned"])}
    def recent_cycles(self, limit: int = 10) -> List[Dict[str, Any]]: return self.cycles["history"][-max(1, int(limit)):]

# ========== BIBLE ENGINE ==========
class BibleEngine:
    def __init__(self):
        self.db = {
            "ciencia": "[Salmos 19:1] Los cielos cuentan la gloria de Dios",
            "presencia": "[Salmos 139:7] ¿A dónde huiré de tu presencia?",
            "adoracion": "[Juan 4:24] Dios es Espíritu; y los que le adoran",
            "fe": "[Hebreos 11:1] La fe es la certeza de lo que se espera",
            "amor": "[1 Juan 4:8] Dios es amor"
        }
    def buscar(self, tema: str) -> str:
        for k in self.db:
            if k in tema.lower(): return self.db[k]
        return "[Salmos 100:2] Servid a Jehová con alegría"

# ========== MUSIC ENGINE + ACORDES ==========
class MusicEngine:
    BPM_DEFAULT = 72
    ACORDES = {"C": "C - G - Am - F", "G": "G - D - Em - C", "D": "D - A - Bm - G"}
    def __init__(self): self.bible = BibleEngine()
    def generar(self, prompt: str, bpm: int = BPM_DEFAULT) -> Dict[str, Any]:
        tema = next((t for t in ["ciencia","presencia","adoracion","fe","amor"] if t in prompt.lower()), "adoracion")
        tonalidad = "C" if bpm < 80 else "G"
        versiculo = self.bible.buscar(tema)
        letra = f"🎵 {bpm} BPM | Tonalidad: {tonalidad} | Tema: {tema}\n\n"
        letra += f"[Intro]\n{versiculo}\n\n"
        letra += f"[Verso 1]\nEn tu creación veo tu poder\nCiencia y fe se unen en tu ser\nTu presencia me hace renacer\nToda mi vida es para ti\n\n"
        letra += f"[Coro]\nTe adoro, te adoro\nRey de gloria y majestad\nMi corazón te pertenece\nPor toda la eternidad\n\n"
        letra += f"[Puente]\nEspíritu ven, llena este lugar\nQue tu gloria descienda sin parar\n\n"
        letra += f"[Coro Final]\nTe adoro, te adoro [x2]"
        return {"letra": letra, "bpm": bpm, "tonalidad": tonalidad, "acordes": self.ACORDES[tonalidad], "tema": tema}

# ========== VOICE ENGINE ==========
class VoiceEngine:
    def __init__(self):
        self.STATUS = "OFFLINE"
        try:
            import pyttsx3; self.engine = pyttsx3.init(); self.engine.setProperty('rate', 145); self.STATUS = "ACTIVE"
        except: pass
    def hablar(self, texto: str):
        if self.STATUS == "ACTIVE":
            try: self.engine.say(texto[:500]); self.engine.runAndWait(); return "✅ Hablado"
            except: return "❌ Error"
        return "⚠️ Instala pyttsx3: pip install pyttsx3"

# ========== CEREBRO CORE ==========
class CerebroCore:
    def __init__(self):
        self.engine = EvolutionEngine()
        self.music = MusicEngine()
        self.voice = VoiceEngine()
    def ejecutar(self, orden: str):
        if any(p in orden.lower() for p in ["cancion","worship","bpm","letra"]):
            mus = self.music.generar(orden)
            resultado = f"{mus['letra']}\n\n[ACORDES: {mus['acordes']}]"
        else: resultado = f"🧠 Orden recibida: {orden}\n\nCEREBRO OMEGA listo para crear."
        ciclo = self.engine.run_cycle(orden, resultado)
        return ciclo, mus if 'mus' in locals() else None
    def diagnostico(self):
        d = self.engine.diagnostics()
        d.update({"music": "ACTIVE", "bible": "READY", "voice": self.voice.STATUS, "acordes": "ACTIVE", "export": "ACTIVE"})
        return d

# ========== STREAMLIT UI ==========
st.set_page_config(page_title="CEREBRO OMEGA v3.0", page_icon="🧠", layout="wide")
cerebro = CerebroCore()

st.title("🧠 CEREBRO OMEGA ∞ v3.0")
st.caption("Motor Evolutivo • Música Worship • Bible • Voz • Acordes • Exportar")

diag = cerebro.diagnostico()
cols = st.columns(6)
cols[0].metric("🧠 CEREBRO", diag["status"])
cols[1].metric("🎵 MÚSICA", diag["music"])
cols[2].metric("📖 BIBLE", diag["bible"])
cols[3].metric("🔊 VOZ", diag["voice"])
cols[4].metric("🎸 ACORDES", diag["acordes"])
cols[5].metric("CICLOS", diag["cycles"])

st.divider()
orden = st.text_area("🎯 ORDEN A CEREBRO OMEGA", "Escribeme una cancion worship 72bpm sobre ciencia, filosofia y religion", height=120)

col1, col2, col3 = st.columns(3)
ejecutar = col1.button("🧠 EJECUTAR", type="primary", use_container_width=True)
hablar = col2.button("🔊 HABLAR", use_container_width=True)
exportar = col3.button("💾 EXPORTAR.TXT", use_container_width=True)

if ejecutar:
    with st.spinner("CEREBRO pensando y componiendo..."):
        ciclo, mus_data = cerebro.ejecutar(orden)
        st.session_state["ultimo"] = ciclo
        st.session_state["mus"] = mus_data

    st.success("✅ CICLO COMPLETADO")
    st.subheader("🎵 RESULTADO")
    st.text(ciclo["result"])

    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Score", ciclo["evaluation"]["score"])
    col_s2.metric("Calidad", ciclo["evaluation"]["quality"])
    col_s3.metric("Tiempo", f"{ciclo['duration_ms']}ms")

if hablar:
    if "ultimo" in st.session_state:
        msg = cerebro.voice.hablar(st.session_state["ultimo"]["result"])
        st.info(msg)
    else: st.warning("Ejecuta una orden primero")

if exportar:
    if "ultimo" in st.session_state:
        txt = st.session_state["ultimo"]["result"]
        st.download_button("📥 Descargar Letra.txt", txt, "letra_omega.txt", "text/plain")
    else: st.warning("Ejecuta una orden primero")

st.divider()
st.subheader("∞ HISTORIAL DE CICLOS")
for c in cerebro.engine.recent_cycles(8)[::-1]:
    with st.expander(f"Ciclo {c['cycle']} | Score: {c['evaluation']['score']} | {c['evaluation']['quality']}"):
        st.text(c["result"][:300] + "...")
        st.caption(f"Input: {c['input']}")

st.divider()
st.subheader("🩺 DIAGNÓSTICO")
st.json(diag)

st.caption("CEREBRO OMEGA v3.0 - Para instalar voz: pip install pyttsx3")
