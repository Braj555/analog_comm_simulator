import numpy as np

def generate_message_signal(freq=5, duration=1, sampling_rate=1000):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    m = np.sin(2 * np.pi * freq * t)
    return t, m
