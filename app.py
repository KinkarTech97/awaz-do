import streamlit as st
import asyncio
import edge_tts
import os

# Page Setup
st.set_page_config(page_title="Awaz Do - Voice Studio", page_icon="🎙️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1e293b; }
    .sub-title { font-size: 1rem; color: #64748b; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🎙️ Awaz Do - Voice Studio</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Generate natural AI voices for free. 100% stable version.</div>", unsafe_allow_html=True)

# 100% Working Voices Only (Strictly 2 best voices per language)
VOICE_DATABASE = {
    "Bengali (India)": {
        "Bashkar (Deep Male)": "bn-IN-BashkarNeural",
        "Tanishaa (Soft Female)": "bn-IN-TanishaaNeural"
    },
    "Hindi (India)": {
        "Madhur (Rich Male)": "hi-IN-MadhurNeural",
        "Swara (Expressive Female)": "hi-IN-SwaraNeural"
    },
    "English (US)": {
        "Andrew (Cinematic Male)": "en-US-AndrewNeural",
        "Jenny (Storytelling Female)": "en-US-JennyNeural"
    }
}

# Stable Style Presets
STYLE_PRESETS = {
    "Normal Conversation": {"rate": "+0%", "pitch": "+0Hz"},
    "Documentary / Slow": {"rate": "-12%", "pitch": "-4Hz"},
    "Deep Suspense": {"rate": "-18%", "pitch": "-6Hz"}
}

# Main Workspace
with st.container():
    st.markdown("### 📝 Enter Your Script")
    user_text = st.text_area(
        label="Script Input",
        height=200,
        placeholder="Type or paste your text here...\n(Tip: Use '...' instead of commas for natural pauses in Bengali/Hindi)",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        chosen_language = st.selectbox("🌍 Select Language", list(VOICE_DATABASE.keys()))

    with col2:
        chosen_voice_name = st.selectbox("🎙️ Select Voice", list(VOICE_DATABASE[chosen_language].keys()))
        selected_voice_code = VOICE_DATABASE[chosen_language][chosen_voice_name]

    with col3:
        chosen_style = st.selectbox("🎭 Speaking Style", list(STYLE_PRESETS.keys()))

    generate_button = st.button("🎧 Generate Audio", type="primary", use_container_width=True)

# Async TTS Engine
async def render_audio(script_content, voice_id, preset, file_path):
    tts_engine = edge_tts.Communicate(
        text=script_content,
        voice=voice_id,
        rate=preset["rate"],
        pitch=preset["pitch"]
    )
    await tts_engine.save(file_path)

# Execution Logic
if generate_button:
    if not user_text.strip():
        st.warning("⚠️ Please enter some text first!")
    else:
        with st.status("🎙️ Generating audio... Please wait...", expanded=True) as status_box:
            try:
                # Replace commas to force pauses in Edge-TTS
                formatted_script = user_text.replace(",", "...").replace(";", "...")
                output_filename = "awaz_output.mp3"
                preset_values = STYLE_PRESETS[chosen_style]

                asyncio.run(render_audio(formatted_script, selected_voice_code, preset_values, output_filename))

                status_box.update(label="✅ Audio generated successfully!", state="complete")
                
                st.audio(output_filename, format="audio/mp3")
                with open(output_filename, "rb") as audio_data:
                    st.download_button(
                        label="📥 Download MP3",
                        data=audio_data,
                        file_name="awaz_do_final.mp3",
                        mime="audio/mpeg",
                        use_container_width=True
                    )

            except Exception as e:
                status_box.update(label="❌ Generation failed", state="error")
                st.error(f"Error: Make sure you are using Bengali font for Bengali voices, and English for English voices.\n\nDetails: {e}")
                
