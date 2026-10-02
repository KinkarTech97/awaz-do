import streamlit as st
from gtts import gTTS
import os

# Page Configuration
st.set_page_config(
    page_title="Awaz Do - AI Voice Hub", 
    page_icon="🎙️", 
    layout="wide"
)

# Custom CSS for styling (Modern UI look)
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
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        text-align: center;
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
st.markdown("<div class='subtitle'>Convert your scripts into natural, high-quality audio instantly for your video projects. No API keys required, 100% free and stable.</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Main Studio Container (Card Style)
with st.container():
    st.markdown("### 📝 Enter Your Script")
    text_input = st.text_area(
        "Type or paste your text below:", 
        height=160, 
        placeholder="Example: Welcome to Moner Kinare... Today we are exploring new stories from Bengal..."
    )
    
    # Options Row
    c1, c2, c3 = st.columns([2, 2, 3])
    with c1:
        languages = {
            "Bengali (India)": "bn",
            "English (US)": "en",
            "Hindi": "hi"
        }
        selected_lang_name = st.selectbox("Select Language", list(languages.keys()))
        selected_lang_code = languages[selected_lang_name]
        
    with c2:
        voice_type = st.selectbox("Select Voice Profile", ["Standard Voice (AI)", "Clear Female Tone", "Deep Male Tone"])
        
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🎵 Generate Audio Now", use_container_width=True)

# Audio Generation Logic
if generate_btn:
    if not text_input.strip():
        st.warning("⚠️ Please enter some text in the box before generating audio!")
    else:
        with st.spinner("🔄 Generating your high-quality audio... Please wait..."):
            try:
                # Using gTTS for reliable, error-free voice generation
                tts = gTTS(text=text_input, lang=selected_lang_code)
                output_file = "generated_voice.mp3"
                tts.save(output_file)
                
                st.success("🎉 Audio generated successfully!")
                
                # Audio Player & Download
                st.audio(output_file, format="audio/mp3")
                
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📥 Download MP3 File",
                        data=f,
                        file_name="awaz_do_voiceover.mp3",
                        mime="audio/mp3",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

st.markdown("---")

# Feature Highlights Section (Matching the clean layout)
st.markdown("### Why Choose Awaz Do?")
f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("⚡ **Fast Processing**<br><span style='color: #64748B; font-size: 0.9rem;'>Generate audio files in just a few seconds.</span>", unsafe_allow_html=True)
with f2:
    st.markdown("🎙️ **Natural Sound**<br><span style='color: #64748B; font-size: 0.9rem;'>Smooth and clear voice output for videos.</span>", unsafe_allow_html=True)
with f3:
    st.markdown("🌍 **Multi-Language**<br><span style='color: #64748B; font-size: 0.9rem;'>Support for Bengali, English, Hindi and more.</span>", unsafe_allow_html=True)
with f4:
    st.markdown("📥 **Easy Export**<br><span style='color: #64748B; font-size: 0.9rem;'>Direct download in high-quality MP3 format.</span>", unsafe_allow_html=True)
    
