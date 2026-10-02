import streamlit as st
import asyncio
import edge_tts
import os

# Page Setup
st.set_page_config(page_title="Awaz Do — Voice Studio", page_icon="🎙️", layout="wide")

# Custom Design
st.markdown("""
    <style>
    .main-title { font-size: 2.2rem; font-weight: 800; color: #1e293b; }
    .sub-title { font-size: 1rem; color: #64748b; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='main-title'>🎙️ Awaz Do — AI Voice Studio</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>যেকোনো ভাষার ভয়েস বেছে নিয়ে এক্সপেরিমেন্ট করুন।</div>", unsafe_allow_html=True)

# ALL Voices Unlocked in a Single Menu
ALL_VOICES = {
    "👨 ভাস্কর (Bengali - Deep Male)": "bn-IN-BashkarNeural",
    "👩 তানিশা (Bengali - Soft Female)": "bn-IN-TanishaaNeural",
    "👨 প্রদীপ (Bengali BD - Clear Male)": "bn-BD-PradeepNeural",
    "👩 নবনীতা (Bengali BD - Natural Female)": "bn-BD-NabanitaNeural",
    "👨 मधुर / Madhur (Hindi - Rich Male)": "hi-IN-MadhurNeural",
    "👩 स्वरा / Swara (Hindi - Expressive Female)": "hi-IN-SwaraNeural",
    "👨 Andrew (English US - Cinematic Male)": "en-US-AndrewNeural",
    "👩 Jenny (English US - Storytelling Female)": "en-US-JennyNeural",
}

# Style Presets
STYLE_PRESETS = {
    "🎬 Documentary (গম্ভীর ও ধীর)": {"rate": "-14%", "pitch": "-4Hz"},
    "🎙️ Normal (স্বাভাবিক)": {"rate": "+0%", "pitch": "+0Hz"},
    "🌙 Suspense (রহস্য)": {"rate": "-18%", "pitch": "-6Hz"}
}

# Main Workspace
with st.container():
    st.markdown("### 📝 আপনার স্ক্রিপ্ট লিখুন")
    user_text = st.text_area(
        label="Script Input",
        height=180,
        placeholder="বাংলা বা ইংরেজি অক্ষরে (Benglish) স্ক্রিপ্ট লিখুন...\n(বিঃদ্রঃ ইংরেজি/হিন্দি ভয়েস দিয়ে বাংলা বলাতে চাইলে 'Ami bhalo achi' স্টাইলে লিখুন)",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        chosen_voice_name = st.selectbox("🎙️ যেকোনো ভয়েস বেছে নিন (Cross-lingual test)", list(ALL_VOICES.keys()))
        selected_voice_code = ALL_VOICES[chosen_voice_name]
    with col2:
        chosen_style = st.selectbox("🎭 বাচনভঙ্গি", list(STYLE_PRESETS.keys()))

    generate_button = st.button("🎧 অডিও তৈরি করুন", type="primary", use_container_width=True)

# TTS Generation Function
async def render_audio(script_content, voice_id, preset, file_path):
    tts_engine = edge_tts.Communicate(
        text=script_content,
        voice=voice_id,
        rate=preset["rate"],
        pitch=preset["pitch"]
    )
    await tts_engine.save(file_path)

# Button Execution
if generate_button:
    if not user_text.strip():
        st.warning("⚠️ অনুগ্রহ করে আগে কিছু টেক্সট লিখুন!")
    else:
        with st.status("🎙️ ভয়েস জেনারেট হচ্ছে...", expanded=True) as status_box:
            try:
                formatted_script = user_text.replace(",", "...").replace(";", "...")
                output_filename = "awaz_output.mp3"
                preset_values = STYLE_PRESETS[chosen_style]

                asyncio.run(render_audio(formatted_script, selected_voice_code, preset_values, output_filename))

                status_box.update(label="✅ অডিও তৈরি সম্পন্ন হয়েছে!", state="complete")
                
                st.audio(output_filename, format="audio/mp3")
                with open(output_filename, "rb") as audio_data:
                    st.download_button("📥 ডাউনলোড করুন (MP3)", data=audio_data, file_name="awaz_do_voice.mp3", mime="audio/mpeg")

            except Exception as error_msg:
                status_box.update(label="❌ কোনো সমস্যা হয়েছে", state="error")
                st.error(f"Error: হতে পারে আপনি ইংরেজি ভয়েস দিয়ে সরাসরি বাংলা ফন্ট (অ,আ) পড়ানোর চেষ্টা করছেন। ইংরেজি ভয়েসের জন্য ইংরেজি অক্ষরে (Benglish) লিখুন।\n\nDetails: {error_msg}")
                
