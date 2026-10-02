import streamlit as st
import requests

# Page Setup
st.set_page_config(page_title="Awaz Do - AI Voice Cloning", page_icon="🎙️", layout="centered")

# Main Title and Subtitles in 3 Languages
st.title("🎙️ Awaz Do - The Local AI Tool")
st.markdown("**Clone your voice and generate audio from text in seconds!**")
st.markdown("*(মাত্র কয়েক সেকেন্ডে আপনার নিজের ভয়েস ক্লোন করুন এবং টেক্সট থেকে অডিও তৈরি করুন!)*")
st.markdown("*(कुछ ही सेकंड में अपनी आवाज़ क्लोन करें और टेक्स्ट से ऑडियो बनाएं!)*")
st.markdown("---")

# Sidebar for API Key
st.sidebar.header("🔑 API Setup (সেটআপ / सेटअप)")
api_key = st.sidebar.text_input("Enter ElevenLabs API Key \n(এখানে API Key দিন / यहाँ API Key दर्ज करें):", type="password")
st.sidebar.markdown("*[Get free API Key from ElevenLabs.io]*")
st.sidebar.info("API Key is required to use this tool. \n(এই টুলটি ব্যবহার করতে API Key প্রয়োজন। / इस टूल के उपयोग के लिए API Key आवश्यक है।)")

# Tabs for features
tab1, tab2 = st.tabs(["🗣️ Clone Voice (ভয়েস ক্লোন / वॉयस क्लोन)", "🔊 Text to Audio (অডিও তৈরি / ऑडियो बनाएं)"])

# ----------------- Tab 1: Voice Cloning -----------------
with tab1:
    st.header("Upload Your Voice (আপনার ভয়েস আপলোড করুন / अपनी आवाज़ अपलोड करें)")
    st.write("Upload a 1-5 minute clear audio clip. (১-৫ মিনিটের পরিষ্কার অডিও আপলোড করুন। / 1-5 मिनट का स्पष्ट ऑडियो अपलोड करें।)")
    
    voice_name = st.text_input("Voice Name (ভয়েসের নাম দিন / आवाज़ का नाम दें):", placeholder="e.g., My AI Voice")
    voice_desc = st.text_input("Description (বিবরণ / विवरण - Optional):")
    uploaded_files = st.file_uploader("Upload Audio (অডিও আপলোড / ऑडियो अपलोड - mp3/wav/m4a):", type=['mp3', 'wav', 'm4a'], accept_multiple_files=True)
    
    if st.button("🚀 Create Voice Clone (ক্লোন তৈরি করুন / क्लोन बनाएं)"):
        if not api_key:
            st.error("Please enter your API Key in the sidebar! (সাইডবারে API Key দিন! / कृपया साइडबार में API Key दर्ज करें!)")
        elif not voice_name or not uploaded_files:
            st.error("Name and audio file are required! (নাম এবং অডিও ফাইল প্রয়োজন! / नाम और ऑडियो फ़ाइल आवश्यक है!)")
        else:
            with st.spinner("Cloning voice... Please wait... (ভয়েস ক্লোন করা হচ্ছে... / आवाज़ क्लोन हो रही है...)"):
                url = "https://api.elevenlabs.io/v1/voices/add"
                headers = {"xi-api-key": api_key}
                data = {"name": voice_name, "description": voice_desc}
                files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
                
                try:
                    response = requests.post(url, headers=headers, data=data, files=files)
                    if response.status_code == 200:
                        st.success(f"🎉 Success! '{voice_name}' is ready. (সফলভাবে তৈরি হয়েছে! / सफलतापूर्वक तैयार है!)")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ----------------- Tab 2: Text to Speech (TTS) -----------------
with tab2:
    st.header("Generate Audio (অডিও তৈরি করুন / ऑडियो उत्पन्न करें)")
    st.write("Type in English, Bengali, or Hindi. (ইংরেজি, বাংলা বা হিন্দিতে টেক্সট লিখুন। / अंग्रेजी, बंगाली या हिंदी में टाइप करें।)")
    
    if not api_key:
        st.warning("Enter API Key to load voices. (ভয়েস দেখতে API Key দিন। / आवाज़ें देखने के लिए API Key दर्ज करें।)")
    else:
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": api_key}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                voices = response.json().get("voices", [])
                voice_dict = {v["name"]: v["voice_id"] for v in voices}
                
                if voice_dict:
                    selected_voice_name = st.selectbox("Select a Voice (ভয়েস বেছে নিন / आवाज़ चुनें):", list(voice_dict.keys()))
                    selected_voice_id = voice_dict[selected_voice_name]
                    
                    text_input = st.text_area("Enter Text (আপনার টেক্সট লিখুন / अपना टेक्स्ट यहाँ लिखें):", height=150, placeholder="Type your text here...")
                    
                    if st.button("🎵 Generate Audio (অডিও জেনারেট করুন / ऑडियो बनाएं)"):
                        if text_input:
                            with st.spinner("Generating... (তৈরি হচ্ছে... / उत्पन्न हो रहा है...)"):
                                tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}"
                                tts_data = {
                                    "text": text_input,
                                    "model_id": "eleven_multilingual_v2",
                                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
                                }
                                tts_response = requests.post(tts_url, json=tts_data, headers=headers)
                                
                                if tts_response.status_code == 200:
                                    st.audio(tts_response.content, format="audio/mp3")
                                    st.success("✅ Ready! Play or download. (তৈরি! প্লে বা ডাউনলোড করুন। / तैयार है! प्ले या डाउनलोड करें।)")
                                else:
                                    st.error(f"❌ Error: {tts_response.text}")
                        else:
                            st.warning("Please enter some text! (কিছু টেক্সট লিখুন! / कृपया कुछ टेक्स्ट लिखें!)")
                else:
                    st.info("No voices found.")
            else:
                st.error("Error loading voices. Check your API Key.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            
