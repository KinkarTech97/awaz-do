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
    """
    Converts normal text into SSML-like markup supported by edge-tts.
    Adds natural pauses around punctuation and paragraphs.
    """

    text = clean_text(text)

    paragraphs = re.split(r"\n\s*\n", text)

    processed_paragraphs = []

    for paragraph in paragraphs:

        # Escape XML-sensitive characters
        paragraph = html.escape(paragraph)

        # Existing punctuation gets subtle pauses
        paragraph = re.sub(
            r"([।!?])",
            rf"\1<break time='{sentence_pause}ms'/>",
            paragraph
        )

        # Bengali comma / English comma
        paragraph = re.sub(
            r"([,،])",
            r"\1<break time='180ms'/>",
            paragraph
        )

        # Colon / semicolon
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

<div style="height:
