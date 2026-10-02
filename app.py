import streamlit as st
import asyncio
import edge_tts
import hashlib
from pathlib import Path

# Page Setup
st.set_page_config(page_title="Awaz Do - Voice Studio", page_icon="🎙️", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1e293b; }
    .sub-title { font-size: 1rem; color: #64748b; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🎙️ Awaz Do - Stable Studio</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>100% Working Voices. Fast and Crash-Free Version.</div>", unsafe_allow_html=True)

# 100% Working Voices Only
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
        placeholder="Type your text here...\n(Use '...' for natural pauses instead of commas)",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        chosen_language = st.selectbox("🌍 Language", list(VOICE_DATABASE.keys()))

    with col2:
        chosen_voice_name = st.selectbox("🎙️ Voice", list(VOICE_DATABASE[chosen_language].keys()))
        selected_voice_code = VOICE_DATABASE[chosen_language][chosen_voice_name]

    with col3:
        chosen_style = st.selectbox("🎭 Style", list(STYLE_PRESETS.keys()))

    generate_button = st.button("🎧 Generate Audio", type="primary", use_container_width=True)

async def render_audio(script_content, voice_id, preset, file_path):
    tts_engine = edge_tts.Communicate(
        text=script_content,
        voice=voice_id,
        rate=preset["rate"],
        pitch=preset["pitch"]
    )
    await tts_engine.save(file_path)

if generate_button:
    if not user_text.strip():
        st.warning("⚠️ Please enter some text first!")
    else:
        with st.status("🎙️ Generating audio...", expanded=True) as status_box:
            try:
                formatted_script = user_text.replace(",", "...").replace(";", "...")
                preset_values = STYLE_PRESETS[chosen_style]
                
                file_hash = hashlib.md5((formatted_script + selected_voice_code + str(preset_values)).encode("utf-8")).hexdigest()[:8]
                output_dir = Path("generated_audio")
                output_dir.mkdir(exist_ok=True)
                output_filename = output_dir / f"awaz_{file_hash}.mp3"

                asyncio.run(render_audio(formatted_script, selected_voice_code, preset_values, str(output_filename)))

                status_box.update(label="✅ Audio generated successfully!", state="complete")
                
                st.audio(str(output_filename), format="audio/mp3")
                with open(output_filename, "rb") as audio_data:
                    st.download_button(
                        label="📥 Download MP3",
                        data=audio_data,
                        file_name="awaz_do_audio.mp3",
                        mime="audio/mpeg",
                        use_container_width=True
                    )
            except Exception as e:
                status_box.update(label="❌ Generation failed", state="error")
                st.error(f"Error details: {e}")
                
