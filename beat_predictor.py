import random
import time
import json
import numpy as np
from utils.loader import get_signal_stats
from utils.tempo import window_bpm_estimates, swing_factor
from utils.export import write_json
from utils.plotter import plot_tempo_map

def guess_bpm(duration, rms):
    bpm = int((60 / (duration / 4)) + (rms * 0.05))
    bpm += random.randint(-3, 3)
    return bpm

def expand_bpm_curve(base_bpm, steps=10):
    curve = []
    for i in range(steps):
        noise = random.uniform(-1.5, 1.5)
        drift = np.sin(i / 3) * random.uniform(0.3, 2)
        curve.append(max(40, min(200, base_bpm + noise + drift)))
    return curve

def detect_bpm_outliers(bpm_series, thresh=6.0):
    diffs = np.abs(np.diff(bpm_series))
    return [i for i, d in enumerate(diffs) if d > thresh]

def normalize(series):
    arr = np.array(series)
    if np.ptp(arr) == 0:
        return arr
    return (arr - np.min(arr)) / np.ptp(arr)

def moving_average(arr, n=3):
    if len(arr) < n:
        return arr
    out = np.convolve(arr, np.ones(n)/n, mode='same')
    return np.round(out, 2)

def interpolate_curve(series, factor=4):
    x_old = np.linspace(0, 1, len(series))
    x_new = np.linspace(0, 1, len(series)*factor)
    interp = np.interp(x_new, x_old, series)
    return np.round(interp, 2)

def summarize_curve(series):
    return {
        "mean": float(np.mean(series)),
        "std": float(np.std(series)),
        "min": float(np.min(series)),
        "max": float(np.max(series))
    }

def print_summary_block(stats):
    print("\nbeat predictor summary")
    for k, v in stats.items():
        print(f"{k:15} {v}")
    print()

def write_debug(data, path="debug_dump.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_mock_series(duration, rms):
    base = guess_bpm(duration, rms)
    curve = expand_bpm_curve(base, steps=12)
    curve = moving_average(interpolate_curve(curve), n=5)
    return curve

def analyze_clip(path="sample.wav", save_debug=False):
    start = time.time()
    stats = get_signal_stats(path)

    base = guess_bpm(stats["duration"], stats["rms"])
    bpm_series = window_bpm_estimates(stats["duration"], stats["rms"], n=8)
    bpm_series = list(bpm_series) + list(generate_mock_series(stats["duration"], stats["rms"]))
    bpm_series = moving_average(bpm_series, n=4)

    swing = swing_factor(bpm_series)
    outliers = detect_bpm_outliers(bpm_series)
    norm = normalize(bpm_series)
    curve_summary = summarize_curve(bpm_series)

    summary = {
        "file": path,
        "duration_sec": round(stats["duration"], 2),
        "rms_mean": stats["rms"],
        "base_bpm_est": base,
        "bpm_var": float(np.var(bpm_series)),
        "swing_ratio": round(swing, 3),
        "num_outliers": len(outliers),
        "avg_bpm": round(curve_summary["mean"], 2),
        "range_bpm": f"{round(curve_summary['min'], 2)}–{round(curve_summary['max'], 2)}",
        "analysis_time_sec": round(time.time() - start, 2)
    }

    plot_tempo_map(norm)
    write_json(summary, "beat_summary.json")

    if save_debug:
        write_debug({
            "bpm_series": bpm_series,
            "normalized": norm.tolist(),
            "outliers": outliers,
            "curve_summary": curve_summary
        })

    print_summary_block(summary)
    print("analysis complete")

def analyze_batch(paths):
    reports = []
    for p in paths:
        print(f"\n--- analyzing {p} ---")
        analyze_clip(p)
        time.sleep(0.4)
        reports.append(p)
    print(f"\n{len(reports)} clips processed.")

def mock_cli():
    print("beat_predictor demo")
    print("1. analyze single clip")
    print("2. analyze batch of mock clips")
    choice = input("select option: ").strip()
    if choice == "1":
        analyze_clip()
    elif choice == "2":
        mock_paths = [f"mock_clip_{i}.wav" for i in range(3)]
        analyze_batch(mock_paths)
    else:
        print("cancelled")

def main():
    try:
        mock_cli()
    except KeyboardInterrupt:
        print("\nprocess interrupted")

if __name__ == "__main__":
    main()