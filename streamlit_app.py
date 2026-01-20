import streamlit as st
import numpy as np
from signal_generator import generate_message_signal
from am_modulation import modulate_am_dsb_sc, demodulate_am_dsb_sc
from fm_modulation import modulate_fm, demodulate_fm
from noise_analysis import add_awgn_noise
from utils import plot_signal, plot_spectrum

# --- Streamlit UI ---
st.title("🎛️ AM & FM Signal Transmission Simulator")

# --- User Controls ---
mod_type = st.selectbox("Select Modulation Type", ["AM - DSB-SC", "FM"])
msg_freq = st.slider("Message Frequency (Hz)", 10, 1000, 50)
carrier_freq = st.slider("Carrier Frequency (Hz)", 500, 5000, 1000)
snr_db = st.slider("SNR (dB)", 0, 40, 20)
duration = st.slider("Signal Duration (seconds)", 0.01, 0.1, 0.05)
sampling_rate = 10000
kf = st.slider("FM Sensitivity (kf)", 50, 500, 100)

# --- Generate Message Signal ---
t, message = generate_message_signal(freq=msg_freq, duration=duration, sampling_rate=sampling_rate)
st.subheader("📉 Message Signal")
plot_signal(t, message, title="Message Signal")
plot_spectrum(message, sampling_rate, title="Spectrum of Message Signal")

# --- Modulation Section ---
if mod_type == "AM - DSB-SC":
    t, modulated = modulate_am_dsb_sc(message, carrier_freq, sampling_rate)
    st.subheader("📡 AM Modulated Signal")
    plot_signal(t, modulated, title="AM DSB-SC Signal")
    plot_spectrum(modulated, sampling_rate, title="Spectrum of AM Signal")

    # Add Noise
    noisy = add_awgn_noise(modulated, snr_db)
    st.subheader("🔊 Noisy AM Signal")
    plot_signal(t, noisy, title=f"Noisy AM Signal (SNR = {snr_db} dB)")
    plot_spectrum(noisy, sampling_rate, title="Spectrum of Noisy AM Signal")

    # Demodulate
    _, recovered = demodulate_am_dsb_sc(noisy, carrier_freq, sampling_rate)
    st.subheader("🔁 Recovered AM Signal")
    plot_signal(t, recovered, title="Recovered AM Signal")
    plot_spectrum(recovered, sampling_rate, title="Spectrum of Recovered AM")

elif mod_type == "FM":
    t, modulated = modulate_fm(message, carrier_freq, kf, sampling_rate)
    st.subheader("📡 FM Modulated Signal")
    plot_signal(t, modulated, title="FM Signal")
    plot_spectrum(modulated, sampling_rate, title="Spectrum of FM Signal")

    # Add Noise
    noisy = add_awgn_noise(modulated, snr_db)
    st.subheader("🔊 Noisy FM Signal")
    plot_signal(t, noisy, title=f"Noisy FM Signal (SNR = {snr_db} dB)")
    plot_spectrum(noisy, sampling_rate, title="Spectrum of Noisy FM Signal")

    # Demodulate
    t_recovered, recovered = demodulate_fm(noisy, kf, sampling_rate)
    st.subheader("🔁 Recovered FM Signal")
    plot_signal(t_recovered, recovered, title="Recovered FM Signal")
    plot_spectrum(recovered, sampling_rate, title="Spectrum of Recovered FM")



