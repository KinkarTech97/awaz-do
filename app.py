import streamlit as st
import asyncio
import edge_tts
import os
import re
import html
import hashlib
from pathlib import Path

# =========================================================
# AWAZ DO — NATURAL VOICE STUDIO
# =========================================================

st.set_page_config(
    page_title="Awaz Do — Natural Voice Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.10), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(14,165,233,.08), transparent 28%),
        #f8fafc;
}
.block-container { max-width: 1250px; padding-top: 2rem; }
.hero { padding: 32px 10px 20px 10px; }
.logo { font-size: 30px; font-weight: 800; color: #0f172a; }
.logo span { color: #6366f1; }
.badge {
    display: inline-block; padding: 7px 13px; border-radius: 999px;
    background: #eef2ff; color: #4f46e5; font-size: 13px; font-weight: 700; margin-bottom: 15px;
}
.hero-title { font-size: clamp(36px, 5vw, 64px); line-height: 1.05; font-weight: 850; letter-spacing: -2px; color: #0f172a; }
.hero-title span { background: linear-gradient(90deg,#4f46e5,#0891b2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.card { background: rgba(255,255,255,.92); border: 1px solid #e2e8f0; border-radius: 24px; padding: 24px; box-shadow: 0 15px 45px rgba(15,23,42,.07); }
</style>
""", unsafe_allow_html=True)

# =========================================================
# REAL WORKING VOICES ONLY (No Fake Names)
# =========================================================

VOICES = {
    "Bengali (India)": {
        "👨 Bashkar — Deep & Heavy Male": "bn-IN-BashkarNeural",
        "👩 Tanishaa — Soft Natural Female": "bn-IN-TanishaaNeural"
    },
    "Hindi (India)": {
        "👨 Madhur — Cinematic Rich Male": "hi-IN-MadhurNeural",
        "👩 Swara — Expressive Female": "hi-IN-SwaraNeural"
    },
    "English (US)": {
        "👨 Andrew — Warm Cinematic Male": "en-US-AndrewNeural",
        "👩 Jenny — Natural Storytelling Female": "en-US-JennyNeural"
    }
}

# =========================================================
# STORY PRESETS (Analyzed from your audio)
# =========================================================

PRESETS = {
    "🎬 Documentary (Banty Style)": {
        "rate": "-14%",
        "pitch": "-5Hz",
        "volume": "+0%",
        "sentence_pause": 550,
        "paragraph_pause": 1200
    },
    "🎙️ Natural Conversation": {
        "rate": "-2%",
        "pitch": "0Hz",
        "volume": "+0%",
        "sentence_pause": 300,
        "paragraph_pause": 650
    },
    "🌙 Deep Suspense Story": {
        "rate": "-18%",
        "pitch": "-7Hz",
        "volume": "+0%",
        "sentence_pause": 700,
        "paragraph_pause": 1500
    }
}

# =========================================================
# TEXT PROCESSING
# =========================================================

def prepare_story_text(text, sentence_pause, paragraph_pause):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    
    paragraphs = re.split(r"\n\s*\n", text)
    processed_paragraphs = []
    
    for paragraph in paragraphs:
        paragraph = html.escape(paragraph)
        paragraph = re.sub(r"([।!?])", rf"\1<break time='{sentence_pause}ms'/>", paragraph)
        paragraph = re.sub(r"([,،])", r"\1<break time='200ms'/>", paragraph)
        paragraph = re.sub(r"(\.\.\.)", r"\1<break time='400ms'/>", paragraph)
        processed_paragraphs.append(paragraph)

    return (
        f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='bn-IN'>"
        f"<prosody>" + f"<break time='{paragraph_pause}ms'/>".join(processed_paragraphs) + "</prosody></speak>"
    )

async def generate_audio(text, voice, output_file, preset):
    communicate = edge_tts.Communicate(
        text, voice, rate=preset["rate"], volume=preset["volume"], pitch=preset["pitch"]
    )
    await communicate.save(output_file)

# =========================================================
# UI
# =========================================================

st.markdown('<div class="hero"><div class="logo">🎙️ <span>Awaz Do</span></div><br><div class="badge">AI NATURAL VOICE STUDIO</div><div class="hero-title">Turn Your Words Into<br><span>Natural Human-Like Voice.</span></div></div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📝 আপনার Script লিখুন")

text_input = st.text_area(
    "Script",
    height=250,
    label_visibility="collapsed",
    placeholder="এখানে আপনার টেক্সট লিখুন...",
    value="চক্রতীর্থের গল্পের আরও একটি গুরুত্বপূর্ণ অধ্যায় রয়েছে...\nএই স্থানটি দীর্ঘদিন ধরেই পরিচিত তার প্রাচীন মহাশ্মশানের জন্য।\n\nনীরব পরিবেশে শেষ বিদায়ের সেই মুহূর্ত... চক্রতীর্থের বর্তমান জীবনেরও একটি গুরুত্বপূর্ণ অংশ।"
)

c1, c2, c3 = st.columns(3)
with c1:
    language = st.selectbox("🌍 Language", list(VOICES.keys()))
with c2:
    voice_name = st.selectbox("🎙️ Voice", list(VOICES[language].keys()))
with c3:
    preset_name = st.selectbox("🎭 Speaking Style", list(PRESETS.keys()))

with st.expander("⚙️ Advanced Voice Controls (Manual Fine-tuning)"):
    preset = PRESETS[preset_name]
    a1, a2, a3 = st.columns(3)
    with a1:
        speed = st.slider("Speaking Speed", -30, 20, int(preset["rate"].replace("%", "").replace("+", "")))
    with a2:
        pitch = st.slider("Voice Pitch", -15, 10, int(preset["pitch"].replace("Hz", "").replace("+", "")))
    with a3:
        volume = st.slider("Volume", -10, 10, int(preset["volume"].replace("%", "").replace("+", "")))
    
    p1, p2 = st.columns(2)
    with p1:
        sentence_pause = st.slider("Sentence Pause (ms)", 100, 1500, int(preset["sentence_pause"]), 50)
    with p2:
        paragraph_pause = st.slider("Paragraph Pause (ms)", 300, 3000, int(preset["paragraph_pause"]), 50)

generate = st.button("🎧 Generate Natural Voice", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if generate:
    if not text_input.strip():
        st.warning("⚠️ আগে কিছু text লিখুন।")
    else:
        selected_voice = VOICES[language][voice_name]
        final_preset = {
            "rate": f"{speed:+d}%", "pitch": f"{pitch:+d}Hz", "volume": f"{volume:+d}%",
            "sentence_pause": sentence_pause, "paragraph_pause": paragraph_pause
        }
        
        file_hash = hashlib.md5((text_input + selected_voice + str(final_preset)).encode("utf-8")).hexdigest()[:12]
        output_dir = Path("generated_audio")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"awaz_do_{file_hash}.mp3"

        with st.status("🎙️ Creating emotional voice...", expanded=True) as status:
            try:
                # The fake text-formatting trick for Edge-TTS
                script_to_process = text_input.replace(",", "...").replace(";", "...")
                asyncio.run(generate_audio(script_to_process, selected_voice, str(output_file), final_preset))
                status.update(label="✅ Voice generated successfully!", state="complete")
            except Exception as e:
                status.update(label="❌ Generation failed", state="error")
                st.error(str(e))
                st.stop()

        st.markdown('<br><div class="card">### 🎧 Your Generated Voice', unsafe_allow_html=True)
        st.audio(str(output_file), format="audio/mp3")
        with open(output_file, "rb") as audio_file:
            st.download_button("📥 Download MP3", data=audio_file, file_name="documentary_voice.mp3", mime="audio/mpeg", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
