import numpy as np
import pandas as pd
import neurokit2 as nk

from preprocessing.filtering import DigitalFilter


def hr_emotibit(
    df,
    sampling_rate,
    timestamp_col="Timestamp",
    signal_col="Ppg",
    output_col="Hr",
    peak_method="elgendi",
):
    """
    Estimate beat-to-beat heart rate from a PPG signal using the EmotiBit logic.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing timestamps and the filtered PPG signal.
    sampling_rate : float
        Sampling frequency in Hz.
    timestamp_col : str, optional
        Timestamp column name, by default "Timestamp".
    signal_col : str, optional
        PPG column name, by default "Ppg".
    output_col : str, optional
        Output heart-rate column name, by default "Hr".
    peak_method : str, optional
        NeuroKit peak detector, by default "elgendi".

    Returns
    -------
    pandas.DataFrame
        Heart-rate time series with one value per detected beat.
    """
    if sampling_rate <= 0:
        raise ValueError("sampling_rate must be positive.")

    if df.empty:
        return pd.DataFrame(columns=[timestamp_col, output_col])

    timestamps = df[timestamp_col].to_numpy(dtype=float)
    signal = df[signal_col].to_numpy(dtype=float)

    peaks = nk.ppg.ppg_findpeaks(
        signal,
        sampling_rate=sampling_rate,
        method=peak_method,
    )["PPG_Peaks"]

    if len(peaks) == 0:
        return pd.DataFrame(columns=[timestamp_col, output_col])

    heart_rate_filter = DigitalFilter("IIR_LOWPASS", sampling_rate, 1)
    sample_period_ms = (1.0 / float(sampling_rate)) * 1000.0

    beats = np.zeros(len(signal), dtype=int)
    beats[peaks] = 1

    heart_rates = []
    beat_timestamps = []
    inter_beat_sample_count = 0

    for index, beat in enumerate(beats):
        inter_beat_sample_count += 1
        if beat:
            inter_beat_interval_ms = inter_beat_sample_count * sample_period_ms
            heart_rate = (60.0 / inter_beat_interval_ms) * 1000.0
            heart_rate = heart_rate_filter.filter(heart_rate)
            heart_rates.append(heart_rate)
            beat_timestamps.append(timestamps[index])
            inter_beat_sample_count = 0

    return pd.DataFrame(
        {
            timestamp_col: beat_timestamps,
            output_col: heart_rates,
        }
    )
