import pandas as pd
import numpy as np

def IQR(df, column):
    """
    Detects and removes outliers from a column using the Interquartile Range (IQR)
    method.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data.
    column : str
        Column to process.

    Returns
    -------
    df_clean : pandas.DataFrame
        A cleaned copy of the DataFrame.
    """

    # Compute IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds for outlier detection
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)

    # Create a clean copy and remove outliers by setting them to NaN
    df_clean = df.copy()
    df_clean.loc[outliers, column] = np.nan

    # Interpolate missing values linearly
    df_clean[column] = pd.Series(df_clean[column]).interpolate(method="linear")

    # Fill any remaining NaNs with the column mean
    df_clean[column] = df_clean[column].fillna(df_clean[column].mean())

    return df_clean
