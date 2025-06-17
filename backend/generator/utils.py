import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch
import neurokit2 as nk

def create_output_directories():
    """Create necessary output directories"""
    directories = [
        "static/plots",
        "static/csv",
        "data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def band_limited_noise(low, high, samples, sr):
    """Generate band-limited noise"""
    nyq = sr / 2
    b, a = butter(4, [low / nyq, high / nyq], btype='band')
    white = np.random.randn(samples)
    return filtfilt(b, a, white)

def extract_band_power(eeg_data, sampling_rate=256):
    """Extract band power features from EEG data"""
    bands = {
        "delta": (1, 4), 
        "theta": (4, 8), 
        "alpha": (8, 12),
        "beta": (13, 30), 
        "gamma": (30, 45)
    }
    
    power = {k: [] for k in bands}
    
    for ch in eeg_data:
        f, Pxx = welch(ch, fs=sampling_rate)
        for band, (low, high) in bands.items():
            idx = np.logical_and(f >= low, f <= high)
            power[band].append(np.trapz(Pxx[idx], f[idx]))
    
    return pd.DataFrame(power)

def extract_hrv_features(ecg_data, sampling_rate=256):
    """Extract HRV features from ECG data"""
    try:
        _, info = nk.ecg_process(ecg_data, sampling_rate=sampling_rate)
        hrv = nk.hrv(info, sampling_rate=sampling_rate, features=['time', 'frequency'], show=False)
        return hrv
    except Exception as e:
        print(f"HRV extraction failed: {e}")
        return pd.DataFrame()

def create_eeg_plot(eeg_data, channels, title, session_id, sampling_rate=256):
    """Create clinical-style EEG plot"""
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # Use first 10 channels for visualization
    shown_channels = channels[:10]
    spacing = 200
    colors = plt.cm.tab10(np.linspace(0, 1, len(shown_channels)))
    
    for i, ch in enumerate(shown_channels):
        if ch in eeg_data.columns:
            y = eeg_data[ch].values + i * spacing
            ax.plot(eeg_data.index / sampling_rate, y, color=colors[i], linewidth=0.8)
            ax.text(-1, i * spacing, ch, fontsize=10, va='center', fontweight='bold')
    
    ax.set_xlim(0, 10)
    ax.set_ylim(-spacing, (len(shown_channels) + 0.5) * spacing)
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("Amplitude (μV)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_yticks([])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = f"static/plots/{session_id}_plot.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return plot_path

def create_ecg_plot(ecg_data, title, session_id, sampling_rate=256):
    """Create clinical-style ECG plot with red grid"""
    fig, ax = plt.subplots(figsize=(15, 4))
    
    # Plot ECG signal
    ax.plot(ecg_data.index / sampling_rate, ecg_data.values, color='black', linewidth=1.2)
    
    # Red grid like ECG paper
    ax.set_facecolor('#fffafa')
    for y in np.arange(-2, 2.5, 0.5):
        ax.axhline(y, color='red', linewidth=0.3, alpha=0.4)
    for x in np.arange(0, len(ecg_data) / sampling_rate + 1, 0.2):
        ax.axvline(x, color='red', linewidth=0.3, alpha=0.4)
    
    ax.set_xlim(0, 10)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_ylabel("mV", fontsize=12)
    ax.grid(False)
    
    plt.tight_layout()
    
    # Save plot
    plot_path = f"static/plots/{session_id}_plot.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return plot_path

def save_data_to_csv(data, session_id, data_type):
    """Save data to CSV file"""
    csv_path = f"static/csv/{session_id}_data.csv"
    data.to_csv(csv_path, index=False)
    return csv_path

def save_features_to_csv(features, session_id):
    """Save features to CSV file"""
    if not features.empty:
        csv_path = f"static/csv/{session_id}_features.csv"
        features.to_csv(csv_path, index=False)
        return csv_path
    return None 