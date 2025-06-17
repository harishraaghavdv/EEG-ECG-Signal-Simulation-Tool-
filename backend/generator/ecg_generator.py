import numpy as np
import pandas as pd
import neurokit2 as nk
from .utils import (
    extract_hrv_features, create_ecg_plot, save_data_to_csv, save_features_to_csv
)

class ECGGenerator:
    def __init__(self):
        self.sampling_rate = 256
        
    def generate(self, ecg_type, duration=30, sampling_rate=256, session_id=None):
        """Generate synthetic ECG data based on type"""
        n_samples = duration * sampling_rate
        
        if ecg_type in ['normal_sinus', 'sinus_bradycardia', 'sinus_tachycardia']:
            ecg_data = self._generate_normal_ecg(ecg_type, n_samples, sampling_rate)
        else:
            ecg_data = self._generate_abnormal_ecg(ecg_type, n_samples, sampling_rate)
        
        # Create DataFrame
        df = pd.DataFrame({"ECG": ecg_data})
        
        # Save data
        csv_path = save_data_to_csv(df, session_id, 'ecg')
        
        # Extract HRV features
        features = extract_hrv_features(ecg_data, sampling_rate)
        features_path = save_features_to_csv(features, session_id)
        
        # Create plot
        title = f"ECG - {ecg_type.replace('_', ' ').title()}"
        plot_path = create_ecg_plot(df, title, session_id, sampling_rate)
        
        return {
            "csv_path": csv_path,
            "features_path": features_path,
            "plot_path": plot_path,
            "duration": duration,
            "sampling_rate": sampling_rate
        }
    
    def _generate_normal_ecg(self, ecg_type, n_samples, sampling_rate):
        """Generate normal ECG patterns"""
        if ecg_type == 'normal_sinus':
            heart_rate = 75
        elif ecg_type == 'sinus_bradycardia':
            heart_rate = 45
        elif ecg_type == 'sinus_tachycardia':
            heart_rate = 120
        else:
            heart_rate = 75
            
        # Generate base ECG using neurokit2
        ecg = nk.ecg_simulate(duration=n_samples/sampling_rate, 
                             sampling_rate=sampling_rate, 
                             heart_rate=heart_rate)
        
        # Add realistic variations
        ecg = self._add_realistic_variations(ecg, sampling_rate)
        
        return ecg
    
    def _generate_abnormal_ecg(self, ecg_type, n_samples, sampling_rate):
        """Generate abnormal ECG patterns"""
        # Start with normal ECG
        base_ecg = nk.ecg_simulate(duration=n_samples/sampling_rate, 
                                  sampling_rate=sampling_rate, 
                                  heart_rate=75)
        
        if ecg_type == 'first_degree_block':
            ecg = self._add_first_degree_block(base_ecg, sampling_rate)
        elif ecg_type == 'second_degree_mobitz1':
            ecg = self._add_second_degree_mobitz1(base_ecg, sampling_rate)
        elif ecg_type == 'second_degree_mobitz2':
            ecg = self._add_second_degree_mobitz2(base_ecg, sampling_rate)
        elif ecg_type == 'third_degree_block':
            ecg = self._add_third_degree_block(base_ecg, sampling_rate)
        elif ecg_type == 'lbbb':
            ecg = self._add_lbbb(base_ecg, sampling_rate)
        elif ecg_type == 'rbbb':
            ecg = self._add_rbbb(base_ecg, sampling_rate)
        elif ecg_type == 'stemi':
            ecg = self._add_stemi(base_ecg, sampling_rate)
        elif ecg_type == 'nstemi':
            ecg = self._add_nstemi(base_ecg, sampling_rate)
        elif ecg_type == 'atrial_fibrillation':
            ecg = self._add_atrial_fibrillation(base_ecg, sampling_rate)
        elif ecg_type == 'ventricular_tachycardia':
            ecg = self._add_ventricular_tachycardia(base_ecg, sampling_rate)
        elif ecg_type == 'hyperkalemia':
            ecg = self._add_hyperkalemia(base_ecg, sampling_rate)
        elif ecg_type == 'hypokalemia':
            ecg = self._add_hypokalemia(base_ecg, sampling_rate)
        elif ecg_type == 'pericarditis':
            ecg = self._add_pericarditis(base_ecg, sampling_rate)
        elif ecg_type == 'pulmonary_embolism':
            ecg = self._add_pulmonary_embolism(base_ecg, sampling_rate)
        elif ecg_type == 'digitalis_effect':
            ecg = self._add_digitalis_effect(base_ecg, sampling_rate)
        else:
            ecg = base_ecg
        
        # Add realistic variations
        ecg = self._add_realistic_variations(ecg, sampling_rate)
        
        return ecg
    
    def _add_realistic_variations(self, ecg, sampling_rate):
        """Add realistic variations to ECG signal"""
        # Add baseline wander
        t = np.linspace(0, len(ecg)/sampling_rate, len(ecg))
        baseline_wander = 0.1 * np.sin(2 * np.pi * 0.1 * t)
        
        # Add muscle artifact
        muscle_artifact = np.random.normal(0, 0.05, len(ecg))
        
        # Add respiratory variation
        respiratory = 0.05 * np.sin(2 * np.pi * 0.2 * t)
        
        return ecg + baseline_wander + muscle_artifact + respiratory
    
    def _add_first_degree_block(self, ecg, sampling_rate):
        """Add first degree AV block (prolonged PR interval)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        # Prolong PR interval by adding delay to P waves
        modified_ecg = ecg.copy()
        for r_peak in r_peaks:
            if r_peak > 100:  # Ensure we have space before R peak
                # Add P wave with prolonged PR interval
                p_wave_start = r_peak - 300  # Normal PR is ~200ms, we make it ~300ms
                if p_wave_start >= 0:
                    p_wave = 0.3 * np.exp(-((np.arange(50) - 25) / 10)**2)
                    modified_ecg[p_wave_start:p_wave_start + 50] += p_wave
        
        return modified_ecg
    
    def _add_second_degree_mobitz1(self, ecg, sampling_rate):
        """Add second degree AV block Mobitz I (Wenckebach)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        dropped_beats = 0
        
        for i, r_peak in enumerate(r_peaks[:-1]):
            if i % 4 == 3:  # Drop every 4th beat (Wenckebach pattern)
                # Remove the QRS complex
                start = max(0, r_peak - 50)
                end = min(len(ecg), r_peak + 50)
                modified_ecg[start:end] = 0
                dropped_beats += 1
        
        return modified_ecg
    
    def _add_second_degree_mobitz2(self, ecg, sampling_rate):
        """Add second degree AV block Mobitz II (fixed PR, sudden drops)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for i, r_peak in enumerate(r_peaks):
            if i % 3 == 2:  # Drop every 3rd beat
                # Remove the QRS complex
                start = max(0, r_peak - 50)
                end = min(len(ecg), r_peak + 50)
                modified_ecg[start:end] = 0
        
        return modified_ecg
    
    def _add_third_degree_block(self, ecg, sampling_rate):
        """Add third degree AV block (complete dissociation)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        # Remove most QRS complexes (ventricular escape rhythm)
        for i, r_peak in enumerate(r_peaks):
            if i % 2 == 0:  # Keep only every other beat (slow ventricular rate)
                # Remove the QRS complex
                start = max(0, r_peak - 50)
                end = min(len(ecg), r_peak + 50)
                modified_ecg[start:end] = 0
        
        # Add atrial activity (P waves) at different rate
        t = np.linspace(0, len(ecg)/sampling_rate, len(ecg))
        atrial_rate = 100  # bpm
        atrial_period = 60 / atrial_rate * sampling_rate
        
        for i in range(0, len(ecg), int(atrial_period)):
            if i + 50 < len(ecg):
                p_wave = 0.2 * np.exp(-((np.arange(50) - 25) / 8)**2)
                modified_ecg[i:i + 50] += p_wave
        
        return modified_ecg
    
    def _add_lbbb(self, ecg, sampling_rate):
        """Add left bundle branch block"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for r_peak in r_peaks:
            if r_peak + 100 < len(ecg):
                # Widen QRS complex
                qrs_start = r_peak - 60
                qrs_end = r_peak + 100
                
                # Create wide QRS with notched R wave
                qrs_duration = qrs_end - qrs_start
                t_qrs = np.linspace(0, qrs_duration/sampling_rate, qrs_duration)
                
                # Wide QRS with notching
                qrs = 1.5 * np.exp(-((t_qrs - 0.08) / 0.04)**2)
                qrs += 0.3 * np.exp(-((t_qrs - 0.12) / 0.02)**2)  # Notching
                
                modified_ecg[qrs_start:qrs_end] = qrs
        
        return modified_ecg
    
    def _add_rbbb(self, ecg, sampling_rate):
        """Add right bundle branch block"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for r_peak in r_peaks:
            if r_peak + 120 < len(ecg):
                # Widen QRS complex with R' wave
                qrs_start = r_peak - 60
                qrs_end = r_peak + 120
                
                # Create wide QRS with R' wave
                qrs_duration = qrs_end - qrs_start
                t_qrs = np.linspace(0, qrs_duration/sampling_rate, qrs_duration)
                
                # Wide QRS with R' wave
                qrs = 1.2 * np.exp(-((t_qrs - 0.08) / 0.04)**2)
                qrs += 0.8 * np.exp(-((t_qrs - 0.15) / 0.03)**2)  # R' wave
                
                modified_ecg[qrs_start:qrs_end] = qrs
        
        return modified_ecg
    
    def _add_stemi(self, ecg, sampling_rate):
        """Add ST elevation myocardial infarction"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for r_peak in r_peaks:
            if r_peak + 200 < len(ecg):
                # Add ST elevation
                st_start = r_peak + 80
                st_end = r_peak + 200
                st_duration = st_end - st_start
                
                # ST elevation pattern
                st_elevation = 0.5 * np.ones(st_duration)
                modified_ecg[st_start:st_end] += st_elevation
        
        return modified_ecg
    
    def _add_nstemi(self, ecg, sampling_rate):
        """Add non-ST elevation myocardial infarction"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for r_peak in r_peaks:
            if r_peak + 200 < len(ecg):
                # Add ST depression
                st_start = r_peak + 80
                st_end = r_peak + 200
                st_duration = st_end - st_start
                
                # ST depression pattern
                st_depression = -0.3 * np.ones(st_duration)
                modified_ecg[st_start:st_end] += st_depression
        
        return modified_ecg
    
    def _add_atrial_fibrillation(self, ecg, sampling_rate):
        """Add atrial fibrillation (irregular rhythm)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        # Remove some R peaks to create irregular rhythm
        for i, r_peak in enumerate(r_peaks):
            if np.random.random() < 0.2:  # Randomly drop 20% of beats
                start = max(0, r_peak - 50)
                end = min(len(ecg), r_peak + 50)
                modified_ecg[start:end] = 0
        
        # Add fibrillatory waves
        t = np.linspace(0, len(ecg)/sampling_rate, len(ecg))
        fibrillatory = 0.1 * np.sin(2 * np.pi * 8 * t) * np.random.random(len(ecg))
        modified_ecg += fibrillatory
        
        return modified_ecg
    
    def _add_ventricular_tachycardia(self, ecg, sampling_rate):
        """Add ventricular tachycardia"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        # Increase heart rate dramatically
        vt_rate = 180  # bpm
        vt_period = 60 / vt_rate * sampling_rate
        
        # Replace normal rhythm with VT
        for i in range(0, len(ecg), int(vt_period)):
            if i + 100 < len(ecg):
                # Wide QRS complex
                qrs = 1.5 * np.exp(-((np.arange(100) - 50) / 20)**2)
                modified_ecg[i:i + 100] = qrs
        
        return modified_ecg
    
    def _add_hyperkalemia(self, ecg, sampling_rate):
        """Add hyperkalemia effects (peaked T waves, wide QRS)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for r_peak in r_peaks:
            if r_peak + 150 < len(ecg):
                # Widen QRS
                qrs_start = r_peak - 60
                qrs_end = r_peak + 100
                qrs_duration = qrs_end - qrs_start
                qrs = 1.3 * np.exp(-((np.arange(qrs_duration) - qrs_duration//2) / 20)**2)
                modified_ecg[qrs_start:qrs_end] = qrs
                
                # Peaked T wave
                t_start = r_peak + 120
                t_end = r_peak + 180
                t_duration = t_end - t_start
                t_wave = 0.8 * np.exp(-((np.arange(t_duration) - t_duration//2) / 15)**2)
                modified_ecg[t_start:t_end] += t_wave
        
        return modified_ecg
    
    def _add_hypokalemia(self, ecg, sampling_rate):
        """Add hypokalemia effects (flattened T waves, U waves)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for r_peak in r_peaks:
            if r_peak + 200 < len(ecg):
                # Flattened T wave
                t_start = r_peak + 120
                t_end = r_peak + 160
                t_duration = t_end - t_start
                t_wave = 0.2 * np.exp(-((np.arange(t_duration) - t_duration//2) / 20)**2)
                modified_ecg[t_start:t_end] = t_wave
                
                # U wave
                u_start = r_peak + 160
                u_end = r_peak + 200
                u_duration = u_end - u_start
                u_wave = 0.3 * np.exp(-((np.arange(u_duration) - u_duration//2) / 15)**2)
                modified_ecg[u_start:u_end] += u_wave
        
        return modified_ecg
    
    def _add_pericarditis(self, ecg, sampling_rate):
        """Add pericarditis effects (diffuse ST elevation, PR depression)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for r_peak in r_peaks:
            if r_peak + 200 < len(ecg):
                # ST elevation
                st_start = r_peak + 80
                st_end = r_peak + 200
                st_duration = st_end - st_start
                st_elevation = 0.4 * np.ones(st_duration)
                modified_ecg[st_start:st_end] += st_elevation
                
                # PR depression
                if r_peak > 100:
                    pr_start = r_peak - 100
                    pr_end = r_peak - 20
                    pr_duration = pr_end - pr_start
                    pr_depression = -0.2 * np.ones(pr_duration)
                    modified_ecg[pr_start:pr_end] += pr_depression
        
        return modified_ecg
    
    def _add_pulmonary_embolism(self, ecg, sampling_rate):
        """Add pulmonary embolism effects (S1Q3T3 pattern, tachycardia)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        # Increase heart rate
        pe_rate = 110  # bpm
        pe_period = 60 / pe_rate * sampling_rate
        
        # Modify rhythm
        for i in range(0, len(ecg), int(pe_period)):
            if i + 100 < len(ecg):
                # QRS with S wave
                qrs = np.exp(-((np.arange(100) - 50) / 20)**2)
                qrs[60:100] = -0.3 * np.exp(-((np.arange(40) - 20) / 10)**2)  # S wave
                modified_ecg[i:i + 100] = qrs
        
        return modified_ecg
    
    def _add_digitalis_effect(self, ecg, sampling_rate):
        """Add digitalis effect (scooped ST, shortened QT)"""
        # Find R peaks
        r_peaks = nk.ecg_peaks(ecg, sampling_rate=sampling_rate)[1]['ECG_R_Peaks']
        
        modified_ecg = ecg.copy()
        
        for r_peak in r_peaks:
            if r_peak + 150 < len(ecg):
                # Scooped ST depression
                st_start = r_peak + 80
                st_end = r_peak + 150
                st_duration = st_end - st_start
                t_st = np.linspace(0, st_duration/sampling_rate, st_duration)
                st_depression = -0.4 * np.sin(np.pi * t_st / (st_duration/sampling_rate))
                modified_ecg[st_start:st_end] += st_depression
        
        return modified_ecg 