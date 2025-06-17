import numpy as np
import pandas as pd
from .utils import (
    band_limited_noise, extract_band_power, create_eeg_plot, 
    save_data_to_csv, save_features_to_csv
)

class EEGGenerator:
    def __init__(self):
        self.eeg_channels = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4',
                            'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'Cz', 'Pz']
        
    def generate(self, eeg_type, duration=30, sampling_rate=256, session_id=None):
        """Generate synthetic EEG data based on type"""
        n_samples = duration * sampling_rate
        t = np.linspace(0, duration, n_samples)
        
        if eeg_type in ['normal_awake', 'sleep_stage1', 'sleep_stage2', 'sleep_stage3', 'rem_sleep']:
            eeg_data = self._generate_normal_eeg(eeg_type, n_samples, sampling_rate)
        else:
            eeg_data = self._generate_abnormal_eeg(eeg_type, n_samples, sampling_rate)
        
        # Create DataFrame
        df = pd.DataFrame(eeg_data.T, columns=self.eeg_channels)
        
        # Save data
        csv_path = save_data_to_csv(df, session_id, 'eeg')
        
        # Extract features
        features = extract_band_power(eeg_data, sampling_rate)
        features_path = save_features_to_csv(features, session_id)
        
        # Create plot
        title = f"EEG - {eeg_type.replace('_', ' ').title()}"
        plot_path = create_eeg_plot(df, self.eeg_channels, title, session_id, sampling_rate)
        
        return {
            "csv_path": csv_path,
            "features_path": features_path,
            "plot_path": plot_path,
            "channels": self.eeg_channels,
            "duration": duration,
            "sampling_rate": sampling_rate
        }
    
    def _generate_normal_eeg(self, eeg_type, n_samples, sampling_rate):
        """Generate normal EEG patterns"""
        t = np.linspace(0, n_samples / sampling_rate, n_samples)
        signal = []
        
        for _ in self.eeg_channels:
            if eeg_type == 'normal_awake':
                alpha = band_limited_noise(8, 12, n_samples, sampling_rate) * 60
                beta = band_limited_noise(13, 30, n_samples, sampling_rate) * 30
                gamma = band_limited_noise(30, 45, n_samples, sampling_rate) * 15
                
            elif eeg_type == 'sleep_stage1':
                alpha = band_limited_noise(8, 12, n_samples, sampling_rate) * 20
                theta = band_limited_noise(4, 8, n_samples, sampling_rate) * 50
                beta = band_limited_noise(13, 30, n_samples, sampling_rate) * 15
                
            elif eeg_type == 'sleep_stage2':
                theta = band_limited_noise(4, 8, n_samples, sampling_rate) * 60
                delta = band_limited_noise(1, 4, n_samples, sampling_rate) * 30
                # Add sleep spindles
                spindles = self._generate_sleep_spindles(n_samples, sampling_rate)
                
            elif eeg_type == 'sleep_stage3':
                delta = band_limited_noise(1, 4, n_samples, sampling_rate) * 80
                theta = band_limited_noise(4, 8, n_samples, sampling_rate) * 20
                
            elif eeg_type == 'rem_sleep':
                theta = band_limited_noise(4, 8, n_samples, sampling_rate) * 40
                beta = band_limited_noise(13, 30, n_samples, sampling_rate) * 35
                alpha = band_limited_noise(8, 12, n_samples, sampling_rate) * 25
            
            # Common components
            drift = np.sin(2 * np.pi * 0.1 * t) * 10
            noise = np.random.normal(0, 3, n_samples)
            
            # Eye blinks
            blink = np.zeros_like(t)
            if np.random.rand() < 0.2:
                blink_pos = np.random.randint(n_samples - 20)
                blink[blink_pos:blink_pos + 20] = 100 * np.exp(-np.arange(20) / 5)
            
            # Combine components
            if eeg_type == 'sleep_stage2':
                ch_signal = theta + delta + spindles + drift + noise + blink
            else:
                ch_signal = locals().get('alpha', 0) + locals().get('beta', 0) + \
                           locals().get('gamma', 0) + locals().get('theta', 0) + \
                           locals().get('delta', 0) + drift + noise + blink
            
            signal.append(ch_signal)
        
        return np.array(signal)
    
    def _generate_abnormal_eeg(self, eeg_type, n_samples, sampling_rate):
        """Generate abnormal EEG patterns"""
        t = np.linspace(0, n_samples / sampling_rate, n_samples)
        signal = []
        
        for ch_idx, _ in enumerate(self.eeg_channels):
            # Base signal
            alpha = band_limited_noise(8, 12, n_samples, sampling_rate) * 30
            beta = band_limited_noise(13, 30, n_samples, sampling_rate) * 20
            theta = band_limited_noise(4, 8, n_samples, sampling_rate) * 15
            noise = np.random.normal(0, 5, n_samples)
            
            # Add specific abnormalities
            if eeg_type == 'interictal_spikes':
                spikes = self._generate_interictal_spikes(n_samples, sampling_rate)
                abnormal = spikes
                
            elif eeg_type == 'spike_wave_3hz':
                spike_wave = self._generate_spike_wave_3hz(n_samples, sampling_rate)
                abnormal = spike_wave
                
            elif eeg_type == 'focal_spikes':
                focal_spikes = self._generate_focal_spikes(n_samples, sampling_rate, ch_idx)
                abnormal = focal_spikes
                
            elif eeg_type == 'polyspike':
                polyspikes = self._generate_polyspikes(n_samples, sampling_rate)
                abnormal = polyspikes
                
            elif eeg_type == 'hypsarrhythmia':
                hypsarrhythmia = self._generate_hypsarrhythmia(n_samples, sampling_rate)
                abnormal = hypsarrhythmia
                
            elif eeg_type == 'focal_slowing':
                focal_slow = self._generate_focal_slowing(n_samples, sampling_rate, ch_idx)
                abnormal = focal_slow
                
            elif eeg_type == 'diffuse_slowing':
                diffuse_slow = self._generate_diffuse_slowing(n_samples, sampling_rate)
                abnormal = diffuse_slow
                
            elif eeg_type == 'triphasic_waves':
                triphasic = self._generate_triphasic_waves(n_samples, sampling_rate)
                abnormal = triphasic
                
            elif eeg_type == 'periodic_discharges':
                periodic = self._generate_periodic_discharges(n_samples, sampling_rate)
                abnormal = periodic
                
            elif eeg_type == 'burst_suppression':
                burst_supp = self._generate_burst_suppression(n_samples, sampling_rate)
                abnormal = burst_supp
                
            elif eeg_type == 'alpha_coma':
                alpha_coma = self._generate_alpha_coma(n_samples, sampling_rate)
                abnormal = alpha_coma
                
            elif eeg_type == 'flat_eeg':
                flat = self._generate_flat_eeg(n_samples, sampling_rate)
                abnormal = flat
                
            else:
                abnormal = np.zeros(n_samples)
            
            ch_signal = alpha + beta + theta + noise + abnormal
            signal.append(ch_signal)
        
        return np.array(signal)
    
    def _generate_sleep_spindles(self, n_samples, sampling_rate):
        """Generate sleep spindles"""
        spindles = np.zeros(n_samples)
        spindle_freq = 12  # Hz
        
        # Add random spindles
        for _ in range(np.random.randint(3, 8)):
            start = np.random.randint(0, n_samples - 100)
            duration = np.random.randint(50, 100)
            t_spindle = np.linspace(0, duration / sampling_rate, duration)
            
            # Spindle envelope
            envelope = np.exp(-((t_spindle - t_spindle[duration//2]) / 0.1)**2)
            spindle_signal = envelope * np.sin(2 * np.pi * spindle_freq * t_spindle) * 50
            
            spindles[start:start + duration] += spindle_signal
            
        return spindles
    
    def _generate_interictal_spikes(self, n_samples, sampling_rate):
        """Generate interictal spikes"""
        spikes = np.zeros(n_samples)
        
        for _ in range(np.random.randint(5, 15)):
            pos = np.random.randint(0, n_samples - 50)
            # Sharp spike followed by slow wave
            spike = np.exp(-np.arange(50) / 5) * np.sin(2 * np.pi * 20 * np.arange(50) / sampling_rate) * 100
            spikes[pos:pos + 50] += spike
            
        return spikes
    
    def _generate_spike_wave_3hz(self, n_samples, sampling_rate):
        """Generate 3 Hz spike-wave complexes"""
        spike_wave = np.zeros(n_samples)
        freq = 3  # Hz
        
        # Generate multiple spike-wave complexes
        for _ in range(np.random.randint(3, 8)):
            start = np.random.randint(0, n_samples - 200)
            duration = 200
            
            t_complex = np.linspace(0, duration / sampling_rate, duration)
            # Spike followed by slow wave
            spike = np.exp(-((t_complex - 0.05) / 0.01)**2) * 150
            wave = -np.exp(-((t_complex - 0.15) / 0.05)**2) * 80
            
            complex_signal = spike + wave
            spike_wave[start:start + duration] += complex_signal
            
        return spike_wave
    
    def _generate_focal_spikes(self, n_samples, sampling_rate, ch_idx):
        """Generate focal spikes (more prominent in certain channels)"""
        spikes = np.zeros(n_samples)
        
        # Focal spikes more prominent in frontal channels
        if ch_idx in [0, 1, 2, 3]:  # Fp1, Fp2, F3, F4
            amplitude = 120
        else:
            amplitude = 30
            
        for _ in range(np.random.randint(3, 10)):
            pos = np.random.randint(0, n_samples - 30)
            spike = np.exp(-np.arange(30) / 3) * amplitude
            spikes[pos:pos + 30] += spike
            
        return spikes
    
    def _generate_polyspikes(self, n_samples, sampling_rate):
        """Generate polyspike complexes"""
        polyspikes = np.zeros(n_samples)
        
        for _ in range(np.random.randint(2, 6)):
            start = np.random.randint(0, n_samples - 100)
            
            # Multiple spikes in sequence
            for i in range(3):
                spike_pos = start + i * 20
                spike = np.exp(-np.arange(20) / 2) * 80
                polyspikes[spike_pos:spike_pos + 20] += spike
                
        return polyspikes
    
    def _generate_hypsarrhythmia(self, n_samples, sampling_rate):
        """Generate hypsarrhythmia pattern"""
        hypsarrhythmia = np.zeros(n_samples)
        
        # Chaotic high-amplitude slow waves with spikes
        for _ in range(np.random.randint(10, 20)):
            start = np.random.randint(0, n_samples - 100)
            duration = np.random.randint(50, 100)
            
            # Slow wave
            slow_wave = np.sin(2 * np.pi * 2 * np.arange(duration) / sampling_rate) * 100
            # Add spikes
            spikes = np.random.choice([0, 1], duration, p=[0.8, 0.2]) * 50
            
            hypsarrhythmia[start:start + duration] += slow_wave + spikes
            
        return hypsarrhythmia
    
    def _generate_focal_slowing(self, n_samples, sampling_rate, ch_idx):
        """Generate focal slowing"""
        focal_slow = np.zeros(n_samples)
        
        # Focal slowing in temporal channels
        if ch_idx in [12, 13]:  # T3, T4
            amplitude = 60
        else:
            amplitude = 10
            
        # Slow waves
        slow_waves = band_limited_noise(1, 4, n_samples, sampling_rate) * amplitude
        focal_slow += slow_waves
        
        return focal_slow
    
    def _generate_diffuse_slowing(self, n_samples, sampling_rate):
        """Generate diffuse slowing"""
        # Widespread slow waves
        delta = band_limited_noise(1, 4, n_samples, sampling_rate) * 50
        theta = band_limited_noise(4, 8, n_samples, sampling_rate) * 40
        
        return delta + theta
    
    def _generate_triphasic_waves(self, n_samples, sampling_rate):
        """Generate triphasic waves"""
        triphasic = np.zeros(n_samples)
        
        for _ in range(np.random.randint(3, 8)):
            start = np.random.randint(0, n_samples - 150)
            duration = 150
            
            t_wave = np.linspace(0, duration / sampling_rate, duration)
            # Three-phase wave: positive-negative-positive
            wave1 = np.exp(-((t_wave - 0.05) / 0.02)**2) * 60
            wave2 = -np.exp(-((t_wave - 0.1) / 0.02)**2) * 80
            wave3 = np.exp(-((t_wave - 0.15) / 0.02)**2) * 60
            
            triphasic[start:start + duration] += wave1 + wave2 + wave3
            
        return triphasic
    
    def _generate_periodic_discharges(self, n_samples, sampling_rate):
        """Generate periodic discharges"""
        periodic = np.zeros(n_samples)
        period = sampling_rate  # 1 second period
        
        for i in range(0, n_samples, period):
            if i + 50 < n_samples:
                # Sharp discharge
                discharge = np.exp(-np.arange(50) / 5) * 100
                periodic[i:i + 50] += discharge
                
        return periodic
    
    def _generate_burst_suppression(self, n_samples, sampling_rate):
        """Generate burst suppression pattern"""
        burst_supp = np.zeros(n_samples)
        
        # Alternating bursts and suppression
        burst_duration = sampling_rate // 2  # 0.5 seconds
        supp_duration = sampling_rate * 2  # 2 seconds
        
        i = 0
        while i < n_samples:
            # Burst
            if i + burst_duration < n_samples:
                burst = band_limited_noise(1, 30, burst_duration, sampling_rate) * 80
                burst_supp[i:i + burst_duration] += burst
                i += burst_duration
            
            # Suppression
            if i + supp_duration < n_samples:
                i += supp_duration
            else:
                break
                
        return burst_supp
    
    def _generate_alpha_coma(self, n_samples, sampling_rate):
        """Generate alpha coma pattern"""
        # Alpha activity in coma (paradoxical)
        alpha_coma = band_limited_noise(8, 12, n_samples, sampling_rate) * 40
        # Reduced reactivity
        alpha_coma *= 0.5
        
        return alpha_coma
    
    def _generate_flat_eeg(self, n_samples, sampling_rate):
        """Generate flat EEG (cerebral silence)"""
        # Very low amplitude activity
        flat = np.random.normal(0, 2, n_samples)
        
        return flat 