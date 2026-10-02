import asyncio
import edge_tts
import os

# ====================== ভয়েস লিস্ট ======================
VOICES = {
    "1": {"name": "বাংলা - সাদিয়া (মহিলা)", "id": "bn-BD-NabanitaNeural"},
    "2": {"name": "বাংলা - প্রদীপ (পুরুষ)", "id": "bn-BD-PradeepNeural"},
    "3": {"name": "বাংলা - তানিশা (মহিলা - ভারত)", "id": "bn-IN-TanishaaNeural"},
    "4": {"name": "বাংলা - ভাস্কর (পুরুষ - ভারত)", "id": "bn-IN-BashkarNeural"},
    "5": {"name": "হিন্দি - স্বরা (মহিলা)", "id": "hi-IN-SwaraNeural"},
    "6": {"name": "হিন্দি - মধুর (পুরুষ)", "id": "hi-IN-MadhurNeural"},
    "7": {"name": "ইংরেজি - জেনি (মহিলা)", "id": "en-US-JennyNeural"},
    "8": {"name": "ইংরেজি - গাই (পুরুষ)", "id": "en-US-GuyNeural"},
    "9": {"name": "ইংরেজি - আরিয়া (মহিলা)", "id": "en-US-AriaNeural"},
    "10": {"name": "ইংরেজি - নীর্জা (মহিলা - ভারত)", "id": "en-IN-NeerjaNeural"},
    "11": {"name": "ইংরেজি - প্রভাত (পুরুষ - ভারত)", "id": "en-IN-PrabhatNeural"},
}

async def generate_voice():
    print("\n" + "="*50)
    print("       Best Free Natural TTS (No API Key)")
    print("="*50)

    # টেক্সট ইনপুট
    print("\nতোমার টেক্সট লিখো (শেষ করতে এন্টার দুইবার চাপো):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    text = "\n".join(lines)

    if not text.strip():
        print("কোনো টেক্সট দেওয়া হয়নি!")
        return

    # ভয়েস সিলেক্ট
    print("\nউপলব্ধ ভয়েসসমূহ:")
    for key, voice in VOICES.items():
        print(f"{key}. {voice['name']}")

    choice = input("\nকোন ভয়েস চাও? (1-11): ").strip()
    if choice not in VOICES:
        print("ভুল সিলেকশন! ডিফল্ট ভয়েস ব্যবহার করা হচ্ছে...")
        choice = "1"

    selected_voice = VOICES[choice]["id"]
    print(f"\nসিলেক্টেড ভয়েস: {VOICES[choice]['name']}")

    # স্পিড
    speed = input("স্পিড দাও (0.7 থেকে 1.3, ডিফল্ট 1.0): ").strip()
    try:
        speed = float(speed)
        rate = f"{int((speed - 1) * 100):+d}%"
    except:
        rate = "+0%"

    # আউটপুট ফাইল
    output_file = input("ফাইলের নাম দাও (ডিফল্ট: output.mp3): ").strip()
    if not output_file:
        output_file = "output.mp3"
    if not output_file.endswith(".mp3"):
        output_file += ".mp3"

    print("\nভয়েস তৈরি হচ্ছে... অপেক্ষা করো...")

    communicate = edge_tts.Communicate(text, selected_voice, rate=rate)
    await communicate.save(output_file)

    print(f"\nসফল হয়েছে!")
    print(f"ফাইল সেভ হয়েছে: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    asyncio.run(generate_voice())
