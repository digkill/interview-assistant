import openai
import asyncio
import websockets
import os
import wave
import pyaudio
import keyboard
from dotenv import load_dotenv
import time

# 📥 Load .env variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DEVICE_INDEX = int(os.getenv("DEVICE_INDEX", 0))

# 🎙️ Audio settings
CHUNK = 1024
RATE = 44100
CHANNELS = 1
FORMAT = pyaudio.paInt16

def record_until_space(filename="temp.wav"):
    print("🎤 Press [Space] to start recording, [Space] again to stop, [X] to exit.")
    while not keyboard.is_pressed("space"):
        if keyboard.is_pressed("x"):
            raise KeyboardInterrupt
        time.sleep(0.05)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        input_device_index=DEVICE_INDEX,
                        frames_per_buffer=CHUNK)
    print("⏺️ Recording... Press [Space] to stop.")

    frames = []
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed("space"):
            print("🛑 Stopped recording.")
            break
        if keyboard.is_pressed("x"):
            raise KeyboardInterrupt

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return filename

def transcribe_via_openai(file_path):
    print("🧠 Transcribing via Whisper...")
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="ru")
        return transcript["text"]

def gpt_suggest(text):
    print(f"🧠 GPT анализ: {text}")
    messages = [
        {"role": "system", "content": "Ты ИИ-помощник, помогаешь пройти собеседование. Отвечай кратко, чётко, по делу. Только на русском языке, в виде пунктов."},
        {"role": "user", "content": text}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

async def send_to_overlay(text):
    uri = "ws://127.0.0.1:8765"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(text)
            print("✅ Sent to overlay")
    except Exception as e:
        print(f"❌ Overlay send error: {e}")

async def main():
    print("🎧 Готово. Жду нажатия клавиш...")
    try:
        while True:
            filename = record_until_space()
            text = transcribe_via_openai(filename)

            if len(text.strip()) > 5:
                print(f"📄 Распознанный текст: {text}")
                answer = gpt_suggest(text)
                await send_to_overlay(answer)
            else:
                print("⚠️ Слишком мало текста, пропуск...")

    except KeyboardInterrupt:
        print("👋 Выход.")

if __name__ == "__main__":
    asyncio.run(main())
