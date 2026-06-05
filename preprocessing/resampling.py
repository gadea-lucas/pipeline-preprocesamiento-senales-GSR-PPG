import pandas as pd
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline


def resample_with_spline(
    df,
    target_frequency,
    timestamp_col="Timestamp",
    signal_col="Signal",
    spline_order=3,
):
    """
    Resample a signal to a target frequency using spline interpolation.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing timestamps and the signal column.
    target_frequency : float
        Desired sampling frequency in Hz.
    timestamp_col : str, optional
        Timestamp column name, by default "Timestamp".
    signal_col : str, optional
        Signal column name, by default "Signal".
    spline_order : int, optional
        Spline interpolation order, by default 3.

    Returns
    -------
    pandas.DataFrame
        Resampled signal with the same column names.
    """
    if target_frequency <= 0:
        raise ValueError("target_frequency must be positive.")

    df_resample = (
        df[[timestamp_col, signal_col]]
        .dropna()
        .drop_duplicates(subset=[timestamp_col])
        .sort_values(timestamp_col)
        .reset_index(drop=True)
    )

    if len(df_resample) < spline_order + 1:
        raise ValueError(
            f"Not enough samples for spline interpolation in {signal_col}. "
            f"Need at least {spline_order + 1}, received {len(df_resample)}."
        )

    timestamps = df_resample[timestamp_col].to_numpy(dtype=float)
    signal = df_resample[signal_col].to_numpy(dtype=float)

    target_interval = 1.0 / float(target_frequency)
    new_timestamps = np.arange(
        timestamps.min(),
        timestamps.max(),
        target_interval,
        dtype=float,
    )

    if new_timestamps.size == 0:
        raise ValueError(
            f"Unable to generate a time grid for {signal_col} at "
            f"{target_frequency} Hz."
        )

    spline = InterpolatedUnivariateSpline(timestamps, signal, k=spline_order)
    new_signal = spline(new_timestamps)

    return pd.DataFrame(
        {
            timestamp_col: new_timestamps,
            signal_col: new_signal,
        }
    )
