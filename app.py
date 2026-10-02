import streamlit as st
import edge_tts
import asyncio
import tempfile
import os
from pathlib import Path

# ====================== Page Config ======================
st.set_page_config(
    page_title="Awaj Dao - Text to Speech",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====================== Custom CSS (Color Theme) ======================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: white;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a, #4c1d95);
        padding: 1rem 2rem;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    /* Title */
    .big-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Card */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4);
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background-color: #1e293b !important;
        color: white !important;
        border-radius: 10px !important;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        height: 100%;
    }
    
    h1, h2, h3, h4, p, label {
        color: #f1f5f9 !important;
    }
</style>
""", unsafe_allow_html=True)

# ====================== Voice Lists ======================
VOICES = {
    "Bengali": {
        "Sadia (Female - Bangladesh)": "bn-BD-NabanitaNeural",
        "Pradeep (Male - Bangladesh)": "bn-BD-PradeepNeural",
        "Tanishaa (Female - India)": "bn-IN-TanishaaNeural",
        "Bashkar (Male - India)": "bn-IN-BashkarNeural",
    },
    "Hindi": {
        "Swara (Female)": "hi-IN-SwaraNeural",
        "Madhur (Male)": "hi-IN-MadhurNeural",
        "Ananya (Female)": "hi-IN-AnanyaNeural",
        "Aarav (Male)": "hi-IN-AaravNeural",
    },
    "English": {
        "Jenny (Female - US)": "en-US-JennyNeural",
        "Guy (Male - US)": "en-US-GuyNeural",
        "Aria (Female - US)": "en-US-AriaNeural",
        "Davis (Male - US)": "en-US-DavisNeural",
        "Neerja (Female - India)": "en-IN-NeerjaNeural",
        "Prabhat (Male - India)": "en-IN-PrabhatNeural",
        "Sonia (Female - UK)": "en-GB-SoniaNeural",
        "Ryan (Male - UK)": "en-GB-RyanNeural",
    }
}

# ====================== TTS Function ======================
async def generate_speech(text: str, voice: str, rate: str = "+0%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp_path = tmp.name
    await communicate.save(tmp_path)
    return tmp_path

# ====================== UI ======================
# Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; align-items: center; gap: 15px;">
        <div style="font-size: 2.5rem;">🎙️</div>
        <div>
            <h1 style="margin:0; font-size: 1.8rem; color: white;">Awaj Dao</h1>
            <p style="margin:0; color: #94a3b8; font-size: 0.9rem;">Audio Made Easy</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Hero Section
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown('<div class="big-title">Awaj Dao</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size: 1.25rem; color: #cbd5e1; margin-bottom: 1.5rem;">
        Convert your text into natural & realistic AI voices in <b>Bengali, Hindi & English</b>
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="display: flex; gap: 20px; margin-bottom: 2rem;">
        <span style="color: #4ade80;">✓ Easy to use</span>
        <span style="color: #4ade80;">✓ Multiple languages & voices</span>
        <span style="color: #4ade80;">✓ Fast & Free</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; font-size: 8rem; opacity: 0.9;">
        🎤
    </div>
    """, unsafe_allow_html=True)

# ====================== Main Input Card ======================
st.markdown("### ✍️ Enter Your Text")

text = st.text_area(
    label="Your text here",
    placeholder="Example: Hello, welcome to Awaj Dao platform...",
    height=150,
    max_chars=3000,
    label_visibility="collapsed"
)

# Controls
col_lang, col_voice, col_speed, col_btn = st.columns([1.2, 1.5, 1.2, 1.3])

with col_lang:
    language = st.selectbox("🌐 Language", list(VOICES.keys()), index=0)

with col_voice:
    voice_name = st.selectbox("👤 Voice", list(VOICES[language].keys()))

with col_speed:
    speed = st.slider("⚡ Speed", 0.5, 1.5, 1.0, 0.1)
    rate = f"{int((speed - 1) * 100):+d}%"

with col_btn:
    st.write("")  # spacing
    st.write("")
    generate_btn = st.button("▶ Generate Audio", use_container_width=True)

# ====================== Generate ======================
if generate_btn:
    if not text.strip():
        st.warning("Please enter some text!")
    else:
        with st.spinner("Generating natural voice... Please wait"):
            selected_voice = VOICES[language][voice_name]
            try:
                audio_path = asyncio.run(generate_speech(text, selected_voice, rate))
                
                st.success("✅ Audio generated successfully!")
                
                # Audio player
                st.audio(audio_path, format="audio/mp3")
                
                # Download button
                with open(audio_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download MP3",
                        data=f,
                        file_name=f"awaj_dao_{language.lower()}.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
                
                # Clean up
                os.unlink(audio_path)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ====================== Features Section ======================
st.markdown("---")
st.markdown("### Why Awaj Dao?")
st.markdown("<p style='color:#94a3b8;'>The best free solution to convert your text into audio</p>", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2rem;">⭐</div>
        <h4>High Quality</h4>
        <p style="color:#94a3b8; font-size:0.9rem;">Premium neural voices that sound natural</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2rem;">⚡</div>
        <h4>Fast Processing</h4>
        <p style="color:#94a3b8; font-size:0.9rem;">Generate audio in seconds</p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2rem;">🔒</div>
        <h4>Private & Secure</h4>
        <p style="color:#94a3b8; font-size:0.9rem;">Your text stays safe</p>
    </div>
    """, unsafe_allow_html=True)

with f4:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 2rem;">❤️</div>
        <h4>For Everyone</h4>
        <p style="color:#94a3b8; font-size:0.9rem;">Students, creators, businesses</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    Made with ❤️ using Microsoft Neural Voices • Completely Free
</div>
""", unsafe_allow_html=True)
