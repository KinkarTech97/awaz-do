import streamlit as st
import requests

# Page Setup
st.set_page_config(page_title="Awaz Do - AI Voice Hub", page_icon="🎙️", layout="centered")

st.title("🎙️ Awaz Do - The Local AI Hub")
st.markdown("**সম্পূর্ণ ফ্রিতে আপনার টেক্সট থেকে অডিও তৈরি করুন!**")
st.markdown("---")

# এখানে তোর কপি করা টোকেনটা বসাবি (ইনভার্টেড কমার ভেতরে)
HF_API_KEY = "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" 

# ভাষা এবং মডেল সিলেক্ট করার অপশন
st.header("১. ভাষা বেছে নিন")
models = {
    "বাংলা (Bengali)": "facebook/mms-tts-ben",
    "হিন্দি (Hindi)": "facebook/mms-tts-hin",
    "ইংরেজি (English)": "facebook/mms-tts-eng"
}
selected_lang = st.selectbox("কোন ভাষায় অডিও বানাতে চান?", list(models.keys()))
model_id = models[selected_lang]

# Hugging Face API URL
API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

st.markdown("---")
st.header("২. আপনার টেক্সট লিখুন")
text_input = st.text_area(
    "এখানে আপনার স্ক্রিপ্ট লিখুন:", 
    height=150, 
    placeholder="যেমন: মনের কিনারে বা বাংলার গল্পের নতুন ভিডিওর ভয়েসওভার..."
)

st.markdown("---")
if st.button("🎵 অডিও তৈরি করুন (Generate Audio)"):
    if HF_API_KEY == "এখানে_তোর_টোকেন_পেস্ট_করবি":
        st.error("⚠️ এডমিন নোটিশ: দয়া করে কোডের ভেতরে আপনার Hugging Face টোকেনটি বসান!")
    elif not text_input:
        st.warning("অনুগ্রহ করে টেক্সট বক্সে কিছু লিখুন!")
    else:
        with st.spinner("অডিও তৈরি হচ্ছে... একটু অপেক্ষা করুন..."):
            try:
                # Hugging Face-এ রিকোয়েস্ট পাঠানো
                response = requests.post(API_URL, headers=headers, json={"inputs": text_input})
                
                if response.status_code == 200:
                    st.success("🎉 আপনার অডিও সফলভাবে তৈরি হয়ে গেছে!")
                    # অডিও প্লেয়ার
                    st.audio(response.content, format="audio/flac")
                    
                    # ডাউনলোড বাটন
                    st.download_button(
                        label="📥 অডিও ডাউনলোড করুন",
                        data=response.content,
                        file_name="awaz_do_audio.flac",
                        mime="audio/flac"
                    )
                else:
                    st.error(f"❌ অডিও তৈরিতে সমস্যা হয়েছে। সার্ভার হয়তো ব্যস্ত আছে, একটু পরে আবার চেষ্টা করুন।")
            except Exception as e:
                st.error(f"❌ এরর: {e}")
                
