import openai
import asyncio
import websockets
import os
import wave
import pyaudio
from dotenv import load_dotenv

# 📥 Load environment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🎙️ Audio recording settings
CHUNK = 1024
RATE = 44100
RECORD_SECONDS = 7
DEVICE_INDEX = int(os.getenv("DEVICE_INDEX", 0))

def record_audio(filename="temp.wav"):
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

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return filename

def transcribe_via_openai(file_path):
    print("📤 Uploading to Whisper API...")
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript["text"]

def gpt_suggest(text):
    print(f"📤 Sending to GPT: {text}")
    messages = [
        {"role": "system", "content": "You are an AI assistant helping the user pass a job interview. Give a clear and short bullet-pointed answer suggestion. Отвечай только на русском языке"},
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
    try:
        while True:
            try:
                filename = record_audio()
                text = transcribe_via_openai(filename)

                if len(text.strip()) > 5:
                    print(f"⚠️ Text: {text}")
                    answer = gpt_suggest(text)
                    await send_to_overlay(answer)
                else:
                    print("⚠️ Too little input, skipping...")

            except Exception as e:
                print(f"⚠️ Error: {e}")

    except KeyboardInterrupt:
        print("👋 Stopped.")

if __name__ == "__main__":
    asyncio.run(main())
