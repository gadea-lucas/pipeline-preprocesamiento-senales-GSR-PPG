import numpy as np
from scipy.signal import find_peaks


def maki_quality(data, fs=64, MinPeakDistance=60/240, MinPeakHeight=0):
    """
    Compute the Q_PHV reliability metric described in the RemotePPG MATLAB
    implementation by Maki et al. (EMBC 2019).

    The signal is mean-centered, normalized by the mean detected peak height,
    and scored as the sample variance of the normalized peak heights.

    Parameters
    ----------
    data : array-like
        Input PPG/BVP signal.
    fs : float, optional
        Sampling frequency in Hz, by default 64.
    MinPeakDistance : float, optional
        Minimum peak distance in seconds, by default 60/240.
    MinPeakHeight : float, optional
        Minimum peak height, by default 0.

    Returns
    -------
    float
        Q_PHV score. Lower values indicate more stable peak amplitudes.
    """

    data = np.asarray(data, dtype=float)
    min_peak_distance_samples = max(1, int(round(MinPeakDistance * fs)))

    def normalize_mean_peak_height(data):
        data = data - np.mean(data)
        idx_pks, _ = find_peaks(data, height=MinPeakHeight,
                                distance=min_peak_distance_samples)
        pks = data[idx_pks]
        if pks.size == 0 or np.isclose(np.mean(pks), 0):
            raise ValueError("Unable to normalize signal: no valid peaks found.")
        dataout = data / np.mean(pks)
        return dataout

    signal = normalize_mean_peak_height(data)

    idx_pks, _ = find_peaks(signal, height=MinPeakHeight,
                            distance=min_peak_distance_samples)
    pks = signal[idx_pks]
    if pks.size <= 1:
        return 0.0

    # MATLAB `var` uses sample variance (N-1 normalization).
    Q_PHV = np.var(pks, ddof=1)

    return Q_PHV
