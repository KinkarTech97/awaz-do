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

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
}

.hero {
    padding: 32px 10px 20px 10px;
}

.logo {
    font-size: 30px;
    font-weight: 800;
    color: #0f172a;
}

.logo span {
    color: #6366f1;
}

.badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 999px;
    background: #eef2ff;
    color: #4f46e5;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 15px;
}

.hero-title {
    font-size: clamp(36px, 5vw, 64px);
    line-height: 1.05;
    font-weight: 850;
    letter-spacing: -2px;
    color: #0f172a;
}

.hero-title span {
    background: linear-gradient(90deg,#4f46e5,#0891b2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    max-width: 760px;
    font-size: 18px;
    line-height: 1.7;
    color: #64748b;
    margin-top: 18px;
}

.card {
    background: rgba(255,255,255,.92);
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 15px 45px rgba(15,23,42,.07);
}

.voice-card {
    background: linear-gradient(145deg,#ffffff,#f8fafc);
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 10px;
}

.feature {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 20px;
    min-height: 145px;
}

.feature-icon {
    font-size: 27px;
}

.feature-title {
    font-weight: 750;
    color: #0f172a;
    margin-top: 8px;
}

.feature-text {
    color: #64748b;
    font-size: 14px;
    line-height: 1.55;
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #0f172a;
    margin-top: 35px;
}

.small-note {
    color: #64748b;
    font-size: 13px;
}

.stButton > button {
    border-radius: 13px;
    min-height: 46px;
    font-weight: 700;
}

div[data-testid="stTextArea"] textarea {
    border-radius: 16px;
    border: 1px solid #cbd5e1;
    font-size: 17px;
    line-height: 1.75;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# VOICES
# =========================================================

VOICES = {
    "Bengali (India)": {
        "👩 Tanishaa — Natural Female": "bn-IN-TanishaaNeural",
        "👨 Bashkar — Deep Male": "bn-IN-BashkarNeural",
    },

    "Hindi (India)": {
        "👩 Swara — Expressive Female": "hi-IN-SwaraNeural",
        "👩 Ananya — Natural Female": "hi-IN-AnanyaNeural",
        "👩 Aarti — Soft Female": "hi-IN-AartiNeural",
        "👩 Kavya — Modern Female": "hi-IN-KavyaNeural",
        "👨 Aarav — Natural Male": "hi-IN-AaravNeural",
        "👨 Arjun — Deep Male": "hi-IN-ArjunNeural",
        "👨 Kunal — Warm Male": "hi-IN-KunalNeural",
        "👨 Madhur — Rich Male": "hi-IN-MadhurNeural",
        "👨 Rehaan — Storytelling Male": "hi-IN-RehaanNeural",
    },

    "English (India)": {
        "👩 Aarti — Indian Female": "en-IN-AartiNeural",
        "👨 Prabhat — Indian Male": "en-IN-PrabhatNeural",
    },

    "English (US)": {
        "👩 Jenny — Natural Female": "en-US-JennyNeural",
        "👩 Aria — Expressive Female": "en-US-AriaNeural",
        "👨 Guy — Natural Male": "en-US-GuyNeural",
        "👨 Andrew — Warm Male": "en-US-AndrewNeural",
    }
}

# =========================================================
# STORY PRESETS
# =========================================================

PRESETS = {
    "🎙️ Natural": {
        "rate": "-3%",
        "pitch": "0Hz",
        "volume": "+0%",
        "sentence_pause": 300,
        "paragraph_pause": 650
    },

    "📖 Historical Story": {
        "rate": "-14%",
        "pitch": "-2Hz",
        "volume": "+0%",
        "sentence_pause": 520,
        "paragraph_pause": 1150
    },

    "🌙 Slow Storytelling": {
        "rate": "-18%",
        "pitch": "-1Hz",
        "volume": "+0%",
        "sentence_pause": 650,
        "paragraph_pause": 1350
    },

    "🎬 Cinematic": {
        "rate": "-9%",
        "pitch": "-2Hz",
        "volume": "+0%",
        "sentence_pause": 470,
        "paragraph_pause": 1000
    },

    "📰 Documentary": {
        "rate": "-7%",
        "pitch": "-1Hz",
        "volume": "+0%",
        "sentence_pause": 380,
        "paragraph_pause": 850
    },

    "💬 Conversational": {
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+0%",
        "sentence_pause": 260,
        "paragraph_pause": 550
    },

    "😌 Calm": {
        "rate": "-10%",
        "pitch": "+0Hz",
        "volume": "-1%",
        "sentence_pause": 500,
        "paragraph_pause": 950
    }
}

# =========================================================
# TEXT PROCESSING
# =========================================================

def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def prepare_story_text(text, sentence_pause, paragraph_pause):
    text = clean_text(text)
    paragraphs = re.split(r"\n\s*\n", text)
    processed_paragraphs = []
    for paragraph in paragraphs:
        paragraph = html.escape(paragraph)
        paragraph = re.sub(
            r"([।!?])",
            rf"\1<break time='{sentence_pause}ms'/>",
            paragraph
        )
        paragraph = re.sub(
            r"([,،])",
            r"\1<break time='180ms'/>",
            paragraph
        )
        paragraph = re.sub(
            r"([:;])",
            r"\1<break time='260ms'/>",
            paragraph
        )
        processed_paragraphs.append(paragraph)

    return (
        f"<speak version='1.0' "
        f"xmlns='http://www.w3.org/2001/10/synthesis' "
        f"xml:lang='bn-IN'>"
        f"<prosody>"
        + f"<break time='{paragraph_pause}ms'/>".join(processed_paragraphs)
        + "</prosody></speak>"
    )


# =========================================================
# ASYNC TTS
# =========================================================

async def generate_audio(text, voice, output_file, preset):
    rate = preset["rate"]
    pitch = preset["pitch"]
    volume = preset["volume"]
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=rate,
        volume=volume,
        pitch=pitch
    )
    await communicate.save(output_file)


# =========================================================
# UI
# =========================================================

st.markdown("""
<div class="hero">

<div class="logo">🎙️ <span>Awaz Do</span></div>

<div style="height:22px"></div>

<div class="badge">AI NATURAL VOICE STUDIO</div>

<div class="hero-title">
Turn Your Words Into<br>
<span>Natural Human-Like Voice.</span>
</div>

<div class="hero-sub">
বাংলা, হিন্দি ও ইংরেজি লেখাকে গল্প, ডকুমেন্টারি,
সিনেমাটিক অথবা স্বাভাবিক কথার মতো voice-এ রূপান্তর করুন।
</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# MAIN STUDIO
# =========================================================

st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("### 📝 আপনার Script লিখুন")

text_input = st.text_area(
    "Script",
    height=230,
    label_visibility="collapsed",
    placeholder=(
        "উদাহরণ:\n\n"
        "আজ থেকে প্রায় একশো বছর আগে...\n"
        "এই জায়গাটা ছিল সম্পূর্ণ অন্যরকম।\n\n"
        "চারপাশে ছিল নদী, জঙ্গল আর নিস্তব্ধতা।"
    )
)

st.markdown("")

c1, c2, c3 = st.columns(3)

with c1:
    language = st.selectbox(
        "🌍 Language",
        list(VOICES.keys())
    )

with c2:
    voice_name = st.selectbox(
        "🎙️ Voice",
        list(VOICES[language].keys())
    )

with c3:
    preset_name = st.selectbox(
        "🎭 Speaking Style",
        list(PRESETS.keys())
    )

st.markdown("")

# =========================================================
# ADVANCED SETTINGS
# =========================================================

with st.expander("⚙️ Advanced Voice Controls"):

    preset = PRESETS[preset_name]

    a1, a2, a3 = st.columns(3)

    with a1:
        speed = st.slider(
            "Speaking Speed",
            min_value=-30,
            max_value=20,
            value=int(preset["rate"].replace("%", "").replace("+", "")),
            step=1,
            help="Negative value = slower speech"
        )

    with a2:
        pitch = st.slider(
            "Voice Pitch",
            min_value=-10,
            max_value=10,
            value=int(preset["pitch"].replace("Hz", "").replace("+", "")),
            step=1
        )

    with a3:
        volume = st.slider(
            "Volume",
            min_value=-10,
            max_value=10,
            value=int(preset["volume"].replace("%", "").replace("+", "")),
            step=1
        )

    p1, p2 = st.columns(2)

    with p1:
        sentence_pause = st.slider(
            "Sentence Pause (ms)",
            100,
            1200,
            int(preset["sentence_pause"]),
            50
        )

    with p2:
        paragraph_pause = st.slider(
            "Paragraph Pause (ms)",
            300,
            2500,
            int(preset["paragraph_pause"]),
            50
        )

# =========================================================
# INFO
# =========================================================

word_count = len(text_input.split()) if text_input.strip() else 0
char_count = len(text_input)

st.markdown(
    f"""
    <div class="small-note">
    {word_count:,} words &nbsp; • &nbsp;
    {char_count:,} characters
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("")

generate = st.button(
    "🎧  Generate Natural Voice",
    type="primary",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# GENERATE
# =========================================================

if generate:
    if not text_input.strip():
        st.warning("⚠️ আগে কিছু text লিখুন, তারপর Generate Natural Voice চাপুন।")
    else:
        selected_voice = VOICES[language][voice_name]

        final_preset = {
            "rate": f"{speed:+d}%",
            "pitch": f"{pitch:+d}Hz",
            "volume": f"{volume:+d}%",
            "sentence_pause": sentence_pause,
            "paragraph_pause": paragraph_pause
        }

        file_hash = hashlib.md5(
            (text_input + selected_voice + str(final_preset)).encode("utf-8")
        ).hexdigest()[:12]

        output_dir = Path("generated_audio")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"awaz_do_{file_hash}.mp3"

        with st.status("🎙️ Creating natural voice...", expanded=True) as status:
            st.write("Analyzing script...")
            st.write(f"Voice: {voice_name}")
            st.write(f"Style: {preset_name}")
            st.write("Applying natural pacing...")

            try:
                asyncio.run(
                    generate_audio(
                        text_input,
                        selected_voice,
                        str(output_file),
                        final_preset
                    )
                )

                status.update(label="✅ Voice generated successfully!", state="complete")

            except Exception as e:
                status.update(label="❌ Voice generation failed", state="error")
                st.error(str(e))
                st.stop()

        # =================================================
        # AUDIO RESULT
        # =================================================
        st.markdown("")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🎧 Your Natural Voice")
        st.audio(str(output_file), format="audio/mp3")

        with open(output_file, "rb") as audio_file:
            st.download_button(
                "📥 Download MP3",
                data=audio_file,
                file_name="awaz_do_natural_voice.mp3",
                mime="audio/mpeg",
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FEATURES
# =========================================================

st.markdown('<div class="section-title">Why Awaz Do?</div>', unsafe_allow_html=True)
st.markdown("")

f1, f2, f3, f4 = st.columns(4)

features = [
    ("🎙️", "Natural Neural Voice", "Neural voices designed for smoother and more human-like speech."),
    ("📖", "Storytelling Mode", "Slow pacing and longer pauses for historical stories and documentaries."),
    ("🎭", "Multiple Styles", "Natural, cinematic, documentary, calm and conversational delivery."),
    ("📥", "MP3 Export", "Generate an audio file ready for video editing and content creation.")
]

for col, feature in zip([f1, f2, f3, f4], features):
    with col:
        st.markdown(
            f"""
            <div class="feature">
            <div class="feature-icon">{feature[0]}</div>
            <div class="feature-title">{feature[1]}</div>
            <div class="feature-text">{feature[2]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# FOOTER
# =========================================================

st.markdown("")
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#94a3b8;font-size:13px;">
    🎙️ Awaz Do — Natural Voice Studio
    </div>
    """,
    unsafe_allow_html=True
            )
