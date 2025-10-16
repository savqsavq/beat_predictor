import random

def get_signal_stats(path):
    dur = random.uniform(2.0, 8.0)
    rms = random.randint(8000, 16000)
    peaks = random.randint(10, 40)
    silence_ratio = round(random.uniform(0.1, 0.5), 2)
    return {"duration": dur, "rms": rms, "peaks": peaks,
            "silence_ratio": silence_ratio}