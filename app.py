
import streamlit as st
import requests

# ওয়েবসাইটের নাম এবং ডিজাইন সেটআপ
st.set_page_config(page_title="Awaz Do - AI Voice Cloning", page_icon="🎙️", layout="centered")

st.title("🎙️ Awaz Do - The Local AI Tool")
st.markdown("আপনার নিজের ভয়েস ক্লোন করুন এবং টেক্সট থেকে অডিও (TTS) তৈরি করুন মাত্র কয়েক সেকেন্ডে!")

# সাইডবারে API Key দেওয়ার জায়গা
st.sidebar.header("🔑 API Key সেটআপ")
api_key = st.sidebar.text_input("ElevenLabs API Key দিন:", type="password")
st.sidebar.markdown("*[ElevenLabs.io থেকে আপনার API Key সংগ্রহ করুন]*")
st.sidebar.markdown("---")
st.sidebar.info("ভয়েস ক্লোনিং ফিচারটি ব্যবহার করতে ElevenLabs-এর API Key থাকা বাধ্যতামূলক।")

# দুটো আলাদা অপশন (Tab) তৈরি করা
tab1, tab2 = st.tabs(["🗣️ নতুন ভয়েস ক্লোন করুন", "🔊 টেক্সট থেকে অডিও (TTS)"])

# ----------------- Tab 1: ভয়েস ক্লোনিং -----------------
with tab1:
    st.header("আপনার ভয়েস আপলোড করুন")
    st.write("যেকোনো মানুষের পরিষ্কার ১-৫ মিনিটের অডিও আপলোড করে তার ডিজিটাল ভয়েস তৈরি করুন।")
    
    voice_name = st.text_input("ভয়েসের একটি নাম দিন (যেমন: Kinkar's Voice):")
    voice_desc = st.text_input("ভয়েসের বিবরণ (ঐচ্ছিক):")
    uploaded_files = st.file_uploader("অডিও ফাইল আপলোড করুন (mp3/wav/m4a):", type=['mp3', 'wav', 'm4a'], accept_multiple_files=True)
    
    if st.button("🚀 ভয়েস ক্লোন তৈরি করুন"):
        if not api_key:
            st.error("অনুগ্রহ করে বামপাশের সাইডবারে আপনার ElevenLabs API Key দিন!")
        elif not voice_name or not uploaded_files:
            st.error("ভয়েসের নাম এবং অন্তত একটি অডিও ফাইল প্রয়োজন!")
        else:
            with st.spinner("আপনার ভয়েস ক্লোন করা হচ্ছে... একটু অপেক্ষা করুন..."):
                url = "https://api.elevenlabs.io/v1/voices/add"
                headers = {"xi-api-key": api_key}
                data = {"name": voice_name, "description": voice_desc}
                files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
                
                try:
                    response = requests.post(url, headers=headers, data=data, files=files)
                    if response.status_code == 200:
                        st.success(f"🎉 অভিনন্দন! '{voice_name}' সফলভাবে ক্লোন হয়েছে। এবার 'টেক্সট থেকে অডিও' ট্যাবে গিয়ে এটি ব্যবহার করুন।")
                    else:
                        st.error(f"❌ কোনো সমস্যা হয়েছে: {response.text}")
                except Exception as e:
                    st.error(f"❌ এরর: {e}")

# ----------------- Tab 2: টেক্সট থেকে অডিও (TTS) -----------------
with tab2:
    st.header("টেক্সট থেকে অডিও তৈরি করুন")
    st.write("আপনার ক্লোন করা ভয়েস বা ডিফল্ট ভয়েস বেছে নিয়ে বাংলা বা ইংরেজিতে অডিও তৈরি করুন।")
    
    if not api_key:
        st.warning("ভয়েস লিস্ট দেখতে বামপাশের সাইডবারে API Key দিন।")
    else:
        # ElevenLabs থেকে সব ভয়েস লোড করা
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": api_key}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                voices = response.json().get("voices", [])
                voice_dict = {v["name"]: v["voice_id"] for v in voices}
                
                if voice_dict:
                    selected_voice_name = st.selectbox("তালিকা থেকে একটি ভয়েস বেছে নিন:", list(voice_dict.keys()))
                    selected_voice_id = voice_dict[selected_voice_name]
                    
                    text_input = st.text_area("এখানে আপনার টেক্সট লিখুন (বাংলা, হিন্দি বা ইংরেজি):", height=150, placeholder="আমি বাংলায় কথা বলতে পারি...")
                    
                    if st.button("🎵 অডিও জেনারেট করুন"):
                        if text_input:
                            with st.spinner("অডিও তৈরি হচ্ছে..."):
                                tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}"
                                tts_data = {
                                    "text": text_input,
                                    "model_id": "eleven_multilingual_v2", # বাংলা সাপোর্টের জন্য multilingual মডেল
                                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
                                }
                                tts_response = requests.post(tts_url, json=tts_data, headers=headers)
                                
                                if tts_response.status_code == 200:
                                    st.audio(tts_response.content, format="audio/mp3")
                                    st.success("✅ আপনার অডিও তৈরি হয়ে গেছে! উপরের প্লেয়ার থেকে শুনুন বা থ্রি-ডটে ক্লিক করে ডাউনলোড করুন।")
                                else:
                                    st.error(f"❌ অডিও তৈরিতে সমস্যা হয়েছে: {tts_response.text}")
                        else:
                            st.warning("অনুগ্রহ করে কিছু টেক্সট লিখুন!")
                else:
                    st.info("কোনো ভয়েস পাওয়া যায়নি।")
            else:
                st.error("ভয়েস লিস্ট লোড করতে সমস্যা হচ্ছে। API Key সঠিক আছে কিনা চেক করুন।")
        except Exception as e:
            st.error(f"❌ এরর: {e}")
                  
