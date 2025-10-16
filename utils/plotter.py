import matplotlib.pyplot as plt, numpy as np

def plot_tempo_map(bpm_series):
    x = np.arange(len(bpm_series))
    plt.plot(x, bpm_series, color="#cc8855", lw=2)
    plt.title("tempo map (est bpm over time)")
    plt.xlabel("segment")
    plt.ylabel("bpm")
    plt.savefig("bpm_map.png", dpi=120)
    plt.close()