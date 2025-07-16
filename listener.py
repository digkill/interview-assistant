import openai
import ssl
import whisper
import asyncio
import websockets
import os
import wave
import pyaudio
from dotenv import load_dotenv

# 📥 Загрузка переменных
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🎙️ Аудио-настройки
CHUNK = 1024
RATE = 44100
RECORD_SECONDS = 7
DEVICE_INDEX = int(os.getenv("DEVICE_INDEX", 0))

# 🎧 Whisper модель
model = whisper.load_model("base")

def save_wav(audio_bytes, filename="temp.wav"):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(audio_bytes)

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=RATE,
                        input=True,
                        input_device_index=DEVICE_INDEX,
                        frames_per_buffer=CHUNK)
    print("🎙️ Recording...")
    frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS))]
    print("🛑 Done.")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return b''.join(frames)

def transcribe(audio_bytes):
    save_wav(audio_bytes, "temp.wav")
    result = model.transcribe("temp.wav")
    return result['text']

def gpt_suggest(text):
    print(f"📤 Sending to GPT: {text}")
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant helping the user pass a job interview. Give a clear and short bullet-pointed answer suggestion. Отвечай только на русском языке."
        },
        {
            "role": "user",
            "content": text
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=200
    )
    return response.choices[0].message.content.strip()

# 🔗 Подключение к WebSocket
async def send_to_overlay(text):
    uri = "ws://127.0.0.1:8765"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(text)
            print("✅ Sent to overlay:", text)
    except Exception as e:
        print(f"❌ WebSocket send error: {e}")

# 🔁 Основной цикл
async def main():
    try:
        while True:
            try:
                audio = record_audio()
                text = transcribe(audio)

                if len(text.strip()) > 5:
                    print(f"⚠️ Input: {text}")
                    answer = gpt_suggest(text)
                    await send_to_overlay(answer)
                else:
                    print("⚠️ Too short, skipping...")

            except Exception as e:
                print(f"⚠️ Inner error: {e}")
    except KeyboardInterrupt:
        print("👋 Stopped by user")

if __name__ == "__main__":
    asyncio.run(main())
