def record_audio(filename="temp.wav"):
    audio = pyaudio.PyAudio()

    # 🔍 Получаем поддерживаемое количество каналов
    device_info = audio.get_device_info_by_index(DEVICE_INDEX)
    max_channels = int(device_info.get('maxInputChannels', 1))
    channels = 1 if max_channels >= 1 else 2  # fallback на 2, если вдруг не поддерживает 1

    print(f"🎛️ Recording with {channels} channel(s)...")

    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
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

    # 🔊 Сохраняем WAV
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    return filename
