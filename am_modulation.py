import numpy as np
from signal_generator import generate_message_signal
from utils import plot_signal
from noise_analysis import add_awgn_noise

def modulate_am_dsb_sc(message, carrier_freq, sampling_rate):
    t = np.linspace(0, len(message)/sampling_rate, len(message), endpoint=False)
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    modulated = message * carrier
    return t, modulated

def demodulate_am_dsb_sc(modulated, carrier_freq, sampling_rate):
    t = np.linspace(0, len(modulated)/sampling_rate, len(modulated), endpoint=False)
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    product = modulated * carrier

    # Low-pass filter using FFT
    fft = np.fft.fft(product)
    freqs = np.fft.fftfreq(len(fft), 1/sampling_rate)
    fft[np.abs(freqs) > 1000] = 0  # LPF at 1 kHz
    recovered = np.fft.ifft(fft).real
    return t, recovered

# New function to handle all AM steps together
def process_am_modulation(msg_freq, carrier_freq, sampling_rate, snr_db, duration=0.05):
    # Generate message
    t, message = generate_message_signal(freq=msg_freq, duration=duration, sampling_rate=sampling_rate)

    # Modulate
    t, am_signal = modulate_am_dsb_sc(message, carrier_freq, sampling_rate)

    # Add noise
    noisy_am = add_awgn_noise(am_signal, snr_db)

    # Demodulate noisy signal
    _, recovered = demodulate_am_dsb_sc(noisy_am, carrier_freq, sampling_rate)

    return t, message, am_signal, noisy_am, recovered

# --- For testing only ---
if __name__ == "__main__":
    sampling_rate = 10000
    msg_freq = 50
    carrier_freq = 1000
    snr_db = 10

    t, message, am_signal, noisy_am, recovered_noisy_am = process_am_modulation(
        msg_freq, carrier_freq, sampling_rate, snr_db
    )

    plot_signal(t, message, "Message Signal (50 Hz)")
    plot_signal(t, am_signal, "AM DSB-SC Modulated Signal")
    plot_signal(t, noisy_am, f"AM Signal with Noise (SNR={snr_db} dB)")
    plot_signal(t, recovered_noisy_am, "Recovered Signal from Noisy AM")

