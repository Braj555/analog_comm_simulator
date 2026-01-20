import numpy as np
from scipy.signal import hilbert

def modulate_fm(message, carrier_freq, kf, sampling_rate):
    """
    Perform frequency modulation on a message signal.

    Parameters:
        message (np.array): Message signal to modulate
        carrier_freq (float): Carrier frequency in Hz
        kf (float): Frequency sensitivity constant
        sampling_rate (int): Sampling frequency in Hz

    Returns:
        t (np.array): Time vector
        fm_signal (np.array): FM modulated signal
    """
    dt = 1 / sampling_rate
    t = np.linspace(0, len(message) / sampling_rate, len(message), endpoint=False)
    integral_of_m = np.cumsum(message) * dt
    fm_signal = np.cos(2 * np.pi * carrier_freq * t + 2 * np.pi * kf * integral_of_m)
    return t, fm_signal

def demodulate_fm(fm_signal, kf, sampling_rate):
    """
    Demodulate an FM signal using the Hilbert transform.

    Parameters:
        fm_signal (np.array): FM modulated signal
        kf (float): Frequency sensitivity constant
        sampling_rate (int): Sampling frequency in Hz

    Returns:
        t (np.array): Time vector (aligned with demodulated signal)
        demodulated (np.array): Recovered message signal
    """
    analytic_signal = hilbert(fm_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    demodulated = np.diff(instantaneous_phase) * sampling_rate / (2 * np.pi * kf)

    # Corrected time vector to match demodulated signal length
    t = np.linspace(0, (len(demodulated) - 1) / sampling_rate, len(demodulated), endpoint=False)
    return t, demodulated


