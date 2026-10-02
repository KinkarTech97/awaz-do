import streamlit as st
import asyncio
import edge_tts
import os

# Page Configuration
st.set_page_config(
    page_title="Awaz Do - AI Voice Hub", 
    page_icon="🎙️", 
    layout="wide"
)

# Custom CSS for Modern UI
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E293B;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #64748B;
    }
    </style>
""", unsafe_allow_html=True)

# Top Navigation Simulation
col_logo, col_nav = st.columns([2, 5])
with col_logo:
    st.markdown("### 🎙️ Awaz Do")
with col_nav:
    st.markdown("<p style='text-align: right; color: #64748B; font-weight: 500;'>Home &nbsp;&nbsp;|&nbsp;&nbsp; How it Works &nbsp;&nbsp;|&nbsp;&nbsp; Voice List &nbsp;&nbsp;|&nbsp;&nbsp; Contact</p>", unsafe_allow_html=True)

st.markdown("---")

# Hero Section
st.markdown("<div class='main-title'>Transform Your Text Into Lifelike AI Voices</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Convert your scripts into ultra-realistic, studio-quality audio instantly. Powered by Advanced AI, 100% Free and Stable.</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Main Studio Container
with st.container():
    st.markdown("### 📝 Enter Your Script")
    text_input = st.text_area(
        "Type or paste your text below:", 
        height=160, 
        placeholder="Example: নমস্কার, 'মনের কিনারে' পেজে আপনাদের স্বাগত... আজ আমরা শোনাব এক অদ্ভুত রহস্যের গল্প..."
    )
    
    # Options Row (Language & Voice Selection)
    c1, c2, c3 = st.columns([2, 2, 3])
    with c1:
        lang_option = st.selectbox(
            "Select Language", 
            ["Bengali (India)", "English (US)", "Hindi (India)"]
        )
        
    with c2:
        # Dynamic Voices based on language selection
        if "Bengali" in lang_option:
            voices = {
                "Madhumita (Natural Female)": "bn-IN-TanishaNeural",
                "Bashkar (Deep Male)": "bn-IN-BashkarNeural"
            }
        elif "Hindi" in lang_option:
            voices = {
                "Swara (Natural Female)": "hi-IN-SwaraNeural",
                "Madhur (Deep Male)": "hi-IN-MadhurNeural"
            }
        else:
            voices = {
                "Ana (Natural Female - US)": "en-US-AnaNeural",
                "Andrew (Deep Male - US)": "en-US-AndrewNeural",
                "Emma (Professional Female)": "en-US-EmmaNeural"
            }
            
        selected_voice_name = st.selectbox("Select Voice Profile", list(voices.keys()))
        selected_voice_code = voices[selected_voice_name]
        
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🎵 Generate Studio Audio", use_container_width=True)

# Async function to generate edge-tts audio
async def generate_edge_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

# Audio Generation Logic
if generate_btn:
    if not text_input.strip():
        st.warning("⚠️ Please enter some text in the box before generating audio!")
    else:
        with st.spinner("🎙️ Generating ultra-realistic studio voice... Please wait..."):
            try:
                output_file = "studio_output.mp3"
                # Run async function in Streamlit
                asyncio.run(generate_edge_audio(text_input, selected_voice_code, output_file))
                
                st.success("🎉 Studio-quality audio generated successfully!")
                
                # Audio Player & Download
                st.audio(output_file, format="audio/mp3")
                
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📥 Download High-Quality MP3",
                        data=f,
                        file_name="awaz_do_studio_voice.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

st.markdown("---")

# Feature Highlights Section
st.markdown("### Why Choose Awaz Do Studio?")
f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("⚡ **Ultra Fast**<br><span style='color: #64748B; font-size: 0.9rem;'>Instant neural voice rendering.</span>", unsafe_allow_html=True)
with f2:
    st.markdown("🎙️ **Studio Quality**<br><span style='color: #64748B; font-size: 0.9rem;'>Deep, expressive, and human-like tones.</span>", unsafe_allow_html=True)
with f3:
    st.markdown("🌍 **Multi-Lingual**<br><span style='color: #64748B; font-size: 0.9rem;'>Native accents in Bengali, English, Hindi.</span>", unsafe_allow_html=True)
with f4:
    st.markdown("📥 **Direct Export**<br><span style='color: #64748B; font-size: 0.9rem;'>Clean MP3 files ready for video editing.</span>", unsafe_allow_html=True)
    
