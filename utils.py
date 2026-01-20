import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def save_plots_to_pdf(figures, filename="all_plots.pdf"):
    """
    Save a list of matplotlib figures to a single PDF file.

    Parameters:
        figures (list): List of matplotlib figures
        filename (str): PDF filename
    Returns:
        BytesIO: The in-memory PDF file buffer
    """
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    for fig in figures:
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        image = ImageReader(buf)
        c.drawImage(image, 40, 300, width=500, height=400)  # adjust placement if needed
        c.showPage()

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

def plot_signal(t, s, title="Signal", xlabel="Time", ylabel="Amplitude"):
    """
    Plot a time-domain signal using matplotlib and display in Streamlit.

    Returns:
        matplotlib.figure.Figure: The figure object
    """
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(t, s)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    st.pyplot(fig)
    return fig

def plot_spectrum(signal, sampling_rate, title="Spectrum"):
    """
    Plot frequency-domain spectrum of a signal.

    Returns:
        matplotlib.figure.Figure: The figure object
    """
    n = len(signal)
    freq = np.fft.fftfreq(n, d=1 / sampling_rate)
    spectrum = np.fft.fft(signal)
    magnitude = np.abs(spectrum) / n

    mask = freq >= 0
    freq = freq[mask]
    magnitude = magnitude[mask]

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(freq, magnitude)
    ax.set_title(title)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.grid(True)
    st.pyplot(fig)
    return fig




