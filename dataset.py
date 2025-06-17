import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import neurokit2 as nk
from scipy.signal import butter, filtfilt, welch

# ---------------------- SETTINGS ----------------------
subjects = 3
sampling_rate = 256
duration = 30
n_samples = duration * sampling_rate
eeg_channels = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4',
                'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'Cz', 'Pz']
shown_channels = eeg_channels[:10]
states = ['before', 'during', 'after']

# Output folders
root_dir = os.path.abspath("mantra_brainwave_dataset")
data_dir = os.path.join(root_dir, "data")
plots_dir = os.path.join(root_dir, "plots")
os.makedirs(data_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# ---------------------- HELPERS ----------------------

def band_limited_noise(low, high, samples, sr):
    nyq = sr / 2
    b, a = butter(4, [low / nyq, high / nyq], btype='band')
    white = np.random.randn(samples)
    return filtfilt(b, a, white)

def generate_realistic_eeg(state):
    t = np.linspace(0, duration, n_samples)
    signal = []

    for _ in eeg_channels:
        if state == 'before':
            alpha = band_limited_noise(8, 12, n_samples, sampling_rate) * 50
            beta = band_limited_noise(13, 30, n_samples, sampling_rate) * 30
            gamma = band_limited_noise(30, 45, n_samples, sampling_rate) * 20
        elif state == 'during':
            alpha = band_limited_noise(8, 12, n_samples, sampling_rate) * 60
            beta = band_limited_noise(13, 30, n_samples, sampling_rate) * 25
            gamma = band_limited_noise(30, 45, n_samples, sampling_rate) * 15
        else:  # after
            alpha = band_limited_noise(8, 12, n_samples, sampling_rate) * 70
            beta = band_limited_noise(13, 30, n_samples, sampling_rate) * 20
            gamma = band_limited_noise(30, 45, n_samples, sampling_rate) * 10

        drift = np.sin(2 * np.pi * 0.2 * t) * 15
        noise = np.random.normal(0, 4, n_samples)

        spike = np.zeros_like(t)
        if np.random.rand() < 0.3:
            blink_pos = np.random.randint(n_samples - 10)
            spike[blink_pos:blink_pos + 10] = 150  # burst

        ch_signal = alpha + beta + gamma + drift + noise + spike
        signal.append(ch_signal)

    return np.array(signal)

def extract_band_power(eeg_data):
    bands = {
        "delta": (1, 4), "theta": (4, 8), "alpha": (8, 12),
        "beta": (13, 30), "gamma": (30, 45)
    }
    power = {k: [] for k in bands}
    for ch in eeg_data:
        f, Pxx = welch(ch, fs=sampling_rate)
        for band, (low, high) in bands.items():
            idx = np.logical_and(f >= low, f <= high)
            power[band].append(np.trapz(Pxx[idx], f[idx]))
    return pd.DataFrame(power)

def save_eeg(subject_path, subj_id, state):
    eeg = generate_realistic_eeg(state)
    df = pd.DataFrame(eeg.T, columns=eeg_channels)
    df.to_csv(os.path.join(subject_path, f"eeg_{state}.csv"), index=False)

    # Plot (first 10 channels for visual reference)
    fig, ax = plt.subplots(figsize=(10, 6))
    spacing = 200
    colors = plt.cm.tab10(np.linspace(0, 1, len(shown_channels)))

    for i, ch in enumerate(shown_channels):
        y = df[ch] + i * spacing
        ax.plot(df.index / sampling_rate, y, color=colors[i], linewidth=1)
        ax.text(-1, i * spacing, f"Ch {i+1:02}", fontsize=8, va='center')

    ax.set_xlim(0, 10)
    ax.set_ylim(-spacing, (len(shown_channels) + 0.5) * spacing)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title(f"Subject {subj_id} EEG - {state.upper()}")
    ax.set_yticks([])
    ax.grid(False)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f"subject_{subj_id}_eeg_{state}.png"))
    plt.close()

    band_df = extract_band_power(eeg)
    band_df.to_csv(os.path.join(subject_path, f"eeg_features_{state}.csv"), index=False)

# ---------------------- ECG UPDATED ----------------------

def generate_realistic_ecg(heart_rate):
    base_ecg = nk.ecg_simulate(duration=duration, sampling_rate=sampling_rate, heart_rate=heart_rate)
    t = np.linspace(0, duration, n_samples)

    # Enhance realism: sharp QRS, irregular amplitude spikes, slow drift
    drift = 0.05 * np.sin(2 * np.pi * 0.2 * t)
    irregular_spikes = np.where(np.random.rand(n_samples) < 0.002, np.random.uniform(0.5, 1.5, size=n_samples), 0)
    return base_ecg + drift + irregular_spikes

def save_ecg(subject_path, subj_id, state):
    hr = 90 if state == "before" else 75 if state == "during" else 65
    ecg = generate_realistic_ecg(heart_rate=hr)
    df = pd.DataFrame({"ECG": ecg})
    df.to_csv(os.path.join(subject_path, f"ecg_{state}.csv"), index=False)

    # ECG plot (simulate paper strip style)
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(df.index / sampling_rate, df["ECG"], color='black', linewidth=1)

    # Red grid like ECG paper
    ax.set_facecolor('#fffafa')
    for y in np.arange(-2, 2.5, 0.5):
        ax.axhline(y, color='red', linewidth=0.2, alpha=0.3)
    for x in np.arange(0, duration + 1, 0.2):
        ax.axvline(x, color='red', linewidth=0.2, alpha=0.3)

    ax.set_xlim(0, 10)
    ax.set_title(f"Subject {subj_id} ECG - {state.upper()}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("mV")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f"subject_{subj_id}_ecg_{state}.png"))
    plt.close()

    try:
        _, info = nk.ecg_process(ecg, sampling_rate=sampling_rate)
        hrv = nk.hrv(info, sampling_rate=sampling_rate, features=['time', 'frequency'], show=False)
        hrv.to_csv(os.path.join(subject_path, f"ecg_features_{state}.csv"), index=False)
    except Exception as e:
        print(f"⚠️ HRV extraction failed for subject {subj_id} ({state}): {e}")

# ---------------------- META ----------------------
def generate_metadata(seed):
    np.random.seed(seed)
    return {
        "age": np.random.randint(20, 50),
        "gender": np.random.choice(["Male", "Female"]),
        "stress_level": round(np.random.uniform(0.2, 1.0), 2)
    }

# ---------------------- MAIN ----------------------

for subj in range(1, subjects + 1):
    subject_path = os.path.join(data_dir, f"subject_{subj:02}")
    os.makedirs(subject_path, exist_ok=True)

    pd.DataFrame([generate_metadata(subj)]).to_csv(
        os.path.join(subject_path, "metadata.csv"), index=False)

    for state in states:
        save_eeg(subject_path, subj, state)
        save_ecg(subject_path, subj, state)

print("\n✅ Realistic EEG + ECG simulation (with clinical-style ECG) complete!")
print(f"📁 All output saved in: {root_dir}")
