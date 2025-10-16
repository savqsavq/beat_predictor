import numpy as np, random

def window_bpm_estimates(duration, rms, n=6):
    base = int((60 / (duration / 4)) + (rms * 0.05))
    offsets = np.linspace(-4,4,n)
    noise = np.random.randint(-2,3,size=n)
    return np.clip(base + offsets + noise, 60, 190)

def swing_factor(bpm_series):
    # naive 'groove' variation calc
    diffs = np.diff(bpm_series)
    swing = np.mean(np.abs(diffs)) / np.mean(bpm_series)
    return swing