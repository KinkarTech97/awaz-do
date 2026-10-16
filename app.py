import asyncio
import re
import tempfile
from pathlib import Path

import edge_tts
import streamlit as st

st.set_page_config(
    page_title="Awaz Do — Natural Voice Studio",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Voice catalogue
# -----------------------------
VOICES = {
    "বাংলা (ভারত)": {
        "পুরুষ — Bashkar": "bn-IN-BashkarNeural",
        "মহিলা — Tanishaa": "bn-IN-TanishaaNeural",
    },
    "হিন্দি": {
        "পুরুষ — Madhur": "hi-IN-MadhurNeural",
        "মহিলা — Swara": "hi-IN-SwaraNeural",
    },
    "English (US)": {
        "Male — Andrew": "en-US-AndrewNeural",
        "Female — Jenny": "en-US-JennyNeural",
    },
    "English (UK)": {
        "Male — Ryan": "en-GB-RyanNeural",
        "Female — Sonia": "en-GB-SoniaNeural",
    },
    "তামিল": {
        "পুরুষ — Valluvar": "ta-IN-ValluvarNeural",
        "মহিলা — Pallavi": "ta-IN-PallaviNeural",
    },
    "তেলুগু": {
        "পুরুষ — Mohan": "te-IN-MohanNeural",
        "মহিলা — Shruti": "te-IN-ShrutiNeural",
    },
    "মারাঠি": {
        "পুরুষ — Manohar": "mr-IN-ManoharNeural",
        "মহিলা — Aarohi": "mr-IN-AarohiNeural",
    },
    "গুজরাটি": {
        "পুরুষ — Niranjan": "gu-IN-NiranjanNeural",
        "মহিলা — Dhwani": "gu-IN-DhwaniNeural",
    },
}

STYLES = {
    "স্বাভাবিক ও পরিষ্কার": {"rate": "+0%", "pitch": "+0Hz"},
    "ডকুমেন্টারি / গল্প বলা": {"rate": "-7%", "pitch": "-1Hz"},
    "গভীর ও ধীর": {"rate": "-12%", "pitch": "-3Hz"},
    "প্রাণবন্ত / এনার্জেটিক": {"rate": "+8%", "pitch": "+2Hz"},
    "নরম ও শান্ত": {"rate": "-5%", "pitch": "+1Hz"},
}

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');
      :root { --ink: #f7f8ff; --muted: #aab2cc; --line: rgba(255,255,255,.12); }
      .stApp {
        background: radial-gradient(ellipse at 12% 0%, rgba(110,67,255,.25), transparent 36%),
                    radial-gradient(ellipse at 88% 10%, rgba(0,208,190,.14), transparent 32%),
                    linear-gradient(145deg, #0a1020 0%, #10162b 50%, #0b1220 100%);
        color: var(--ink);
        font-family: 'Inter', 'Hind Siliguri', sans-serif;
      }
      [data-testid="stHeader"] { background: transparent; }
      [data-testid="stSidebar"] { background: rgba(8,14,28,.94); border-right: 1px solid var(--line); }
      [data-testid="stSidebar"] * { font-family: 'Inter', 'Hind Siliguri', sans-serif; }
      h1,h2,h3,p,span,label,div { font-family: 'Inter', 'Hind Siliguri', sans-serif; }
      .hero {
        border: 1px solid rgba(255,255,255,.14); border-radius: 26px;
        padding: 28px 30px; margin-bottom: 22px;
        background: linear-gradient(120deg, rgba(106,76,255,.22), rgba(0,210,190,.08)), rgba(255,255,255,.035);
        box-shadow: 0 20px 70px rgba(0,0,0,.18);
      }
      .eyebrow { color: #9cefe4; letter-spacing: 2px; font-size: 11px; font-weight: 800; text-transform: uppercase; }
      .hero h1 { font-size: clamp(30px, 5vw, 48px); line-height: 1.12; margin: 9px 0 10px; color: #fff; font-weight: 800; }
      .hero p { color: #c3cbe0; margin: 0; font-size: 15px; line-height: 1.7; max-width: 740px; }
      .pill-row { display:flex; gap:8px; flex-wrap:wrap; margin-top:18px; }
      .pill { border:1px solid rgba(255,255,255,.16); background:rgba(255,255,255,.06); color:#e8ecff; padding:6px 11px; border-radius:999px; font-size:12px; }
      .panel { background: rgba(255,255,255,.045); border:1px solid var(--line); border-radius:20px; padding:20px; }
      .section-title { font-size:19px; font-weight:800; color:#fff; margin:0 0 5px; }
      .subtle { color: #aab2cc; font-size: 13px; line-height:1.6; }
      .stButton > button, .stDownloadButton > button { border:0; border-radius:12px; min-height:46px; font-weight:800; color:#081321; background:linear-gradient(100deg,#a7f3e8,#9aaeff); box-shadow:0 8px 24px rgba(94,145,255,.18); }
      .stButton > button:hover, .stDownloadButton > button:hover { border:0; color:#081321; filter:brightness(1.06); }
      .stTextArea textarea, .stTextInput input { background:rgba(255,255,255,.055); color:#fff; border:1px solid rgba(255,255,255,.15); border-radius:13px; }
      [data-baseweb="select"] > div { background:rgba(255,255,255,.055); border-color:rgba(255,255,255,.15); border-radius:12px; }
      .metric-card { border:1px solid var(--line); background:rgba(255,255,255,.04); border-radius:15px; padding:14px 16px; height:100%; }
      .metric-big { font-size:22px; font-weight:800; color:#fff; }
      .metric-small { color:#aab2cc; font-size:12px; margin-top:4px; }
      .footer { text-align:center; color:#818ba8; font-size:12px; margin-top:30px; padding:12px; }
      .stAlert { border-radius:14px; }
      @media(max-width: 700px) { .hero { padding:22px 18px; } }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🎙️ Awaz Do")
    st.caption("Natural Voice Studio")
    st.divider()
    st.markdown("**আপনার স্টুডিও**")
    st.markdown("- ✍️ Text to Speech")
    st.markdown("- 🌏 একাধিক ভাষা")
    st.markdown("- 🎚️ Voice style controls")
    st.markdown("- ⬇️ MP3 ডাউনলোড")
    st.divider()
    st.caption("বর্তমান ইঞ্জিন: Microsoft Edge neural voices")
    st.caption("ইন্টারনেট সংযোগ প্রয়োজন।")

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">AI VOICE WORKSPACE</div>
      <h1>আপনার কথায় দিন<br>প্রাণের ছোঁয়া।</h1>
      <p>স্ক্রিপ্ট লিখুন, পছন্দের ভাষা ও কণ্ঠ বেছে নিন, তারপর অডিও তৈরি করে শুনুন। ভিডিও ন্যারেশন, গল্প, রিলস ও তথ্যভিত্তিক কনটেন্টের জন্য তৈরি।</p>
      <div class="pill-row"><span class="pill">বাংলা • হিন্দি • English</span><span class="pill">পুরুষ ও মহিলা কণ্ঠ</span><span class="pill">MP3 Export</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.45, 1], gap="large")

with left:
    st.markdown('<div class="section-title">✍️ আপনার স্ক্রিপ্ট</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">যে কথাগুলো ভয়েসে শুনতে চান, এখানে লিখুন বা পেস্ট করুন।</div>', unsafe_allow_html=True)
    sample = "নমস্কার বন্ধুরা। আজকের এই ভিডিওতে আপনাদের এমন একটি জায়গার গল্প শোনাব, যার সঙ্গে জড়িয়ে আছে অনেক অজানা কথা।"
    script = st.text_area(
        "স্ক্রিপ্ট",
        value=sample,
        height=260,
        max_chars=12000,
        label_visibility="collapsed",
        placeholder="এখানে আপনার বাংলা, হিন্দি বা ইংরেজি স্ক্রিপ্ট লিখুন...",
    )
    clean_script = script.strip()
    word_count = len(re.findall(r"\S+", clean_script)) if clean_script else 0
    char_count = len(clean_script)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-big">{word_count}</div><div class="metric-small">শব্দ</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-big">{char_count}</div><div class="metric-small">অক্ষর</div></div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-title">🎛️ ভয়েস সেটিংস</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtle">আপনার কনটেন্টের সঙ্গে মানানসই কণ্ঠ ও বলার ধরন বেছে নিন।</div>', unsafe_allow_html=True)
    language = st.selectbox("ভাষা", list(VOICES.keys()), index=0)
    voice_label = st.selectbox("কণ্ঠ", list(VOICES[language].keys()))
    style = st.selectbox("বলার ধরন", list(STYLES.keys()), index=1)
    volume = st.select_slider("ভলিউম", options=["-20%", "-10%", "+0%", "+10%", "+20%"], value="+0%")
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.info("টিপস: বাংলা ন্যারেশনে স্বাভাবিক ফল পেতে ছোট বাক্য লিখুন। কমা ও দাঁড়ি দিয়ে বিরতি বোঝান।", icon="💡")
    generate = st.button("✨ ভয়েস তৈরি করুন", use_container_width=True, type="primary")

if generate:
    if not clean_script:
        st.warning("আগে স্ক্রিপ্ট লিখুন, তারপর ভয়েস তৈরি করুন।")
    else:
        selected_voice = VOICES[language][voice_label]
        settings = STYLES[style]
        with st.spinner("আপনার অডিও তৈরি হচ্ছে… একটু অপেক্ষা করুন।"):
            try:
                async def make_audio(text: str, voice: str, rate: str, pitch: str, vol: str) -> bytes:
                    communicate = edge_tts.Communicate(
                        text=text,
                        voice=voice,
                        rate=rate,
                        pitch=pitch,
                        volume=vol,
                    )
                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                        output_path = Path(tmp.name)
                    try:
                        await communicate.save(str(output_path))
                        return output_path.read_bytes()
                    finally:
                        output_path.unlink(missing_ok=True)

                audio_bytes = asyncio.run(
                    make_audio(
                        clean_script,
                        selected_voice,
                        settings["rate"],
                        settings["pitch"],
                        volume,
                    )
                )
                st.session_state["awaz_audio"] = audio_bytes
                st.session_state["awaz_voice_name"] = f"{language} · {voice_label}"
                st.session_state["awaz_style_name"] = style
            except Exception as exc:
                st.error("অডিও তৈরি করা যায়নি। ইন্টারনেট সংযোগ পরীক্ষা করে আবার চেষ্টা করুন।")
                with st.expander("প্রযুক্তিগত তথ্য"):
                    st.code(str(exc))

if st.session_state.get("awaz_audio"):
    st.markdown("---")
    st.markdown('<div class="section-title">🎧 আপনার অডিও তৈরি</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="subtle">{st.session_state.get("awaz_voice_name", "Selected voice")} · {st.session_state.get("awaz_style_name", "Natural style")}</div>',
        unsafe_allow_html=True,
    )
    st.audio(st.session_state["awaz_audio"], format="audio/mp3")
    st.download_button(
        "⬇️ MP3 ডাউনলোড করুন",
        data=st.session_state["awaz_audio"],
        file_name="awaz-do-narration.mp3",
        mime="audio/mpeg",
        use_container_width=True,
    )

st.markdown("---")
with st.expander("ℹ️ এই সংস্করণে কী আছে এবং কী নেই?"):
    st.markdown(
        """
        **এখন কাজ করবে:** টেক্সট থেকে ভয়েস তৈরি, একাধিক ভারতীয় ভাষা, পুরুষ/মহিলা কণ্ঠের বিকল্প, বলার গতি ও পিচের প্রিসেট, অডিও প্লেব্যাক এবং MP3 ডাউনলোড।

        **এখনও যোগ করা হয়নি:** নিজের কণ্ঠ ক্লোন, লগইন/ইউজার অ্যাকাউন্ট, পাবলিক Voice Library এবং পেমেন্ট। কণ্ঠ ক্লোন করতে আলাদা AI মডেল ও যথেষ্ট সার্ভার রিসোর্স লাগে; এই সাধারণ Streamlit সংস্করণে সেটি চালু আছে বলে দাবি করা হচ্ছে না। অন্য কারও কণ্ঠ ব্যবহার বা ক্লোন করার আগে তাঁর স্পষ্ট অনুমতি নিন।

        **নোট:** ভয়েসগুলো অনলাইন সার্ভিসের মাধ্যমে তৈরি হয়, তাই কাজ করার জন্য ইন্টারনেট লাগবে এবং ভয়েসের প্রাপ্যতা বদলাতে পারে।
        """
    )

st.markdown('<div class="footer">Awaz Do — Natural Voice Studio · Made for storytellers and creators</div>', unsafe_allow_html=True)
