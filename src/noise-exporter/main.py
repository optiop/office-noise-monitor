import sounddevice as sd
import numpy as np
import pyloudnorm as pyln
from collections import deque

RATE = 44100
BLOCK = 0.1  # klein für streaming

meter = pyln.Meter(RATE)

BUFFER_SECONDS = 3
buffer = deque(maxlen=int(RATE * BUFFER_SECONDS))

def compute_lufs(audio):
    try:
        return meter.integrated_loudness(audio)
    except:
        return -100.0

def callback(indata, frames, time, status):
    audio = indata[:, 0].astype(np.float64)

    buffer.extend(audio)

    # nur rechnen wenn genug Daten da sind
    if len(buffer) < RATE:
        print("LUFS: collecting...")
        return

    chunk = np.array(buffer)

    loudness = compute_lufs(chunk)

    print(f"LUFS: {loudness:.2f}")

with sd.InputStream(
    samplerate=RATE,
    channels=1,
    blocksize=int(RATE * BLOCK),
    callback=callback
):
    input("Streaming... Enter to stop\n")
    