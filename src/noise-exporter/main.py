import sounddevice as sd
import numpy as np
import pyloudnorm as pyln

samplerate = 48000
block_size = 1024

meter = pyln.Meter(samplerate)

def callback(indata, frames, time, status):
    if status:
        print(status)
    # mono or stereo
    audio = indata.copy()
    loudness = meter.integrated_loudness(audio)
    print(f"Loudness: {loudness:.2f} LUFS")

with sd.InputStream(channels=1, samplerate=samplerate,
                    blocksize=block_size, callback=callback):
    input("Streaming... press Enter to stop\n")
