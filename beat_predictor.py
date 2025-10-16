import random

# very rough bpm guesser based on clip length + rms amplitude
def guess_bpm(duration, rms):
    bpm = int((60 / (duration / 4)) + (rms * 0.05))
    bpm += random.randint(-3,3)
    return bpm

if __name__ == "__main__":
    dur = 2.8   # seconds
    rms = 12000 # signal intensity
    print("est bpm:", guess_bpm(dur, rms))