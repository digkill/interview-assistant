import pyaudio

pa = pyaudio.PyAudio()
DEVICE_INDEX = 2  # замени на свой
for rate in [8000, 16000, 22050, 32000, 44100, 48000]:
    try:
        if pa.is_format_supported(rate,
                                  input_device=DEVICE_INDEX,
                                  input_channels=1,
                                  input_format=pyaudio.paInt16):
            print(f"✅ Supported sample rate: {rate}")
    except Exception:
        print(f"❌ Not supported: {rate}")
