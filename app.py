from elevenlabs.client import ElevenLabs
from elevenlabs import save
from google.cloud import texttospeech
import os

# ================== কনফিগ ==================
ELEVENLABS_API_KEY = "YOUR_ELEVENLABS_API_KEY"
GOOGLE_CREDENTIALS = "path/to/your-service-account.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS
# ===========================================

def elevenlabs_tts(text, voice_id="JBFqnCBsd6RMkjVDRZzb", output="elevenlabs.mp3"):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    save(audio, output)
    print(f"ElevenLabs → {output}")

def google_tts(text, language_code="bn-IN", voice_name="bn-IN-Chirp3-HD-Achernar", output="google.mp3"):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(output, "wb") as out:
        out.write(response.audio_content)
    print(f"Google Cloud → {output}")

# ========== ব্যবহার ==========
text = """এখানে তোমার লম্বা স্ক্রিপ্ট দাও।"""

# যেটা চাও সেটা আনকমেন্ট করো
elevenlabs_tts(text)
# google_tts(text)nsafe_allow_html=True)
