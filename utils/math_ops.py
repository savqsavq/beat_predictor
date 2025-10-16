import numpy as np

def normalize(arr):
    arr = np.array(arr, dtype=float)
    if np.max(arr) == 0:
        return arr
    return arr / np.max(arr)

def moving_std(arr, n=5):
    if len(arr) < n:
        return np.zeros_like(arr)
    stds = []
    for i in range(len(arr)-n):
        stds.append(np.std(arr[i:i+n]))
    return np.array(stds)

def weighted_mean(arr, weights=None):
    if weights is None:
        weights = np.ones_like(arr)
    return np.sum(arr * weights) / np.sum(weights)