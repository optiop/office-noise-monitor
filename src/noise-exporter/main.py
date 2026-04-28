import sounddevice as sd
import numpy as np
import pyloudnorm as pyln
from collections import deque
from prometheus_client import start_http_server, Gauge

RATE = 44100
BLOCK = 0.1

meter = pyln.Meter(RATE)

BUFFER_SECONDS = 3
buffer = deque(maxlen=int(RATE * BUFFER_SECONDS))

# Prometheus Metric
loudness_gauge = Gauge("room_loudness_lufs", "Room loudness in LUFS")

def compute_lufs(audio):
    try:
        return meter.integrated_loudness(audio)
    except:
        return -100.0

def callback(indata, frames, time, status):
    audio = indata[:, 0].astype(np.float64)
    buffer.extend(audio)

    if len(buffer) < RATE:
        print("LUFS: collecting...")
        return

    chunk = np.array(buffer)
    loudness = compute_lufs(chunk)

    # Prometheus Metric setzen
    loudness_gauge.set(loudness)

    print(f"LUFS: {loudness:.2f}")

def main():
    # Prometheus endpoint starten
    start_http_server(8000)
    print("Metrics running on http://localhost:8000/metrics")

    with sd.InputStream(
        samplerate=RATE,
        channels=1,
        blocksize=int(RATE * BLOCK),
        callback=callback
    ):
        input("Streaming... Enter to stop\n")

if __name__ == "__main__":
    main()
    