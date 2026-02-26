import numpy as np
from scipy.signal import butter, filtfilt
from statsmodels.tsa.arima.model import ARIMA


def butterworth_filter(series, cutoff_minutes=240, order=4):
    """
    Apply a Butterworth low-pass filter to smooth noisy price data.

    Parameters:
        series (pd.Series): Price series (e.g., df['close'])
        cutoff_minutes (int): Period defining cutoff frequency (default 4 hours)
        order (int): Filter order

    Returns:
        np.ndarray: Filtered signal
    """

    # Sampling frequency: 1 sample every 15 minutes → fs = 1/15 samples per minute
    fs = 1 / 15.0

    # Convert cutoff period to frequency (cycles per minute)
    fc = 1 / cutoff_minutes

    # Normalize by Nyquist frequency
    nyq = 0.5 * fs
    wn = fc / nyq

    # Design Butterworth filter
    b, a = butter(order, wn, btype='low', analog=False)

    # Zero-phase filtering to avoid phase shift
    filtered = filtfilt(b, a, series)

    return filtered


def compute_fft(series):
    """
    Compute FFT magnitude spectrum for frequency-domain analysis.

    Parameters:
        series (pd.Series): Price series

    Returns:
        freqs (np.ndarray): Frequency bins
        magnitude (np.ndarray): Magnitude of FFT
    """

    N = len(series)

    # Remove mean to avoid DC spike dominating spectrum
    centered = series - np.mean(series)

    # FFT (real-valued)
    fft_vals = np.fft.rfft(centered)

    # Frequency bins (15 minutes = 900 seconds)
    freqs = np.fft.rfftfreq(N, d=15 * 60)

    magnitude = np.abs(fft_vals)

    return freqs, magnitude


def dsp_forecast(filtered_series, steps=4):
    """
    Forecast future values using ARIMA on the filtered signal.

    Parameters:
        filtered_series (array-like): Output of Butterworth filter
        steps (int): Number of future points to forecast (4 = next hour)

    Returns:
        np.ndarray: Forecasted values
    """

    model = ARIMA(filtered_series, order=(2, 1, 2))
    res = model.fit()

    return res.forecast(steps=steps)
